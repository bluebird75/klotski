mypy --strict src
del /s /q build
copy README.md src
python setup.py sdist bdist_wheel