from setuptools import setup, find_packages

setup(
   name='mylib-aakriti',
   version='1.0',
   description='A useful module',
   author='Aakriti',
   author_email='aakritiverma385@gmail.com',
   packages=find_packages(),  #same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)