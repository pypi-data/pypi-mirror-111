from setuptools import setup

setup(
	name='RollingGroupCorrelation',
	version='v0.3',
	description='This is a library that calculates the rolling group correlation for a set of time series.',
	url='https://github.com/johantilli/RollingGroupCorrelation',
	download_url='https://github.com/johantilli/RollingGroupCorrelation/archive/refs/tags/v0.3.tar.gz',
	author='Johan Tilli',
	author_email='johan.tilli@gmail.com',
	license='OSI Approved :: GNU General Public License v3 (GPLv3)',
	packages=['RollingGroupCorrelation'],
	zip_safe=False,
	long_description='This is a library that calculates the rolling group correlation for a set of time series. I got the idea for this kind of statistical measurement a couple of months ago but could not find anything similar in academic papers or forums (please let me know if this or something similar already exists). This tool has really added value for me when modeling portfolio risk. It has also increased the accuracy of some of my ML models when used for feature engineering.',
	long_description_content_type="text/markdown",
	keywords = ['correlation', 'multi', 'rolling', 'group', 'mean'],
	install_requires=[ 
	          'pandas',
	          'numpy',
	      ],
	classifiers=[
	    'Development Status :: 3 - Alpha',    
	    'Intended Audience :: Developers',  
	    'Topic :: Software Development :: Build Tools',
	    'Programming Language :: Python :: 3',    
  ],

)