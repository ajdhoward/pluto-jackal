from setuptools import setup, find_packages

setup(
    name="pluto-jackal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "pluto-jackal = scripts.pluto_jackal_main:cli"
        ]
    },
)
