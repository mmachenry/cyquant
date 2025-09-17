clean:
  rm -rf build dist .tox *.egg-info

build:
  python setup.py build_ext --inplace
  python setup.py sdist

twine-login:
  aws codeartifact login --tool twine --repository keystonetowersystems --domain keystonetowersystems --domain-owner 563407091361 --region us-east-1

release: clean build
  pip install --upgrade twine
  twine upload --repository codeartifact dist/*
