from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name = "mytask",
    version = "0.1.2",
    description = "mytask manager tool",
    long_description = readme,
    long_description_content_type='text/markdown',
    url = "https://github.com/kasul092/todo",
    author  = "Sumit Pujari",
    author_email = "sumitpujari199723@gmail.com",
    packages = find_packages(include=["mytask"]),
    python_requires ='>=3.6',
    install_requires = ['click', 'tabulate'],
    entry_points = {
        "console_scripts":[
            "mytask=mytask:main",
        ],
    },
)
