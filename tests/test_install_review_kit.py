"""Standard-library tests. All installations use temporary directories."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_review_kit", ROOT / "scripts/install-review-kit.py")
kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit)


class InstallReviewKitTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.target = self.root / "target"
        self.source = self.root / "source"
        for relative in kit.ASSETS:
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("new " + relative, encoding="utf-8")

    def test_preview_makes_no_directory(self):
        result = kit.install(self.source, self.target)
        self.assertIn("DRY RUN", result[0])
        self.assertFalse(self.target.exists())

    def test_install_and_idempotent_rerun(self):
        kit.install(self.source, self.target, apply=True)
        for relative in kit.ASSETS:
            self.assertEqual((self.target / relative).read_bytes(), (self.source / relative).read_bytes())
        result = kit.install(self.source, self.target, apply=True)
        self.assertEqual(sum(line.startswith("KEEP:") for line in result), 4)
        self.assertFalse((self.target / ".review-kit-backups").exists())

    def test_conflict_refuses_all_writes(self):
        existing = self.target / kit.ASSETS[0]
        existing.parent.mkdir(parents=True)
        existing.write_text("my rule", encoding="utf-8")
        with self.assertRaises(ValueError):
            kit.install(self.source, self.target, apply=True)
        self.assertEqual(existing.read_text(), "my rule")
        self.assertFalse((self.target / "agents").exists())

    def test_overwrite_preserves_backup_and_other_settings(self):
        kit.install(self.source, self.target, apply=True)
        existing = self.target / kit.ASSETS[0]
        existing.write_text("my old rule", encoding="utf-8")
        settings = self.target / "settings.json"
        settings.write_text('{"theme":"light"}', encoding="utf-8")
        kit.install(self.source, self.target, apply=True, overwrite=True)
        backups = list((self.target / ".review-kit-backups").glob("*/rules/review-first.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "my old rule")
        self.assertEqual(settings.read_text(), '{"theme":"light"}')

    def test_missing_source_causes_no_writes(self):
        (self.source / kit.ASSETS[-1]).unlink()
        with self.assertRaises(ValueError):
            kit.install(self.source, self.target, apply=True)
        self.assertFalse(self.target.exists())

    def test_refuses_symlink_root(self):
        other = self.root / "other"
        other.mkdir()
        self.target.symlink_to(other, target_is_directory=True)
        with self.assertRaises(ValueError):
            kit.install(self.source, self.target, apply=True)
        self.assertEqual(list(other.iterdir()), [])

    def test_refuses_symlink_file(self):
        self.target.mkdir()
        outside = self.root / "outside.md"
        outside.write_text("keep", encoding="utf-8")
        destination = self.target / kit.ASSETS[0]
        destination.parent.mkdir()
        destination.symlink_to(outside)
        with self.assertRaises(ValueError):
            kit.install(self.source, self.target, apply=True, overwrite=True)
        self.assertEqual(outside.read_text(), "keep")

    def test_refuses_file_in_parent_path(self):
        self.target.mkdir()
        (self.target / "skills").write_text("not a directory", encoding="utf-8")
        with self.assertRaises(ValueError):
            kit.install(self.source, self.target, apply=True)
        self.assertFalse((self.target / "rules").exists())


if __name__ == "__main__":
    unittest.main()
