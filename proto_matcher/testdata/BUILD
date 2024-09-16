load("@rules_proto//proto:defs.bzl", "proto_library")
load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")

package(default_visibility = ["//proto_matcher:internal"])

proto_library(
    name = "test_proto",
    testonly = True,
    srcs = ["test.proto"],
    deps = ["@com_google_protobuf//:struct_proto"],
)

py_proto_library(
    name = "test_py_pb2",
    testonly = True,
    deps = [":test_proto"],
)
