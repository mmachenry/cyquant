./clean.sh
deactivate
./venv/bin/deactivate
python setup.py build_ext --inplace
python setup.py sdist
pip install --upgrade twine
twine upload ./dist/*