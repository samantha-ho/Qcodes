from qcodes.utils.tuple_wrap import tuple_wrap_kwargs


@tuple_wrap_kwargs("a", "c", wrap_type=str)
def tuple_wrapped_strs(**kwargs):
    return kwargs


def test_str_wrap() -> None:
    test_kwargs = tuple_wrapped_strs(a="foo", b=5, c=["bar", "bar2"])
    assert type(test_kwargs["a"]) == tuple
    assert type(test_kwargs["c"]) == tuple
