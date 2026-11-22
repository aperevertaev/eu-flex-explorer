# Contributing to EU-Flex Explorer

Thanks for your interest! This project aims to make EU-Flex results accessible to everyone, and contributions from both developers and energy-domain experts are welcome.

## Where does my feedback belong?

| Topic | Where |
|---|---|
| Bug or idea for **this explorer** (UI, charts, export, docs) | [Issues in this repo](../../issues) |
| Wrong or unclear **interpretation of an indicator** in the explorer | Issue here with the `domain` label |
| Bug, methodology or data question about the **EU-Flex model itself** | [EU-Flex repository](https://github.com/EU-ACER/eu-flex-model/issues) |
| Formal feedback on the model during the consultation | [ACER public consultation](https://ec.europa.eu/eusurvey/runner/PC_2026_E_10) |

## Ways to contribute

- **Report a bug** using the bug template.
- **Check indicator interpretation.** If you know power systems, reviewing how we explain and plot flexibility indicators is extremely valuable, and needs no code.
- **Improve accessibility.** Keyboard navigation, screen-reader descriptions, colour contrast.
- **Code.** Look for issues labelled `good first issue` or `help wanted`.

## Before you open a pull request

1. For anything larger than a small fix, **open an issue first** so we can agree on the approach.
2. Fork the repo and create a branch: `git checkout -b feat/short-description`.
3. Keep PRs focused, with one change per PR.
4. Add or update tests and docs.
5. Make sure checks pass locally:

```bash
# Python (adapter, etl, api)
pip install -e "./adapter[dev]"
ruff check . && ruff format --check .
pytest

# Frontend
cd web && npm run lint && npm test
```

## Design rules

- **EU-Flex internals stay in `adapter/`.** No other module may read NetCDF files or rely on EU-Flex variable names directly. They consume the tidy Parquet schema documented in `docs/data-schema.md`.
- **Record provenance.** Every exported run stores the EU-Flex commit, config file and export timestamp.
- **Accessibility is a requirement.** New charts need a text summary and a table alternative.
- **Never present teaser results as real-world conclusions.** UI text must keep the "illustrative data" notice visible.

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Code of conduct

Be respectful and constructive. Harassment or personal attacks are not tolerated. <!-- TODO: adopt Contributor Covenant once the community grows: https://opensource.guide/code-of-conduct/ -->

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
