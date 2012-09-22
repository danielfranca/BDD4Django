#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import morelia

setup(name         = 'BDD4Django',
      version      = bdd4django.__version__,
      description  = 'for "Behavior Driven Development" (BDD) -- ' +
                     'a client-facing scripting language to ' +
                     'put the squeeze on all your features',
      author       = 'Daniel Franca
      author_email = 'daniel.franca@gmail.com',
      url          = 'http://c2.com/cgi/wiki?MoreliaViridis',
      py_modules   = ['bdd4django'],
      keywords     = "test bdd behavior",
      classifiers  = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        "Development Status :: 4 - Beta"
      ]
    )
