from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in attendease/__init__.py
from attendease import __version__ as version

setup(
	name="attendease",
	version=version,
	description="attendease",
	author="erevive",
	author_email="laxmantandon@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
