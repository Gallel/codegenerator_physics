import json
from pathlib import Path

def _format_java_number(value, var_type="double"):
    """Render a numeric literal so Java types it correctly.

    A bare integer literal like 44200000000 is an int in Java and overflows
    its 2.1e9 max, even when assigned to a double. So for double-typed values
    we always emit a decimal/scientific form; ints stay as ints.
    """
    if value is None:
        return "0.0" if var_type != "int" else "0"
    # Strings: try to parse so type/value mismatches get reconciled too.
    if isinstance(value, str):
        text = value.strip()
        try:
            value = float(text)
        except ValueError:
            return text  # non-numeric (rare); pass through unchanged
    if isinstance(value, bool):
        return str(value).lower()

    f = float(value)
    if var_type == "int":
        # The DSL sometimes declares an int but carries a float value (e.g. 2.0).
        # Java rejects 'int x = 2.0;'. If the value is a whole number, emit it as
        # an int; if it actually has a fractional part, emit a double so we keep
        # precision instead of silently truncating.
        if f == int(f):
            return str(int(f))
        return repr(f)
    # double / everything else: always decimal/scientific so large ints don't
    # overflow Java's int (e.g. 44200000000 -> 44200000000.0).
    return repr(f)


def translate_op_to_java(op, declared_vars, type_map, indent="        "):
    """
    Translates a single DSL operation to a Java code line.
    """
    op_type = op.get("type")
    res = op.get("result")
    if not res: return []
    
    lines = []

    # Default type is double unless specified in type_map or op
    var_type = type_map.get(res, "double")
    
    prefix = ""
    if res not in declared_vars:
        prefix = f"{var_type} "
        declared_vars.add(res)

    def val(v):
        # Operands feed double arithmetic, so format any numeric literal as a
        # double to avoid Java int-overflow on large values (e.g. 4.42e10).
        if v is None:
            return "0.0"
        if isinstance(v, (int, float)):
            return _format_java_number(v, "double")
        try:
            float(v)
            return _format_java_number(v, "double")
        except (ValueError, TypeError):
            return str(v)

    if op_type == "assignment":
        right = val(op.get('right'))
        lines.append(f"{indent}{prefix}{res} = {right};")

    elif op_type in ["binary", "binary_literal"]:
        left = val(op.get('left') or op.get('left_var'))
        right = val(op.get('right') or op.get('literal'))
        op_char = op.get('operator')
        
        if op_char == "^":
            lines.append(f"{indent}{prefix}{res} = Math.pow({left}, {right});")
        else:
            lines.append(f"{indent}{prefix}{res} = {left} {op_char} {right};")

    elif op_type == "unary":
        arg = val(op.get('operand') or op.get('arg'))
        func = op.get('function')
        if not func: return []

        if func.lower() == "sqrt":
            polarity = op.get("solution_polarity", "positive")
            if polarity == "negative":
                lines.append(f"{indent}{prefix}{res} = -Math.sqrt({arg});")
            elif polarity == "both":
                lines.append(f"{indent}{prefix}{res} = Math.sqrt({arg});")
                # Add the negative counterpart as a secondary result
                lines.append(f"{indent}{var_type} {res}_negative = -{res};")
                declared_vars.add(f"{res}_negative")
            else:
                lines.append(f"{indent}{prefix}{res} = Math.sqrt({arg});")
        elif func.lower() == "ln":
            lines.append(f"{indent}{prefix}{res} = Math.log({arg});")
        elif func.lower() == "log":
            lines.append(f"{indent}{prefix}{res} = Math.log10({arg});")
        elif func.lower() in ["sin", "cos", "tan"]:
            lines.append(f"{indent}{prefix}{res} = Math.{func.lower()}({arg});")
        else:
            lines.append(f"{indent}{prefix}{res} = {func}({arg});")
            
    elif op_type == "module_call":
        mod_id = op.get("module")
        args_dict = op.get("args", {})
        # Map values properly
        arg_list = [val(v) for v in args_dict.values()]
        args_str = ", ".join(arg_list)
        lines.append(f"{indent}{prefix}{res} = {mod_id}({args_str});")

    return lines

