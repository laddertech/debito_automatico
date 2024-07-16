# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='debito_automatico',
    version='0.02',
    author='Ladder Tecnologia',
    author_email='ladder@ladder.dev.br',
    url='https://github.com/laddertech/debito_automatico',
    packages=find_packages(),
    package_data={
        'debito_automatico': ['layout/*/*/*.json']
    },
    zip_safe=False,
    install_requires=[],
    provides=[
        'debito_automatico'
    ],
    license='MIT',
    description='Classe para gerar arquivo de débito automático',
    download_url='https://github.com/laddertech/debito_automatico',
    scripts=[],
    classifiers=[],
    platforms='any',
    test_suite='',
    tests_require=[],
)
