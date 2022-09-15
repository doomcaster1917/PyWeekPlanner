from setuptools import setup, find_packages

long_description = open('README.md').read()

DESCRIPTION = 'Draws images those shows hours-plan for each week'
LONG_DESC = long_description

setup(
    name='PyWeekPlanner',
    version='1.0',
    author='doomcaster1917',
    author_email='webtalestoday@gmail.com',
    url='https://github.com/doomcaster1917/PyWeekPlanner',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    long_description=LONG_DESC,
    
    },
    install_requires=[
        'pillow',
	'textwrap3'
    ]
)
