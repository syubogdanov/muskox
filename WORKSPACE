workspace(name = "muskox")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("//bazel/env:cpython.bzl", CPYTHON_ROOT = "ROOT")

http_archive(
    name = "argparse",
    build_file = "//third_party:argparse.BUILD",
    sha256 = "674e724c2702f0bfef1619161815257a407e1babce30d908327729fba6ce4124",
    strip_prefix = "argparse-3.0",
    url = "https://github.com/p-ranav/argparse/archive/refs/tags/v3.0.zip",
)

new_local_repository(
    name = "cpython",
    build_file = "//third_party:cpython.BUILD",
    path = CPYTHON_ROOT,
)
