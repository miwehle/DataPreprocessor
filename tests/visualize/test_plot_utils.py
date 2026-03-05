from datapreprocessor.visualize.plot_utils import format_wrapped_label


def test_format_wrapped_label_prefers_break_before_opening_paren() -> None:
    label = "is_too_long(max_chars=500)"
    wrapped = format_wrapped_label(label, width=16)
    assert wrapped == "is too long\n(max chars=500)"


def test_format_wrapped_label_keeps_short_label_on_one_line() -> None:
    label = "contains_email"
    wrapped = format_wrapped_label(label, width=30)
    assert wrapped == "contains email"
