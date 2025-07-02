# MultiversX multi-version node scripts

These scripts allow one to use multiple versions of the MultiversX node, in sequence, to _sync_ (from the deep past) or run _import-db_ flows.

**Important:** these scripts are only suitable for observers, not for validators. Furthermore, the MultiversX proxy isn't handled.

## Python virtual environment

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt --upgrade
```

## Building the artifacts

Skip this flow if you choose to download the pre-built Node artifacts, instead of building them.

```
PYTHONPATH=. python3 ./multistage/build.py --workspace=~/mvx-workspace --config=./multistage/build.json
```

## Set up an observer (or a squad)

```
PYTHONPATH=. python3 ./multistage/driver.py --config=./multistage/driver.testnet.json
```
