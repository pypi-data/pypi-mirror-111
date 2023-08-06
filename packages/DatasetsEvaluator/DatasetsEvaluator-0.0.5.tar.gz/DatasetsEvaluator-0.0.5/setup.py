from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
	name='DatasetsEvaluator',
	version='0.0.5',
	author='Brett Kennedy',
	author_email='wm.brett.kennedy@gmail.com',
	packages=find_packages(),
	install_requires=[
          'numpy',
	  'pandas',
	  'openml'
	],
	description = 'A tool to automate collecting and testing against datasets on openml.org',
	long_description = long_description, 
	long_description_content_type = 'text/markdown',
        classifiers=[
        	'Development Status :: 3 - Alpha',
	        'License :: OSI Approved :: MIT License',
        	'Programming Language :: Python :: 3'
	      ],
	keywords='machine learning classification regression evaulation public datasets'

)
