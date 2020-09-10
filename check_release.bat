:: mypy --strict src
del /s /q build dist
copy README.md src
python setup.py sdist bdist_wheel
twine check dist\*
del /q src\README.md