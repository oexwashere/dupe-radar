import tempfile
import unittest
from pathlib import Path
import app


class Tests(unittest.TestCase):
    def test_content_groups_and_estimates(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for name, content in [
                ("a", "same"),
                ("b", "same"),
                ("c", "else"),
                ("d", "same"),
            ]:
                (p / name).write_text(content)
            r = app.scan(p)
            self.assertEqual(r["files_scanned"], 4)
            self.assertEqual(r["reclaimable_bytes"], 8)
            self.assertEqual(r["groups"][0]["files"], ["a", "b", "d"])

    def test_ignores_and_symlinks(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "a").write_text("x")
            (p / "b.tmp").write_text("x")
            (p / "link").symlink_to(p / "a")
            self.assertEqual(app.scan(p, ("*.tmp",))["files_scanned"], 1)

    def test_empty_files_are_duplicates_but_save_no_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "a").touch()
            (p / "b").touch()
            r = app.scan(p)
            self.assertEqual(len(r["groups"]), 1)
            self.assertEqual(r["reclaimable_bytes"], 0)

    def test_missing_root(self):
        with self.assertRaises(ValueError):
            app.scan("/not-a-real-dupe-radar-directory")


if __name__ == "__main__":
    unittest.main()
