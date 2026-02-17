import pytest

from pycps_sysmlv2.type_utils import evaluate_type, get_primitive_type, is_list, parse_literal, value_iterator


@pytest.mark.parametrize(
    ("value", "expected_value", "expected_type"),
    [
        (True, True, "Boolean"),
        (42, 42, "Integer"),
        (3.14, 3.14, "Real"),
        ("abc", "abc", "String"),
        ([1, 2, 3], [1, 2, 3], "List[Integer]"),
        ((1.0, 2.0), [1.0, 2.0], "List[Real]"),
        ([], [], "List[]"),
    ],
)
def test_evaluate_type_identifies_python_primitives_and_lists(
    value, expected_value, expected_type
):
    parsed, type_name = evaluate_type(value)
    assert parsed == expected_value
    assert type_name == expected_type


@pytest.mark.parametrize(
    ("type_name", "expected"),
    [
        ("List[Integer]", True),
        ("List[]", True),
        ("Integer", False),
        ("Boolean", False),
    ],
)
def test_is_list_detects_list_type_names(type_name, expected):
    assert is_list(type_name) is expected


@pytest.mark.parametrize(
    ("type_name", "expected"),
    [
        ("List[Integer]", "Integer"),
        ("List[Real]", "Real"),
        ("Integer", "Integer"),
        ("String", "String"),
    ],
)
def test_get_type_returns_inner_type_for_lists(type_name, expected):
    assert get_primitive_type(type_name) == expected


@pytest.mark.parametrize(
    ("literal", "expected_value", "expected_type"),
    [
        (None, None, None),
        ("", None, None),
        ("   ", None, None),
        ("true", True, "Boolean"),
        ("FALSE", False, "Boolean"),
        ("42", 42, "Integer"),
        ("3.5", 3.5, "Real"),
        ("1e-3", 0.001, "Real"),
        ("[1, 2, 3]", [1, 2, 3], "List[Integer]"),
        ("[]", [], "List[]"),
        ('"quoted"', "quoted", "String"),
        ("unquoted_text", "unquoted_text", "String"),
    ],
)
def test_parse_literal_returns_value_and_identified_type(
    literal, expected_value, expected_type
):
    parsed, type_name = parse_literal(literal)
    assert parsed == expected_value
    assert type_name == expected_type


@pytest.mark.parametrize(
    ("value", "expected_value"),
    [
        (True, [True]),
        (42, [42]),
        (3.14, [3.14]),
        ("abc", ["abc"]),
        ([1, 2, 3], [1, 2, 3]),
        ((1.0, 2.0), [1.0, 2.0]),
        ([], []),
    ],
)
def test_evaluate_value_generator(
    value, expected_value
):
    out = []
    for i in value_iterator(value):
        out.append(i)
    assert out == expected_value