def parse_dsl_to_java(json_path: Path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data.get("metadata", {})
    class_name = metadata.get("name", json_path.stem)
    
    main_decls = data.get("main_declarations", data.get("declarations", []))
    definitions = data.get("definitions", [])
    execution_flow = data.get("execution_flow", data.get("operations", []))
    
    # Pre-scan definitions for return types
    mod_return_types = {m["id"]: m.get("return_type", "double") for m in definitions}
    
    # Global type map for variables
    type_map = {d["name"]: d.get("type", "double") for d in main_decls}
    for op in execution_flow:
        if op.get("type") == "module_call":
            res = op.get("result")
            mod_id = op.get("module")
            if res and mod_id in mod_return_types:
                type_map[res] = mod_return_types[mod_id]

    lines = [
        "/**",
        f" * Generated Physics-Validated Program: {class_name}",
        " * Automatically generated from Modular DSL.",
        " */",
        f"public class {class_name} {{",
        "",
        "    public static void main(String[] args) {",
        "        // --- Main Declarations ---"
    ]
    
    main_vars = set()
    for decl in main_decls:
        name = decl.get("name")
        v_type = decl.get("type", "double")
        raw_val = decl.get("value", 0.0)
        val_str = _format_java_number(raw_val, v_type)
        sem = decl.get("semantics", {})
        quant = sem.get("quantity", "").split("#")[-1]
        lines.append(f"        {v_type} {name} = {val_str}; // {quant}")
        main_vars.add(name)
        
    lines.append("")
    lines.append("        // --- Main Execution Flow ---")
    for op in execution_flow:
        lines.extend(translate_op_to_java(op, main_vars, type_map))
        
    # Print final results
    results_to_print = data.get("results_to_print")
    
    if results_to_print:
        leaf_results = results_to_print
    else:
        # Fallback to leaf detection if results_to_print is missing
        all_produced = set()
        all_consumed = set()
        for op in execution_flow:
            res = op.get("result") or op.get("left")
            if res:
                all_produced.add(res)
                if op.get("type") == "unary" and op.get("function", "").lower() == "sqrt" and op.get("solution_polarity") == "both":
                    all_produced.add(f"{res}_negative")
                    
            op_type = op.get("type")
            if op_type == "assignment": all_consumed.add(op.get("right"))
            elif op_type in ["binary", "binary_literal"]: 
                all_consumed.update([op.get("left") or op.get("left_var"), op.get("right") or op.get("literal")])
            elif op_type in ["unary", "unary_literal"]: all_consumed.add(op.get("operand") or op.get("arg"))
            elif op_type == "module_call":
                args = op.get("args", {})
                if isinstance(args, dict): all_consumed.update(args.values())
        leaf_results = [p for p in all_produced if p not in all_consumed]

    # Final printing for results
    lines.append("        // --- Output Results in JSON format ---")
    lines.append('        System.out.println("{");')
    lines.append(f'        System.out.println("  \\"problem\\": \\"{metadata.get("name", "Unknown")}\\",");')
    lines.append('        System.out.println("  \\"results\\": {");')
    for i, res in enumerate(leaf_results):
        comma = "," if i < len(leaf_results) - 1 else ""
        lines.append(f'        System.out.println("    \\"{res}\\": " + {res} + "{comma}");')
    lines.append('        System.out.println("  }");')
    lines.append('        System.out.println("}");')
            
    lines.append("    }")
    lines.append("")

    # Module definitions
    for mod in definitions:
        mod_id = mod.get("id")
        inputs = mod.get("inputs", [])
        output_var = mod.get("output_var")
        ret_type = mod.get("return_type", "double")
        ops = mod.get("operations", [])
        
        # Build local type map and signature
        local_type_map = {}
        input_decls = []
        for inp in inputs:
            i_name = inp["name"] if isinstance(inp, dict) else inp
            i_type = inp["type"] if isinstance(inp, dict) else "double"
            local_type_map[i_name] = i_type
            input_decls.append(f"{i_type} {i_name}")
            
        args_decl = ", ".join(input_decls)
        lines.append(f"    /** {mod.get('description', '')} */")
        lines.append(f"    public static {ret_type} {mod_id}({args_decl}) {{")
        
        local_vars = set([inp["name"] if isinstance(inp, dict) else inp for inp in inputs])
        for op in ops:
            lines.extend(translate_op_to_java(op, local_vars, local_type_map, indent="        "))
        
        if output_var:
            lines.append(f"        return {output_var};")
        elif ops:
            last_op_res = ops[-1].get("result")
            lines.append(f"        return {last_op_res};")
        else:
            lines.append(f"        return ({ret_type})0;")
            
        lines.append("    }")
        lines.append("")

    lines.append("}")
    
    output_java = json_path.parent / f"{class_name}.java"
    with open(output_java, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"[JAVA_EMITTER] Generated Validated Java code at: {output_java}")
    return output_java
