# Contributing

The CSL file is a formatting specification used by citation processors, so apparently small XML changes can alter manuscript output.

## Before changing the style

Run:

```bash
python scripts/validate_style.py
python -m pytest
```

## Change principles

1. Keep style changes narrowly scoped.
2. Preserve the original attribution and rights metadata.
3. Do not change the style ID casually; citation managers use it as an identifier.
4. If behavior changes, update the CSL `<updated>` timestamp.
5. Add or update tests for structural invariants affected by the change.
6. Test rendering in the citation processor used by the target manuscript workflow.

## Repository-specific invariants

The current repository intentionally checks that:

- the style is CSL 1.0;
- citations are numeric;
- bibliography entries include numeric labels;
- bibliography sorting starts with author and then title;
- the self-link matches the style ID;
- macro names are unique;
- rights metadata remains present.

If one of these properties is intentionally changed, the tests and documentation should be changed in the same pull request, with the reason explained.
