from setuptools import setup, find_packages
 
classifiers = [
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basic-calculator-101',
  version='1.0.1',
  description='Calculator with basic functions: Add, Subtract, Multiply, Divide, Nth-root, ability to reset to 0',
  url='https://github.com/Ifyokoh/calculator',  
  author='Ifeoma Okoh',
  author_email='odibest1893@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages()
)