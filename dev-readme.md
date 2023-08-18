Developer hints
---------------

Pre

``` shell
python3 -m pip install --upgrade pip flake8 pylint
```

To set up virtual environment

``` shell
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

To run it from there

``` shell
pipenv run ./dymka -V
```

To publish the new version to pypi

``` shell
python3 -m pip install --upgrade setuptools wheel twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
Taken from https://packaging.python.org/tutorials/packaging-projects/.
