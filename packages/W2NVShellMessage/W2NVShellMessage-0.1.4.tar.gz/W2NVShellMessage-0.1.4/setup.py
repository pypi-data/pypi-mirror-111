import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

# README = (HERE / "README.md").read_text()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='W2NVShellMessage',
    version='0.1.4',
    description='A package to display quotes from "Welcome to Night Vale" whenever a new terminal window is launched',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rijumone/W2NVShellMessage',
    project_urls={
        "Bug Tracker": "https://github.com/rijumone/W2NVShellMessage/issues",
    },
    author='Rijumone Choudhuri',
    author_email='mailmeonriju@gmail.com',
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=[
        'pytest',
        'requests',
        'loguru',
        'bs4',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'w2nv=w2nvshellmsg.main:show_msg',
            'w2nv-init=w2nvshellmsg.main:init',
        ],
    },
    python_requires=">=3.6",
)
