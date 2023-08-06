from setuptools import setup, find_packages
import subprocess

VERSION = '0.0.2'
DESCRIPTION = 'Extract metadata from url'
LONG_DESCRIPTION = 'A package that allows you to extract metadata from static webpages.'

subprocess.Popen("make", cwd="metadata_from_url")

setup(
    name="metadata_from_url",
    version=VERSION,
    author="hectortav (Ektoras Tavoularis)",
    author_email="<tavhector@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'metadata', 'extract'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)

# python3 setup.py sdist bdist_wheel
# twine upload dist/*