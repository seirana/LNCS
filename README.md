# LNCS Citation Style

This repository contains a Citation Style Language (CSL) file for **Springer Lecture Notes in Computer Science (LNCS)** with an alphabetically sorted bibliography.

The repository is intentionally small: the main artifact is the CSL style itself. The quality upgrade adds validation, provenance documentation, tests, and continuous integration around that artifact without rewriting the original citation rules.

## Main style file

```text
springer-lecture-notes-in-computer-science-alphabetical.csl
```

The embedded style metadata identifies it as:

- title: **Springer - Lecture Notes in Computer Science (sorted alphabetically)**
- CSL version: **1.0**
- citation format: **numeric**
- bibliography order: **author, then title**
- original style author: **Ammar Memari**
- contributors recorded in the CSL metadata: **Mikko Ronkko** and **Naeem Esfahani**
- license declared by the style: **Creative Commons Attribution-ShareAlike 3.0**

See [ATTRIBUTION.md](ATTRIBUTION.md) for provenance and licensing notes.

## What the style does

In-text citations use numeric citation numbers, for example:

```text
[1]
[2, 3]
```

The bibliography remains numbered but is sorted alphabetically by the author macro and then by title.

That distinction is important:

```text
citation rendering  -> numeric
bibliography order  -> alphabetical by author/title
```

The validator in this repository checks that those structural properties remain true after edits.

## Install in Zotero

1. Download the `.csl` file.
2. Open Zotero.
3. Open **Settings/Preferences → Cite → Styles**.
4. Use the **+** button to install the local CSL file.
5. Select the installed LNCS style when formatting a bibliography.

Exact menu wording can vary slightly between Zotero versions.

## Use with Pandoc

```bash
pandoc manuscript.md \
  --citeproc \
  --bibliography=references.bib \
  --csl=springer-lecture-notes-in-computer-science-alphabetical.csl \
  -o manuscript.docx
```

## Use with Quarto

In document YAML:

```yaml
bibliography: references.bib
csl: springer-lecture-notes-in-computer-science-alphabetical.csl
```

## Validation

The repository includes a lightweight semantic validator based only on Python's standard library.

Run:

```bash
python scripts/validate_style.py
```

For machine-readable output:

```bash
python scripts/validate_style.py --json
```

The validator checks, among other things:

- well-formed CSL XML;
- CSL 1.0 root metadata;
- style ID and matching self-link;
- numeric citation declaration;
- presence of citation numbers in citations and bibliography;
- bibliography sorting first by author and then title;
- duplicate macro names;
- licensing metadata.

This is a repository-specific structural validator. It is not a replacement for testing the style in the citation processor used by a final manuscript workflow.

## Automated tests

Install development tools:

```bash
python -m pip install pytest ruff
```

Then run:

```bash
python -m pytest
python -m ruff check scripts tests
```

GitHub Actions runs these checks on Python 3.10, 3.11, and 3.12.

## Repository structure

```text
.
├── springer-lecture-notes-in-computer-science-alphabetical.csl
├── scripts/
│   └── validate_style.py
├── tests/
│   └── test_style.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── ATTRIBUTION.md
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md
```

## Editing the style safely

The CSL file is the primary artifact. Changes should be small, reviewable, and accompanied by tests when they alter structure.

Before committing a style change:

```bash
python scripts/validate_style.py
python -m pytest
```

If a change modifies citation or bibliography behavior, also test it in the citation processor used for the target manuscript workflow.

## Scope

This repository does not claim to be the official Springer distribution point for LNCS styles. It contains the CSL file identified by its own embedded metadata and adds repository-level quality controls around it.

No authorship or ownership of the original CSL style is inferred from repository ownership.
