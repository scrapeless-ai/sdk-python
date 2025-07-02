from setuptools import setup, find_packages

setup(
    name='scrapeless-sdk',
    version='0.1.0',
    description='A Python SDK for Scrapeless, migrated from Node.js version.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    python_requires='>=3.8',
) 