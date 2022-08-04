# -*- coding: utf-8 -*-

"""
Installation script
"""

from __future__ import absolute_import

from pkg_resources import DistributionNotFound, get_distribution
from setuptools import setup, find_packages


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None




setup(
    name="roar-stats",
    description=(
        "Scrapes info on current utilization of SAGEMAPP nodes"
    ),
    author="Garrett Wendel",
    author_email="gmw5164@psu.edu",
    url="tbd",
    license="Apache 2.0",
    version="0.01",
    python_requires=">=3.6",
    packages=find_packages(),
    zip_safe=False,
    entry_points={
    'console_scripts': [
        'sagemapp_stats=stats:main'],
},
)
