#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   TYPES - types.py

   Contains enums and types in general
"""


class tcolors:
    """Provides ANSI escape characters for colored terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class hydra_image_engines:
    GIS = 1
    GIPHY = 2
