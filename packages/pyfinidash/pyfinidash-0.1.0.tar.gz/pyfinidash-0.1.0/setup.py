import pathlib
from setuptools import setup, find_packages

CURRENT_DIR = pathlib.Path(__file__).parent
README_CONTENT = (CURRENT_DIR / "README.md").read_text()

setup(
    name='pyfinidash',
    version='0.1.0',
    packages=["pyfinidash"],
    author="Chris Stead",
    author_email="cmstead@gmail.com",
    url="https://github.com/cmstead/pyfinidash#readme",
    platforms=['any'],
    description="A simple-to-use wrapper over the AWS Infinidash API",
    license='MIT',
    long_description=README_CONTENT,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        "console_scripts": [
            "pyfinidash = pyfinidash.__main__:main"
        ]
    }
)