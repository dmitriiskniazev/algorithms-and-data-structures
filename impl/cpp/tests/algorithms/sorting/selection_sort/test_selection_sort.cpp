import std;
import algorithms.sorting;

int main() {
    std::array values{64, 25, 12, 22, 11};
    auto end = algorithms::sorting::selection_sort(values);

    if (not std::ranges::equal(values, std::array{11, 12, 22, 25, 64}) or
        end != values.end()) {
        throw std::runtime_error("selection_sort failed for a range");
    }

    std::forward_list descending{1, 3, 2, 5, 4};
    algorithms::sorting::selection_sort(descending, std::ranges::greater{});

    if (not std::ranges::equal(descending, std::array{5, 4, 3, 2, 1})) {
        throw std::runtime_error(
            "selection_sort failed for a custom comparator");
    }
}
