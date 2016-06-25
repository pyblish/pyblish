from setuptools import setup, find_packages


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
    version="1.4.2",
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
    install_requires=[
        "pyblish-base==1.4.1",
        # "pyblish-hiero==1.0.0",  # Awaiting upload to PyPI
        # "pyblish-houdini==0.2.2",
        "pyblish-maya==2.0.0",
        # "pyblish-nuke==1.1.2",
        "pyblish-modo==0.0.2",
        "pyblish-lite==0.3.3",
        "pyblish-qml==0.7.0",
        # pyblish-standalone==0.1.0,
    ],
)
