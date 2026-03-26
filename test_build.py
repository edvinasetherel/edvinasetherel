import tempfile
import unittest
from pathlib import Path
from build import generate_readme
from build import write_readme
from build import ENCODING
from config import Config
from config import Link
from config import Profile

APPROVED_OUTPUT = """<h3 align="center">Test Title</h3>

<p align="center">
  <samp>
    Line one<br>
    Line two
  </samp>
</p>

<p align="center">
  <a href="https://example.com">Example</a>&emsp;•&emsp;<a href="mailto:test@test.com">Email</a>
</p>
"""

APPROVED_OUTPUT_SINGLE = """<h3 align="center">Solo Title</h3>

<p align="center">
  <samp>
    Only tagline
  </samp>
</p>

<p align="center">
  <a href="https://solo.com">Solo</a>
</p>
"""

APPROVED_OUTPUT_MULTIPLE = """<h3 align="center">Multi Title</h3>

<p align="center">
  <samp>
    First<br>
    Second<br>
    Third<br>
    Fourth
  </samp>
</p>

<p align="center">
  <a href="https://one.com">One</a>&emsp;•&emsp;<a href="https://two.com">Two</a>&emsp;•&emsp;<a href="https://three.com">Three</a>
</p>
"""

TEST_CONFIG = Config(
    profile=Profile(title="Test Title", taglines=["Line one", "Line two"]),
    links=[
        Link(name="Example", url="https://example.com"),
        Link(name="Email", url="mailto:test@test.com")
    ]
)

SINGLE_VALUE_CONFIG = Config(
    profile=Profile(title="Solo Title", taglines=["Only tagline"]),
    links=[Link(name="Solo", url="https://solo.com")]
)

MULTIPLE_VALUES_CONFIG = Config(
    profile=Profile(title="Multi Title", taglines=["First", "Second", "Third", "Fourth"]),
    links=[
        Link(name="One", url="https://one.com"),
        Link(name="Two", url="https://two.com"),
        Link(name="Three", url="https://three.com")
    ]
)


class TestGenerateReadme(unittest.TestCase):
    def test_matches_approved_output(self):
        result = generate_readme(TEST_CONFIG.model_dump())
        self.assertEqual(result, APPROVED_OUTPUT)

    def test_single_tagline_and_link(self):
        result = generate_readme(SINGLE_VALUE_CONFIG.model_dump())
        self.assertEqual(result, APPROVED_OUTPUT_SINGLE)

    def test_multiple_taglines_and_links(self):
        result = generate_readme(MULTIPLE_VALUES_CONFIG.model_dump())
        self.assertEqual(result, APPROVED_OUTPUT_MULTIPLE)


class TestWriteReadme(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            write_readme("test content", path)
            output_file = path.joinpath("README.md")
            self.assertTrue(output_file.exists())
            self.assertEqual(output_file.read_text(encoding=ENCODING), "test content")

    def test_creates_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            write_readme("", path)
            output_file = path.joinpath("README.md")
            self.assertTrue(output_file.exists())
            self.assertEqual(output_file.read_text(encoding=ENCODING), "")

    def test_raises_on_invalid_path(self):
        with self.assertRaises(ValueError):
            write_readme("content", Path("/nonexistent/path"))

    def test_raises_on_file_path(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            with self.assertRaises(ValueError):
                write_readme("content", Path(tmpfile.name))


if __name__ == "__main__":
    unittest.main()
