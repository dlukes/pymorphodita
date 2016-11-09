from setuptools import setup

setup(
    name="pymorphodita",
    version="0.1",
    description="A more newbie-friendly API for MorphoDiTa",
    url="https://github.com/dlukes/pymorphodita",
    author="David Lukeš",
    license="GPLv3",
    packages=["pymorphodita"],
    install_requires=[
        "ufal.morphodita (>=1.9)"
    ],
    zip_safe=True
)
