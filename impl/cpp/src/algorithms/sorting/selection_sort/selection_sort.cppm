export module algorithms.sorting.selection_sort;

import std;

export namespace algorithms::sorting {

    template <std::forward_iterator I, std::sentinel_for<I> S,
              class Comp = std::ranges::less, class Proj = std::identity>
        requires std::sortable<I, Comp, Proj>
    auto selection_sort(I first, S last, Comp comp = {}, Proj proj = {}) -> I {
        I n = std::ranges::next(first, last);

        for (I i = first; i != n; ++i) {
            I minimum = i;

            for (I j = std::ranges::next(i); j != n; ++j) {
                if (std::invoke(comp, std::invoke(proj, *j),
                                std::invoke(proj, *minimum))) {
                    minimum = j;
                }
            }

            std::ranges::iter_swap(i, minimum);
        }

        return n;
    }

    template <std::ranges::forward_range R, class Comp = std::ranges::less,
              class Proj = std::identity>
        requires std::sortable<std::ranges::iterator_t<R>, Comp, Proj>
    auto selection_sort(R &&range, Comp comp = {}, Proj proj = {})
        -> std::ranges::borrowed_iterator_t<R> {
        if constexpr (std::ranges::borrowed_range<R>) {
            return selection_sort(std::ranges::begin(range),
                                  std::ranges::end(range), std::move(comp),
                                  std::move(proj));
        } else {
            selection_sort(std::ranges::begin(range), std::ranges::end(range),
                           std::move(comp), std::move(proj));
            return {};
        }
    }

} // namespace algorithms::sorting
