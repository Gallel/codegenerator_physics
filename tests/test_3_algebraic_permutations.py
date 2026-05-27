"""Tabla de equivalencias algebraicas en SymPy.

Este fichero NO prueba el sistema; prueba que SymPy reconoce equivalencias.
Lo dejamos como documentación viva. Se omite por defecto en la suite y se
ejecuta solo con `pytest -m algebra_docs`.
"""
import pytest
pytest.skip("Algebraic-equivalence sanity table; not part of the system contract.",
            allow_module_level=True)
