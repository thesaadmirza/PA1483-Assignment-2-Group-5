# Flask performance

This folder is for section 4 of the report.

- `scripts/`: the test app and benchmark scripts
- `config/`: dependencies and test settings
- `data/`: results saved when we run the tests

Run from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r qa3/config/requirements.txt
flask --app qa3/scripts/app run
```

Open http://127.0.0.1:5000/ to see a list of 20 numbers.
