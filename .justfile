clean:
  rm -rf build dist .tox *.egg-info

release: clean
  python setup.py build_ext --inplace
  python setup.py sdist
  pip install --upgrade twine
  twine upload ./dist/*
