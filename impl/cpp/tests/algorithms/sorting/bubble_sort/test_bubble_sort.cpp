import std;
import algorithms.sorting;

int main() {
    std::forward_list values{5, 1, 4, 2, 8};
    auto end = algorithms::sorting::bubble_sort(values);

    if (not std::ranges::equal(values, std::array{1, 2, 4, 5, 8}) or
        end != values.end()) {
        throw std::runtime_error("bubble_sort failed for a forward range");
    }

    std::array counted_values{4, 2, 3, 1};
    auto first = std::counted_iterator(counted_values.begin(), 4);
    auto counted_end =
        algorithms::sorting::bubble_sort(first, std::default_sentinel);

    if (not std::ranges::equal(counted_values, std::array{1, 2, 3, 4}) or
        counted_end.count() != 0) {
        throw std::runtime_error("bubble_sort failed for a distinct sentinel");
    }

    std::array records{std::pair{2, 'a'}, std::pair{1, 'b'}, std::pair{2, 'c'},
                       std::pair{1, 'd'}};
    algorithms::sorting::bubble_sort(records, std::ranges::less{},
                                     &std::pair<int, char>::first);

    if (records != std::array{std::pair{1, 'b'}, std::pair{1, 'd'},
                              std::pair{2, 'a'}, std::pair{2, 'c'}}) {
        throw std::runtime_error("bubble_sort failed to preserve stability");
    }
}
