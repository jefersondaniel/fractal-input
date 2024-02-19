import xml.etree.ElementTree as ET
from os import system, unlink
from os.path import dirname, join
from phulpy import task


@task
def test(phulpy):
    phulpy.start(['lint', 'unit_test'])


@task
def lint(phulpy):
    result = system('flake8 fractal_input')
    if result:
        raise Exception('lint test failed')


@task
def unit_test(phulpy):
    result = system(
        'pytest --cov-report term-missing'
        + ' --cov-report xml --cov=fractal_input test'
    )
    if result:
        raise Exception('Unit tests failed')
    coverage_path = join(dirname(__file__), 'coverage.xml')
    xml = ET.parse(coverage_path).getroot()
    unlink(coverage_path)
