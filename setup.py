try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'PostgreSQL backup and restore tools',
	'author': 'BitBacker, Inc.',
	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'My email.',
	'version': '0.1',
	'install_requires': [''],
	'packages': ['bbpgsql'],
	'scripts': ['bbpgsql/cmdline_scripts/archivewal'],
	'name': 'bbpgsql'
}

setup(**config)

