# -*- coding: utf-8 -*-

from setuptools import (
    find_packages,
    setup,
)

with open('./README.md') as readme:
    long_description = readme.read()

setup(
    name="mervyn",
    author='lmist',
    author_email='louaimisto@gmail.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    scripts=["mervyn"],
    version="2.0.0",
    description="A command line tool for software project management.",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/lmist/mervyn',
    install_requires=[
        "certifi==2021.5.30",
        "chardet==4.0.0",
        "fire==0.4.0",
        "idna==2.10",
        "netifaces==0.11.0",
        "pynpm==0.1.2",
        "randomname==0.1.3",
        "requests==2.25.1",
        "six==1.16.0",
        "termcolor==1.1.0",
        "tqdm==4.61.0",
        "urllib3==1.26.5",
    ],
    python_requires='>=3.6,<4',
    license="MIT",
    zip_safe=False,

)
