export module algorithms.sorting.bubble_sort;

import std;

export namespace algorithms::sorting {

    template <std::forward_iterator I, std::sentinel_for<I> S,
              class Comp = std::ranges::less, class Proj = std::identity>
        requires std::sortable<I, Comp, Proj>
    auto bubble_sort(I first, S last, Comp comp = {}, Proj proj = {}) -> I {
        I end = std::ranges::next(first, last);
        I n = end;

        while (first != n) {
            I m = first;
            bool swapped = false;

            for (I i = first, j = std::ranges::next(i); j != n; ++i, ++j) {
                if (std::invoke(comp, std::invoke(proj, *j),
                                std::invoke(proj, *i))) {
                    std::ranges::iter_swap(i, j);
                    m = std::ranges::next(j);
                    swapped = true;
                }
            }

            if (not swapped) {
                break;
            }

            n = m;
        }

        return end;
    }

    template <std::ranges::forward_range R, class Comp = std::ranges::less,
              class Proj = std::identity>
        requires std::sortable<std::ranges::iterator_t<R>, Comp, Proj>
    auto bubble_sort(R &&range, Comp comp = {}, Proj proj = {})
        -> std::ranges::borrowed_iterator_t<R> {
        if constexpr (std::ranges::borrowed_range<R>) {
            return bubble_sort(std::ranges::begin(range),
                               std::ranges::end(range), std::move(comp),
                               std::move(proj));
        } else {
            bubble_sort(std::ranges::begin(range), std::ranges::end(range),
                        std::move(comp), std::move(proj));
            return {};
        }
    }

} // namespace algorithms::sorting
