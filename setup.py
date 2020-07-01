from pathlib import Path
import re

from setuptools import setup  # type: ignore  # no typehints

root = Path(__file__).parent

init = (root / "gdplatformer.py").read_text("utf-8")

result = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', init, re.MULTILINE
)

if result is None:
    raise RuntimeError("Failed to find version.")

version = result.group(1)

readme = (root / "README.rst").read_text("utf-8")


setup(
    name="gd.platformer",
    author="NeKitDS, Sapfirenko",
    author_email="gdpy13@gmail.com",
    url="https://github.com/NeKitDS/gd.platformer",
    project_urls={
        "Issue tracker": "https://github.com/NeKitDS/gd.platformer/issues"
    },
    version=version,
    py_modules=["gdplatformer"],
    license="MIT",
    description="Geometry Dash Platformer Mod",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={"console_scripts": ["gd.platformer = gdplatformer:main"]},
)
