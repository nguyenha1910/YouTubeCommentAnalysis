#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    author="Nguyen Ha",
    author_email='nguyenhbhcm@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    name='YouTubeCommentAnalysis',
    description="YouTube Comment Analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nguyenha1910/YouTubeCommentAnalysis",
    packages=setuptools.find_packages(exclude=('test*','testing*')),
    include_package_data=True,
    package_data={'YouTubeCommentAnalysis': ['*.csv']},
    license="MIT license",
    version='0.0.1',
    zip_safe=False,
    install_requires=['beautifulsoup4', 'nltk', 'emoji', 'gensim', 'pandas',
                      'os','importlib_resources','collections','ast','pandas',
                      're', 'pickle5'],
    python_requires='>=3.6',
)