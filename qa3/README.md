# Flask performance

This folder is for section 4 of the report.

- `scripts/`: the test app and benchmark scripts
- `config/`: dependencies and test settings
- `data/`: results saved when we run the tests

Run from the main assignment folder containing `justfile`:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r qa3/config/requirements.txt
flask --app qa3/scripts/app run
```

Open http://127.0.0.1:5000/ to see a list of 20 numbers.

## Benchmark

Install Docker with Compose, just and Python 3. Run these commands from the main assignment folder containing `justfile`.

```sh
just build
just start on
just bench
just start off
just bench
just stop
```

For the full comparison, repeat `just start` and `just bench` in this order: on, off, off, on, on, off. Each benchmark includes a 15-second warm-up and a 60-second measurement.

Results are saved in `qa3/data/`. To summarise new runs, update the six run names in `qa3/data/environment.txt`, then run `just summary`.
