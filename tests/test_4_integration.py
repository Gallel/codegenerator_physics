"""
Phase 4: Integration Validation
Validates the extraction of humanly-readable feedback dynamically from
the validator pipeline using Python ASTs mapped back from OWL logic.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from owlready2 import get_ontology
from src.validator import describe_error

class DummyOWLInstance:
    """Mocking an OWL instance since we are unit testing the string formatter isolated from Pellet."""
    def __init__(self, name, props_dict=None):
        self.name = name
        self.props = props_dict or {}

    def get_properties(self):
        # We don't necessarily need to implement the deep property iterator for basic describe tests.
        return []

    def __getattr__(self, name):
        if name in self.props:
            return self.props[name]
        return []

class DummyOWLLabel:
    def __init__(self, name_val):
        self.name = name_val

def test_describe_quantity_incompatibility_feedback():
    """Ensure the validator correctly extracts contextual operands from the graph for LLM Feedback."""
    
    left_q = DummyOWLLabel("MassQuantity")
    right_q = DummyOWLLabel("TimeQuantity")
    
    left_op = DummyOWLInstance("Measurement_m1", {"hasQuantityType": [left_q]})
    right_op = DummyOWLInstance("Measurement_t1", {"hasQuantityType": [right_q]})
    
    error_instance = DummyOWLInstance(
        name="AdditionOperation_3", 
        props_dict={
            "hasLeftOperand": [left_op],
            "hasRightOperand": [right_op]
        }
    )
    
    description = describe_error("Physics.QuantityIncompatibilityError", error_instance)
    
    # Check that it identifies the operands
    assert "Measurement_m1" in description
    assert "Measurement_t1" in description
    
    # Check that it identifies the mismatching types extracted
    assert "MassQuantity" in description
    assert "TimeQuantity" in description
    
    # Check Context marker
    assert "CONTEXTO " in description

def test_describe_trigonometry_feedback():
    """Ensure trigonometry extraction yields AngleQuantity missing context."""
    op_q = DummyOWLLabel("MassQuantity")
    op = DummyOWLInstance("Measurement_mass", {"hasQuantityType": [op_q]})
    
    error_instance = DummyOWLInstance(
        name="SineExpression_1",
        props_dict={"hasOperand": [op]}
    )
    
    description = describe_error("Physics.InvalidTrigonometryArgumentError", error_instance)
    
    assert "AngleQuantity" in description
    assert "MassQuantity" in description
    assert "Measurement_mass" in description
