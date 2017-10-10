"""Install setup."""
import setuptools


setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]


setuptools.setup(
    name="patents4j",
    version="0.0.1",

    author="Luca Verginer",
    description="Scripts to transform the Morrison/Riccaboni Patent to a Neo4j DB",

    packages=setuptools.find_packages(include=['src']),
    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
