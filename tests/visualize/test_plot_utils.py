from datapreprocessor.visualize.plot_utils import format_wrapped_label
from datapreprocessor.visualize.plot_utils import integer_histogram_bins


def test_format_wrapped_label_prefers_break_before_opening_paren() -> None:
    label = "is_too_long(max_chars=500)"
    wrapped = format_wrapped_label(label, width=16)
    assert wrapped == "is too long\n(max chars=500)"


def test_format_wrapped_label_keeps_short_label_on_one_line() -> None:
    label = "contains_email"
    wrapped = format_wrapped_label(label, width=30)
    assert wrapped == "contains email"


def test_integer_histogram_bins_scales_step_to_cap_bin_count() -> None:
    bins = integer_histogram_bins([1, 2, 3], [100], max_bins=10)
    assert len(bins) <= 11
    assert bins[0] <= 0.5
    assert bins[-1] >= 100.5


def test_integer_histogram_bins_empty_fallback() -> None:
    bins = integer_histogram_bins([], [], max_bins=10)
    assert bins == [-0.5, 0.5]
