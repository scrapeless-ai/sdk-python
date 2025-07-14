import os
from setuptools import setup, find_packages

VERSION = "1.1.0"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="scrapeless",
    version=VERSION,
    author="scrapelessteam",
    author_email="scrapelessteam@gmail.com",
    description="scrapeless python sdk",
    license="MIT",
    keywords=[
        "scrapeless",
        "browserless",
        "scraping browser",
        "scraping",
        "web unlocker",
        "captcha solver",
        "rotate proxy"
    ],
    url="https://github.com/scrapeless-ai/sdk-python",
    project_urls={
        "Documentation": "https://github.com/scrapeless-ai/sdk-python#readme",
        "Source": "https://github.com/scrapeless-ai/sdk-python",
    },
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    python_requires='>=3.8',
)
