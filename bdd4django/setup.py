#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import bdd4django 

setup(name         = 'BDD4Django',
      version      = bdd4django.__version__,
      description  = '"Behavior Driven Development" (BDD) -- ' +
                     'Integrating Morelia + Splinter + Django',
      author       = u'Daniel França',
      url          = 'http://github.com/danielfranca/BDD4Django',
      author_email = 'daniel.franca@gmail.com',
      py_modules   = ['bdd4django'],
      keywords     = "test bdd behavior django splinter morelia",
      classifiers  = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        "Development Status :: 4 - Beta"
      ]
    )
