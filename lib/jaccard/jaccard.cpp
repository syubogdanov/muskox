#include "jaccard.hpp"

#include <set>
#include <limits>
#include <iterator>
#include <iostream>

void split_string_to_set(std::set<std::string>& res, const std::string& str, char d = ' ') {
    std::string actual_word;
    for (size_t i = 0; i < str.size(); i++) {
        if (str.at(i) != d) {
            actual_word += str.at(i);
        } else {
            res.insert(actual_word);
            actual_word = "";
        }
    }
    if (!actual_word.empty()) {
        res.insert(actual_word);
    }
}

double jaccard::jaccard_coefficient(const std::string& lh, const std::string& rh) {
    std::set<std::string> lh_set;
    std::set<std::string> rh_set;
    split_string_to_set(lh_set, lh);
    split_string_to_set(rh_set, rh);

    if (lh_set.empty()|| rh_set.empty()) {
        return 0.0;
    }

    std::set<std::string> set_intersect;

    std::set_intersection(lh_set.begin(), lh_set.end(),
                          rh_set.begin(), rh_set.end(),
                          std::inserter(set_intersect, set_intersect.begin()));

    double len_intersect = static_cast<double>(set_intersect.size());
    double len_set_lh = static_cast<double>(lh_set.size());
    double len_set_rh = static_cast<double>(rh_set.size());

    double jaccard_coef = len_intersect / (len_set_lh + len_set_rh - len_intersect);

    return jaccard_coef;
}
