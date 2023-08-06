from setuptools import setup

setup(
	name='RollingGroupCorrelation',
	version='v0.2',
	description='A function that calculates the rolling window mean multi correlation between all columns of a Pandas DataFrame.',
	url='https://github.com/johantilli/RollingGroupCorrelation',
	download_url='https://github.com/johantilli/RollingGroupCorrelation/archive/refs/tags/v0.2.tar.gz',
	author='Johan Tilli',
	author_email='johan.tilli@gmail.com',
	license='OSI Approved :: GNU General Public License v3 (GPLv3)',
	packages=['RollingGroupCorrelation'],
	zip_safe=False,
	long_description='A function that calculates the rolling group correlation between all columns of a Pandas DataFrame.',
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