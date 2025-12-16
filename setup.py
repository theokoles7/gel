"""# gel.setup

GEL setup utility.
"""

from pathlib    import Path
from setuptools import find_packages, setup
from typing     import Any, Dict

# HELPERS ==========================================================================================

def get_long_description() -> str:
    """# Get Long Description.

    ## Returns:
        * str:  README file contents.
    """
    with open(Path(__file__).parent / "README.md", encoding = "utf-8") as f: return f.read()


def get_version() -> str:
    """# Get Package Version.

    ## Returns:
        * str:  Current package version.
    """
    # Initialize dictionary to store metadata.
    metadata:   Dict[str, Any] =    {}

    # Open metadata file.
    with open(Path(__file__).parent / "gel" / "__meta__.py") as f:

        # Read variables.
        exec(f.read(), metadata)

    # Provide version.
    return metadata["__version__"]


# SETUP UTILITY ====================================================================================

setup(
    name =                          "curatio",
    version =                       get_version(),
    author =                        "Gabriel C. Trahan",
    author_email =                  "gabrieltrahan777@hotmail.com",
    description =                   """Gabriel's Everything Library.""",
    long_description =               get_long_description(),
    long_description_content_type = "text/markdown",
    license =                       "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007",
    license_files =                 ("LICENSE"),
    url =                           "https://github.com/theokoles7/gel",
    packages =                      find_packages(),
    python_requires =               ">=3.10",
    install_requires =              [
                                        "pytest",
                                    ],
    entry_points =                  {
                                        "console_scripts":  [
                                                                "gel=gel.__main__:gel_entry_point"
                                                            ],
                                    },
    classifiers =                   [
                                        "Intended Audience :: Developers",
                                        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                                        "Operating System :: OS Independent",
                                        "Programming Language :: Python :: 3",
                                        "Programming Language :: Python :: 3.10",
                                        "Programming Language :: Python :: 3.11",
                                        "Programming Language :: Python :: 3.12",
                                        "Topic :: Scientific/Engineering :: Artificial Intelligence",
                                    ]
)