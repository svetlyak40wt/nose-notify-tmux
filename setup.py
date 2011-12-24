# -*- coding: utf-8 -*-
"""
nose-notify-tmux
~~~~~~~~~~~

A nose plugin to display testsuite progress in the notify osd.


:copyright: 2010, Pascal Hartig <phartig@rdrei.net>
:license: BSD, see LICENSE for more details
"""

from setuptools import setup
from nosenotifytmux import __version__


setup(
    name="nose-notify-tmux",
    version=__version__,
    author="Alexander Artemenko",
    author_email="svetlyak.40wt@gmail.com",
    description="A nose plugin to display testsuite progress in TMUX",
    url="http://github.com/svetluyak40wt/nose-notify-tmux",
    packages=['nosenotifytmux'],
    long_description=__doc__,
    requires=['nose (>=0.10)'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        'nose.plugins': [
            'tmux = nosenotifytmux.plugin:NotifyPlugin'
        ]
    }
)
