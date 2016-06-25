from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("VERSION") as f:
    version = f.read()

with open("requirements.txt") as f:
    install_requires = list(
        line for line in f.read().split("\n")

        # Exclude comments
        if not line.startswith("#")
    )


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]


setup(
    name="pyblish",
    version=version,
    description="Plug-in driven automation framework for content",
    long_description="Collection of latest supported "
                     "combinations of Pyblish projects",
    author="Abstract Factory and Contributors",
    author_email="marcus@abstractfactory.com",
    url="https://github.com/pyblish/pyblish",
    license="LGPL",
    packages=find_packages(),
    zip_safe=False,
    classifiers=classifiers,
    entry_points={
        "console_scripts": ["pyblish = pyblish.cli:main"]
    },
    install_requires=install_requires,
)
