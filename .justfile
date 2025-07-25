clean:
  rm -rf build dist .tox *.egg-info

build:
  python setup.py build_ext --inplace
  python setup.py sdist

release: clean build
  pip install --upgrade twine
  twine upload ./dist/*
