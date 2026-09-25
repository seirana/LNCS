from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.validate_style import CSL_NS, validate_style


STYLE_PATH = Path(
    "springer-lecture-notes-in-computer-science-alphabetical.csl"
)


def test_style_is_well_formed_xml():
    tree = ET.parse(STYLE_PATH)
    root = tree.getroot()

    assert root.tag == f"{{{CSL_NS}}}style"


def test_repository_style_passes_semantic_validation():
    result = validate_style(STYLE_PATH)

    assert result.valid, result.errors
    assert result.errors == []


def test_style_is_numeric_and_bibliography_is_alphabetical():
    result = validate_style(STYLE_PATH)

    assert result.metadata["version"] == "1.0"
    assert result.metadata["class"] == "in-text"
    assert result.metadata["title"] == (
        "Springer - Lecture Notes in Computer Science "
        "(sorted alphabetically)"
    )


def test_self_link_matches_style_id():
    result = validate_style(STYLE_PATH)

    assert result.metadata["self_link"] == result.metadata["id"]


def test_style_declares_license_metadata():
    result = validate_style(STYLE_PATH)

    assert result.metadata["rights_license"] == (
        "http://creativecommons.org/licenses/by-sa/3.0/"
    )
