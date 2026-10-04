export module algorithms.sorting.insertion_sort;

import std;

export namespace algorithms::sorting {

    template <std::bidirectional_iterator I, std::sentinel_for<I> S,
              class Comp = std::ranges::less, class Proj = std::identity>
        requires std::sortable<I, Comp, Proj>
    auto insertion_sort(I first, S last, Comp comp = {}, Proj proj = {}) -> I {
        I n = std::ranges::next(first, last);
        I i = first;

        if (i != n) {
            ++i;
        }

        while (i != n) {
            I j = i;

            while (j != first) {
                I k = std::ranges::prev(j);

                if (not std::invoke(comp, std::invoke(proj, *j),
                                    std::invoke(proj, *k))) {
                    break;
                }

                std::ranges::iter_swap(j, k);
                j = k;
            }

            ++i;
        }

        return n;
    }

    template <std::ranges::bidirectional_range R,
              class Comp = std::ranges::less, class Proj = std::identity>
        requires std::sortable<std::ranges::iterator_t<R>, Comp, Proj>
    auto insertion_sort(R &&range, Comp comp = {}, Proj proj = {})
        -> std::ranges::borrowed_iterator_t<R> {
        if constexpr (std::ranges::borrowed_range<R>) {
            return insertion_sort(std::ranges::begin(range),
                                  std::ranges::end(range), std::move(comp),
                                  std::move(proj));
        } else {
            insertion_sort(std::ranges::begin(range), std::ranges::end(range),
                           std::move(comp), std::move(proj));
            return {};
        }
    }

} // namespace algorithms::sorting
