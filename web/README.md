# web/

Frontend of EU-Flex Explorer.

Planned stack: Vite + React + TypeScript, MapLibre GL (bidding-zone map), ECharts (time series, duration curves, stacked contributions), DuckDB-WASM (queries Parquet in the browser).

## MVP screens

1. **Overview map**: seasonal / weekly / daily flexibility need by bidding zone
2. **Zone detail**: residual load, flexibility needs over the year, ramping
3. **Contributions**: technology and cross-border contributions (stacked)
4. **Short-term needs**: forecast-error-driven needs and shortfalls
5. **Compare**: two runs side by side (e.g. `teaser-ds-cross-border` vs `teaser-ds-no-cross-border`)
6. **About**: what each indicator means, links to the modelling specification, disclaimer

## Accessibility checklist (per chart)

- [ ] Text summary of the key takeaway
- [ ] "Show as table" toggle
- [ ] Keyboard-reachable controls with visible focus
- [ ] Colour palette passes WCAG AA; never colour-only encoding
- [ ] "Illustrative teaser data" notice visible

TODO: scaffold with `npm create vite@latest . -- --template react-ts`.
