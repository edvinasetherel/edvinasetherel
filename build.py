import yaml
from pathlib import Path

from config import Config

CONFIG_FILE = "config.yaml"
OUTPUT_FILE = "README.md"
ENCODING = "utf-8"
LINK_SEPARATOR = "&emsp;•&emsp;"
TAGLINE_SEPARATOR = "<br>\n    "

TEMPLATE = """<h3 align="center">{title}</h3>

<p align="center">
  <samp>
    {tagline}
  </samp>
</p>

<p align="center">
  {links}
</p>
"""

LINK_TEMPLATE = """<a href="{url}">{name}</a>"""


def generate_readme(config):
    config = Config(**config)

    tagline_html = TAGLINE_SEPARATOR.join(config.profile.taglines)

    link_parts = [
        LINK_TEMPLATE.format(url=link.url, name=link.name)
        for link in config.links
    ]
    links_html = LINK_SEPARATOR.join(link_parts)

    return TEMPLATE.format(
        title=config.profile.title,
        tagline=tagline_html,
        links=links_html
    )


def write_readme(content: str, path: Path):
    if not path.is_dir():
        raise ValueError(f"Path {path} is not a directory")
    file = path.joinpath(OUTPUT_FILE)
    Path(file).write_text(content, encoding=ENCODING)
    print("README.md generated")


def build_readme():
    config = yaml.safe_load(Path(CONFIG_FILE).read_text(encoding=ENCODING))
    content = generate_readme(config)
    write_readme(content, Path("."))


if __name__ == "__main__":
    build_readme()
