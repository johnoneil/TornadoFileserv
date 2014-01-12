from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='tornado_fileserv',
    version='0.1',
    description='Put a folder and subfolders on the web with password protection.',
    long_description = readme(),
	classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
      ],
    keywords = 'tornado http web filesystem',
    url='https://github.com/johnoneil/tornado_fileserv',
    author='John O\'Neil',
    author_email='oneil.john@gmail.com',
    license='MIT',
    packages=[
	    'tornado_fileserv'
    ],
    install_requires=[
        'tornado',
        'argparse'
      ],
	package_data = {
		'': ['*.html', '*.css', '*.gif', '*.ico'],
		'tornado_fileserv': ['icons/*.gif', 'icons/*.ico'],
	},
    entry_points = {
		'console_scripts': [
            'tornado-fileserv=tornado_fileserv.fileserver:main',
        ],
    },
    zip_safe=True)
