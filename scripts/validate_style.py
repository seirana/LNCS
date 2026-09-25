from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


CSL_NS = "http://purl.org/net/xbiblio/csl"
NS = {"csl": CSL_NS}


@dataclass(frozen=True)
class ValidationResult:
    path: str
    valid: bool
    errors: list[str]
    warnings: list[str]
    metadata: dict[str, str | None]


def _text(root: ET.Element, xpath: str) -> str | None:
    element = root.find(xpath, NS)
    if element is None or element.text is None:
        return None
    return element.text.strip()


def validate_style(path: str | Path) -> ValidationResult:
    style_path = Path(path).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        tree = ET.parse(style_path)
    except (ET.ParseError, OSError) as exc:
        return ValidationResult(
            path=str(style_path),
            valid=False,
            errors=[f"Could not parse CSL XML: {exc}"],
            warnings=[],
            metadata={},
        )

    root = tree.getroot()
    expected_root = f"{{{CSL_NS}}}style"
    if root.tag != expected_root:
        errors.append(
            "Root element must be the CSL <style> element in the CSL namespace."
        )

    version = root.attrib.get("version")
    style_class = root.attrib.get("class")
    title = _text(root, "csl:info/csl:title")
    style_id = _text(root, "csl:info/csl:id")
    updated = _text(root, "csl:info/csl:updated")

    self_link = root.find(
        "csl:info/csl:link[@rel='self']",
        NS,
    )
    self_href = (
        self_link.attrib.get("href")
        if self_link is not None
        else None
    )

    rights = root.find("csl:info/csl:rights", NS)
    rights_license = (
        rights.attrib.get("license")
        if rights is not None
        else None
    )

    citation_category = root.find(
        "csl:info/csl:category[@citation-format='numeric']",
        NS,
    )

    if version != "1.0":
        errors.append("CSL version must be 1.0.")
    if style_class != "in-text":
        errors.append("Style class must be 'in-text'.")
    if not title:
        errors.append("Style metadata must include a title.")
    if not style_id:
        errors.append("Style metadata must include an id.")
    if not updated:
        errors.append("Style metadata must include an updated timestamp.")
    if not self_href:
        errors.append("Style metadata must include a rel='self' link.")
    elif style_id and self_href != style_id:
        errors.append("The rel='self' link must match the style id.")
    if citation_category is None:
        errors.append("Style must declare numeric citation formatting.")
    if rights is None:
        errors.append("Style metadata must declare licensing/rights.")
    elif not rights_license:
        warnings.append("Rights metadata exists but does not include a license URL.")

    macro_names: list[str] = []
    for macro in root.findall("csl:macro", NS):
        name = macro.attrib.get("name")
        if not name:
            errors.append("Every macro must have a name.")
            continue
        macro_names.append(name)

    duplicates = sorted(
        name
        for name in set(macro_names)
        if macro_names.count(name) > 1
    )
    if duplicates:
        errors.append(
            "Duplicate macro names: " + ", ".join(duplicates)
        )

    citation = root.find("csl:citation", NS)
    if citation is None:
        errors.append("Style must define a citation block.")
    else:
        citation_number = citation.find(
            ".//csl:text[@variable='citation-number']",
            NS,
        )
        if citation_number is None:
            errors.append(
                "Citation block must render citation-number."
            )

    bibliography = root.find("csl:bibliography", NS)
    if bibliography is None:
        errors.append("Style must define a bibliography block.")
    else:
        sort_keys = bibliography.findall(
            "csl:sort/csl:key",
            NS,
        )
        sort_signature = [
            (
                key.attrib.get("macro"),
                key.attrib.get("variable"),
            )
            for key in sort_keys
        ]

        expected_prefix = [
            ("author", None),
            (None, "title"),
        ]
        if sort_signature[:2] != expected_prefix:
            errors.append(
                "Bibliography must sort first by author macro and then by title."
            )

        bibliography_number = bibliography.find(
            ".//csl:text[@variable='citation-number']",
            NS,
        )
        if bibliography_number is None:
            errors.append(
                "Bibliography must render citation-number."
            )

    metadata = {
        "title": title,
        "id": style_id,
        "version": version,
        "class": style_class,
        "updated": updated,
        "self_link": self_href,
        "rights_license": rights_license,
    }

    return ValidationResult(
        path=str(style_path),
        valid=not errors,
        errors=errors,
        warnings=warnings,
        metadata=metadata,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the repository's LNCS CSL style."
    )
    parser.add_argument(
        "style",
        nargs="?",
        default="springer-lecture-notes-in-computer-science-alphabetical.csl",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable validation output.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = validate_style(args.style)

    if args.json:
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print(f"Style: {result.path}")
        print(f"Valid: {result.valid}")
        if result.errors:
            print("Errors:")
            for error in result.errors:
                print(f"  - {error}")
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"  - {warning}")

    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
