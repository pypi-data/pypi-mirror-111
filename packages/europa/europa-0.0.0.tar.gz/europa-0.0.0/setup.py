""" setup.py created according to https://packaging.python.org/tutorials/packaging-projects """

import setuptools #type:ignore

setuptools.setup(
    name="europa",
    version="0.0.0",
    author="hashberg",
    author_email="sg495@users.noreply.github.com",
    description="",
    url="https://github.com/frostbyte-lang/europa",
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[ # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    package_data={"": [],
                  "europa": ["europa/py.typed"],
                 },
    install_requires=[
        "frostbyte-lang",
    ],
    include_package_data=True
)
