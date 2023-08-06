from setuptools import setup, find_packages

setup(
   name='mylib-aakriti2.0',
   version='1.1',
   description='A useful module',
   author='Aakriti',
   author_email='aakritiverma385@gmail.com',
   packages=find_packages(),  #same as name
   install_requires=['wheel', 'bar','pandas'], #external packages as dependencies
)