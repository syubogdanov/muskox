#include <cstdlib>
#include <iostream>
#include <string>

#include <include/argparse/argparse.hpp>

#include "src/config/config.hpp"

namespace cli_default
{

const int threads = 8;

} // namespace cli_default

int main(int argc, char *argv[])
{
    auto cli_parser = argparse::ArgumentParser(
        config::program_name,
        config::version
    );

    cli_parser.add_argument("lhs")
        .help("the ox path to the first object")
        .metavar("OXPATH");

    cli_parser.add_argument("rhs")
        .help("the ox path to the second object")
        .metavar("OXPATH");

    cli_parser.add_argument("-t", "--threads")
        .help("maximum number of threads")
        .scan<'i', int>()
        .default_value(cli_default::threads)
        .nargs(1)
        .metavar("N");

    try {
        cli_parser.parse_args(argc, argv);
    }

    catch (const std::exception& exception) {
        std::cerr << exception.what() << std::endl;
        std::cerr << cli_parser << std::endl;
        std::exit(EXIT_FAILURE);
    }

    return EXIT_SUCCESS;
}
