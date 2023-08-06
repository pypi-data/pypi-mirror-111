"""
    setup.py created according to https://packaging.python.org/tutorials/packaging-projects
    scripts added according to https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
"""

import setuptools #type:ignore

setuptools.setup(
    name="frostbyte-lang",
    version="0.0.0",
    author="hashberg",
    author_email="sg495@users.noreply.github.com",
    description=" Reference implementation for the Frostbyte programming language and smart contract protocol.",
    url="https://github.com/frostbyte-lang/frostbyte-lang",
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[ # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    package_data={"": [],
                  "frostbyte-lang": ["frostbyte/py.typed"],
                 },
    install_requires=[
        "cbor2",
        "py-cid"
    ],
    entry_points = {
        'console_scripts': [
            'frostbyte-run=frostbyte.node:run',
            'frostbyte-setup=frostbyte.node:setup',
            'frostbyte-config=frostbyte.node:config',
        ],
    },
    include_package_data=True
)
