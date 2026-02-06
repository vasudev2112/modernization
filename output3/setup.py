"""Setup configuration for discount_calculator package.

This setup file allows the discount_calculator module to be installed
as a Python package using pip.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discount-calculator',
    version='1.0.0',
    description='A Python module for calculating discounts based on customer type and purchase amount',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Automated Java to Python Migration Agent',
    author_email='migration@example.com',
    url='https://github.com/vasudev2112/modernization',
    
    # Package configuration
    py_modules=['discount_calculator'],
    python_requires='>=3.7',
    
    # Dependencies
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    
    # Development dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'black>=23.0.0',
            'pylint>=2.16.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.2.0',
        ],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Typing :: Typed',
    ],
    
    # Keywords
    keywords='discount calculator pricing ecommerce business-logic',
    
    # Project URLs
    project_urls={
        'Source': 'https://github.com/vasudev2112/modernization',
        'Bug Reports': 'https://github.com/vasudev2112/modernization/issues',
        'Documentation': 'https://github.com/vasudev2112/modernization/blob/main/output3/README.md',
    },
)
