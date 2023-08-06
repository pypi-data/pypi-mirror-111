from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(name='hnapi',
      version='0.0.0',
      description='HN API Wrapper',
      long_description=readme,
      url='https://github.com/IThinkImOKAY/hnapi',
      author='diogenesjunior',
      author_email='diogenesjunior@protonmail.com',
      packages=['hnapi'],
      keywords='hn hackernews api hacker news',
      install_requires=['requests'])
