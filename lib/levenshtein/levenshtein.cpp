#include "levenshtein.hpp"

#include <algorithm>
#include <limits>
#include <stdexcept>
#include <vector>

std::size_t levenshtein::levenshtein(const std::string& lh, const std::string& rh)
{
    if (lh.length() > rh.length())
    {
        return levenshtein::levenshtein(rh, lh);
    }

    if (lh.length() == 0)
    {
        return rh.length();
    }

    if (rh.length() == 0)
    {
        return lh.length();
    }

    if (lh.length() == std::numeric_limits<std::size_t>::max())
    {
        throw std::overflow_error("The strings are too long");
    }

    std::vector<std::size_t> previous_row(lh.length() + 1, 0);
    std::vector<std::size_t> current_row(lh.length() + 1, 0);

    for (std::size_t index = 1; index <= lh.length(); ++index)
    {
        previous_row[index] = index;
    }

    for (std::size_t rh_index = 0; rh_index < rh.length(); ++rh_index)
    {
        current_row[0] = rh_index + 1;
        for (std::size_t lh_index = 0; lh_index < lh.length(); ++lh_index)
        {
            std::size_t deletion = previous_row[lh_index + 1] + 1;
            std::size_t insertion = current_row[lh_index] + 1;

            bool equal_symbols = (lh[lh_index] == rh[rh_index]);
            std::size_t substitution = previous_row[lh_index] + ((equal_symbols) ? 0 : 1);

            current_row[lh_index + 1] = std::min({
                deletion,
                insertion,
                substitution,
            });
        }
        std::swap(previous_row, current_row);
    }

    return previous_row[lh.length()];
}
