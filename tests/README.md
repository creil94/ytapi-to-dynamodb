# Tests
This folder contains a mix of unit- and integration-tests mainly for the lambda functions and the connectors.
## Usage
1. Add `functions`-folder to python path. On mac run the following command in the root of the project: ```export PYTHONPATH=`pwd`/functions```
2. run the following command from the root of the project to execute all tests `pytest -c tests/pytest.ini` 