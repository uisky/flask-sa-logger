from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flask_sa_logger',
    version='0.0.1',

    description='Flask+SQLAlchemy logger & request counter',
    long_description=long_description,
    url='https://github.com/uisky/flask-sa-logger',
    author='Dmitry Romakhin',
    author_email='romakhin@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    keywords='flask sqlalchemy logger',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    py_modules=["flask_sa_logger"],
    install_requires=['flask', 'sqlalchemy', 'sqlparse', 'ansicolors']
)
