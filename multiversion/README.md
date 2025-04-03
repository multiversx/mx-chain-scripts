# MultiversX multi-version node scripts

These scripts allow one to use multiple versions of the MultiversX node, in sequence, to _sync_ (from the deep past) or run _import-db_ flows.

**Important:** these scripts are only suitable for observers, not for validators. Furthermore, the MultiversX proxy isn't handled.

## Building the binaries

Go must be installed beforehand.

```
PYTHONPATH=. python3 ./multiversion/build.py --workspace=~/mvx-workspace --config=./multiversion/build.json
```

## Maintenance

### Python virtual environment

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt --upgrade
```
