import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT / "product_development"
NAMES = {
    "new-product-from-scratch",
    "product-discovery-to-scope",
    "product-scope-to-prd",
    "product-prototype-build",
    "product-market-testing",
    "prototype-to-production",
}
spec = importlib.util.spec_from_file_location("install_skills", ROOT / "scripts/install_skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def local_links(path):
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
        if not target.startswith(("https://", "http://", "#")):
            yield path.parent / target.split("#", 1)[0]


class PackagingTests(unittest.TestCase):
    def test_complete_family_and_metadata(self):
        skills = list(FAMILY.glob("*/SKILL.md"))
        self.assertEqual({path.parent.name for path in skills}, NAMES)
        for path in skills:
            with self.subTest(skill=path.parent.name):
                frontmatter = path.read_text().split("---", 2)[1].strip().splitlines()
                self.assertIn(f"name: {path.parent.name}", frontmatter)
                self.assertEqual(len(frontmatter), 2)
                self.assertTrue(frontmatter[1].startswith("description: "))
                metadata = path.parent / "agents/openai.yaml"
                self.assertTrue(metadata.is_file())
                self.assertIn(f"${path.parent.name}", metadata.read_text())

    def test_family_and_engineering_links_resolve(self):
        files = list(FAMILY.rglob("*.md"))
        files.append(ROOT / "playbooks/new-web-app-from-scratch/SKILL.md")
        files.extend([ROOT / "README.md", ROOT / "CLAUDE.md"])
        for path in files:
            for target in local_links(path):
                with self.subTest(source=path, target=target):
                    self.assertTrue(target.exists(), str(target))

    def test_documentation_section_links_resolve(self):
        files = list(FAMILY.rglob("*.md")) + [ROOT / "README.md", ROOT / "CLAUDE.md"]
        for path in files:
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if "#" not in link or link.startswith(("https://", "http://")):
                    continue
                filename, fragment = link.split("#", 1)
                destination = path.parent / filename if filename else path
                headings = re.findall(r"^#{1,6} +(.+)$", destination.read_text(), re.MULTILINE)
                anchors = {
                    re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
                    for heading in headings
                }
                with self.subTest(source=path, link=link):
                    self.assertIn(fragment, anchors)

    def test_installed_links_preserve_shared_and_engineering_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "installed"
            installer.install(ROOT, target)
            for name in NAMES:
                installed = target / name / "SKILL.md"
                self.assertEqual(installed.resolve(), FAMILY / name / "SKILL.md")
                # Resolve the canonical skill first, as the installation guide instructs.
                for dependency in local_links(installed.resolve()):
                    self.assertTrue(dependency.exists(), str(dependency))

    def test_installer_cli(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "agent-skills"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/install_skills.py"),
                 "--target-dir", str(target)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "new-product-from-scratch/SKILL.md").is_file())
            self.assertTrue((target / "new-web-app-from-scratch/SKILL.md").is_file())

    def test_installer_cli_reports_conflict_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "agent-skills"
            conflict = target / "new-product-from-scratch"
            conflict.mkdir(parents=True)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/install_skills.py"),
                 "--target-dir", str(target)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertTrue(conflict.is_dir())
            self.assertEqual(list(target.iterdir()), [conflict])


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "source"
        self.target = self.base / "target"
        for name in ("first", "second"):
            directory = self.source / "family" / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text("fixture")

    def test_install_and_reinstall(self):
        self.assertEqual(installer.install(self.source, self.target), (2, 0))
        self.assertEqual(installer.install(self.source, self.target), (0, 2))

    def test_existing_directory_is_preserved_before_any_links_created(self):
        (self.target / "second").mkdir(parents=True)
        marker = self.target / "second" / "private.txt"
        marker.write_text("preserve")
        with self.assertRaises(FileExistsError):
            installer.install(self.source, self.target)
        self.assertEqual(marker.read_text(), "preserve")
        self.assertFalse((self.target / "first").exists())

    def test_existing_file_is_preserved(self):
        self.target.mkdir()
        destination = self.target / "first"
        destination.write_text("preserve")
        with self.assertRaises(FileExistsError):
            installer.install(self.source, self.target)
        self.assertEqual(destination.read_text(), "preserve")

    def test_broken_symlink_is_preserved(self):
        self.target.mkdir()
        destination = self.target / "first"
        destination.symlink_to(self.base / "missing")
        with self.assertRaises(FileExistsError):
            installer.install(self.source, self.target)
        self.assertTrue(destination.is_symlink())
        self.assertEqual(destination.readlink(), self.base / "missing")

    def test_other_library_symlink_is_preserved(self):
        self.target.mkdir()
        destination = self.target / "first"
        destination.symlink_to(self.source / "family" / "second", target_is_directory=True)
        with self.assertRaises(FileExistsError):
            installer.install(self.source, self.target)
        self.assertEqual(destination.resolve(), self.source / "family" / "second")

    def test_duplicate_skill_names_fail_without_installing(self):
        duplicate = self.source / "another" / "first"
        duplicate.mkdir(parents=True)
        (duplicate / "SKILL.md").write_text("fixture")
        with self.assertRaises(ValueError):
            installer.install(self.source, self.target)
        self.assertFalse(self.target.exists())

    def test_empty_library_fails(self):
        empty = self.base / "empty"
        empty.mkdir()
        with self.assertRaises(ValueError):
            installer.install(empty, self.target)
        self.assertFalse(self.target.exists())

    def test_install_inside_library_is_rejected(self):
        for target in (self.source, self.source / "installed"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                installer.install(self.source, target)


if __name__ == "__main__":
    unittest.main()
