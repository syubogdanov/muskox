load("@muskox//bazel/env:cpython.bzl", "HDRS")
load("@muskox//bazel/env:cpython.bzl", "INCLUDES")
load("@muskox//bazel/env:cpython.bzl", "SRCS")
load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "cpython",
    srcs = SRCS,
    hdrs = HDRS,
    includes = INCLUDES,
    visibility = ["//visibility:public"],
)
