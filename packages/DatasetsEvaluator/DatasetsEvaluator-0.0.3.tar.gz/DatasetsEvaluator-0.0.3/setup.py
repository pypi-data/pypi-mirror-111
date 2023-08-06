from setuptools import setup, find_packages

setup(
	name='DatasetsEvaluator',
	version='0.0.3',
	author='Brett Kennedy',
	author_email='wm.brett.kennedy@gmail.com',
	packages=find_packages(),
	install_requires=[
          'numpy',
	  'pandas',
	  'openml'
	],
)
