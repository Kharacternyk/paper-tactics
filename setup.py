from setuptools import find_packages
from setuptools import setup

setup(
    name="paper-tactics",
    url="https://github.com/Kharacternyk/paper-tactics",
    version="0.0.0",
    license="AGPLv3+",
    author="Nazar Vinnichuk",
    packages=find_packages(),
    package_data={"paper-tactics": ["templates/*", "static/*"]},
    install_requires=["flask"],
    extras_require={
        "tests": ["pytest", "hypothesis"],
    },
)
