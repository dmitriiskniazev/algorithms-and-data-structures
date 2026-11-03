import tracemalloc

from algorithms.dynamic_programming import edit_distance


def test_edit_distance_examples_and_boundaries() -> None:
    assert edit_distance.compute("kitten", "sitting") == 3
    assert edit_distance.compute("", "abc") == 3
    assert edit_distance.compute("same", "same") == 0


def test_edit_alignment_transforms_source_with_minimum_cost() -> None:
    source, target = "intention", "execution"
    distance, edits = edit_distance.align(source, target)
    assert distance == edit_distance.compute(source, target)
    assert "".join(edit.source for edit in edits if edit.source is not None) == source
    assert "".join(edit.target for edit in edits if edit.target is not None) == target
    assert sum(edit.kind != "match" for edit in edits) == distance


def test_equal_strings_align_only_matches() -> None:
    assert edit_distance.align("abc", "abc") == (0, [("match", "a", "a"), ("match", "b", "b"), ("match", "c", "c")])


def test_distance_uses_short_row_without_retaining_history() -> None:
    short, long = "aaaa", "a" * 2000
    for source, target in ((short, long), (long, short)):
        tracemalloc.start()
        try:
            assert edit_distance.compute(source, target) == 1996
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert peak < 64 * 1024


def test_alignment_history_does_not_allocate_edits_for_every_cell() -> None:
    source, target = "a" * 100, "b" * 100
    tracemalloc.start()
    try:
        distance, parent = edit_distance.build_parents(source, target)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert distance == 100
    assert peak < 100 * 1024
    edits = edit_distance.restore_from_parents(source, target, parent)
    assert len(edits) == 100
    assert all(edit.kind == "replace" for edit in edits)
