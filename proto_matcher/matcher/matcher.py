from __future__ import annotations

from typing import Union

from google.protobuf import message
from google.protobuf import text_format
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

from proto_matcher.compare import ProtoComparisonOptions
from proto_matcher.compare import ProtoComparisonScope
from proto_matcher.compare import ProtoFloatComparison
from proto_matcher.compare import RepeatedFieldComparison
from proto_matcher.compare import proto_compare

_ProtoValue = Union[str, message.Message]

# Declared as the plain hamcrest interface (not _EqualsProto) so that pyright
# resolves compositions like not_(equals_proto(...)) to Matcher[Message].
_ProtoMatcher = Matcher[message.Message]


class _EqualsProto(BaseMatcher[message.Message]):
    def __init__(self, msg: _ProtoValue):
        self._msg = msg
        self._opts = ProtoComparisonOptions()

    def mut_options(self) -> ProtoComparisonOptions:
        return self._opts

    def matches(
        self, item: message.Message, mismatch_description: Description | None = None
    ) -> bool:
        if isinstance(self._msg, str):
            proto_type = type(item)
            expected = text_format.Parse(self._msg, proto_type())
        else:
            expected = self._msg
        cmp_result = proto_compare(item, expected, opts=self._opts)
        if not cmp_result.is_equal and mismatch_description:
            mismatch_description.append_text(cmp_result.explanation)
        return cmp_result.is_equal

    def describe_mismatch(
        self, item: message.Message, mismatch_description: Description
    ):
        self.matches(item, mismatch_description)

    def describe_to(self, description: Description):
        description.append_text(f"a protobuf of:\n{self._msg}")


def equals_proto(expected: _ProtoValue) -> _ProtoMatcher:
    return _EqualsProto(expected)


def partially(matcher: _ProtoMatcher) -> _ProtoMatcher:
    _mut_options(matcher).scope = ProtoComparisonScope.PARTIAL
    return matcher


def approximately(
    matcher: _ProtoMatcher,
    float_margin: float | None = None,
    float_fraction: float | None = None,
) -> _ProtoMatcher:
    opts = _mut_options(matcher)
    opts.float_comp = ProtoFloatComparison.APPROXIMATE
    if float_margin:
        opts.float_margin = float_margin
    if float_fraction:
        opts.float_fraction = float_fraction
    return matcher


def ignoring_field_paths(
    field_paths: set[tuple[str, ...]], matcher: _ProtoMatcher
) -> _ProtoMatcher:
    opts = _mut_options(matcher)
    opts.ignore_field_paths = field_paths
    return matcher


def ignoring_repeated_field_ordering(matcher: _ProtoMatcher) -> _ProtoMatcher:
    opts = _mut_options(matcher)
    opts.repeated_field_comp = RepeatedFieldComparison.AS_SET
    return matcher


def _mut_options(matcher: _ProtoMatcher) -> ProtoComparisonOptions:
    if not isinstance(matcher, _EqualsProto):
        raise TypeError(
            f"proto matcher modifiers only compose with equals_proto, got {matcher}"
        )
    return matcher.mut_options()
