from setuptools import setup

setup(
	name = 'maskutils',
	version = '0.0.2',
	description = 'Functionality for working with 2D image masks',
	url = 'https://github.com/adamrehn/maskutils',
	author = 'Adam Rehn',
	author_email = 'adam@adamrehn.com',
	license = 'MIT',
	packages = ['maskutils'],
	zip_safe = True,
	install_requires = [
		'opencv-python',
		'numpy',
		'slidingwindow'
	]
)
