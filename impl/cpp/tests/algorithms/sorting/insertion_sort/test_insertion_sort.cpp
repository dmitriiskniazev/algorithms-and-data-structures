import std;
import algorithms.sorting;

int main() {
    std::list values{5, 2, 4, 6, 1, 3};
    auto end =
        algorithms::sorting::insertion_sort(values.begin(), values.end());

    if (not std::ranges::equal(values, std::array{1, 2, 3, 4, 5, 6}) or
        end != values.end()) {
        throw std::runtime_error("insertion_sort failed for iterator pair");
    }

    std::array records{std::pair{2, 'a'}, std::pair{1, 'b'}, std::pair{2, 'c'},
                       std::pair{1, 'd'}};
    algorithms::sorting::insertion_sort(records, std::ranges::greater{},
                                        &std::pair<int, char>::first);

    if (records != std::array{std::pair{2, 'a'}, std::pair{2, 'c'},
                              std::pair{1, 'b'}, std::pair{1, 'd'}}) {
        throw std::runtime_error(
            "insertion_sort failed for projection or stability");
    }
}
