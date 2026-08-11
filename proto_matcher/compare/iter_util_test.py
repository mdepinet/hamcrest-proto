import unittest

from proto_matcher.compare import iter_util


class ZipPairsTest(unittest.TestCase):
    def test_unkeyed_pairs_align_by_index(self):
        self.assertEqual(
            list(iter_util.zip_pairs(["a", "b", "c"], ["d", "e"])),
            [("a", "d"), ("b", "e"), ("c", None)],
        )

    def test_unkeyed_pairs_pad_shorter_first_iterable(self):
        self.assertEqual(
            list(iter_util.zip_pairs(["a"], ["b", "c"])),
            [("a", "b"), (None, "c")],
        )

    def test_keyed_pairs_align_by_key(self):
        self.assertEqual(
            list(iter_util.zip_pairs([3, 1], [2, 3], key=lambda x: x)),
            [(1, None), (None, 2), (3, 3)],
        )


if __name__ == "__main__":
    unittest.main()
