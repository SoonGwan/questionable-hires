# Repository working agreements

- Make small, focused commits as work progresses, as requested by the owner.
- For banners, comparison charts, and other project visuals, use Montage semantic colors. Follow the palette and visual guidance in [assets/README.md](assets/README.md); do not introduce an unrelated palette unless the owner requests it.
- Treat `benchmarks/featured.json` as the single pointer to the landing-page benchmark. Whenever featured benchmark data, charts, paths, or claims change, run `python3 -B scripts/sync_featured_benchmark.py`, review both `README.md` and `README.ko.md`, then run the same command with `--check`. Never update one language or a plotted number independently.
