#!/usr/bin/env python3

# from distutils.core import setup
from os import path
from setuptools import setup

from alphabhta import __version__
# from alphabhta.version import __version__
# from alphabhta.version import __license__
# from alphabhta.version import __author__
# from alphabhta.version import __email__

here = path.abspath(path.dirname(__file__))

# ------------------------------------------------------------------------------

# Package name
packageName = "alphabhta"

# Import version info
exec(open(path.join(here, '{}/version.py'.format(packageName))).read())

# Long description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

# ------------------------------------------------------------------------------
# Setup config
setup(
	use_scm_version=True,
	setup_requires=['setuptools_scm'],

	name=packageName,
	packages=[packageName],
	version=__version__,
	license=__license__,
	description='Build utils',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author=__author__,
	author_email=__email__,
	url='https://github.com/tedicreations/alphabhta',
	download_url='https://github.com/TediCreations/alphabhta/archive/' + __version__ + '.tar.gz',
	keywords=['build', 'make', 'util'],
	install_requires=["importlib-metadata"],
	# package_data={'alphabhta': ['conf/make/*']},
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"alphabhta = alphabhta.main:main",
			"ab = alphabhta.main:main",
		]
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
	],
)
