#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   HYDRABOT - "STAY HYDRATED" MESSENGER

   A program to randomly generate and send Facebook messenges
   which remind people to stay hydrated

   (c) 2020 by Alexander Roidl (alexanderroidl@gmail.com)
"""


# Dependencies
import atexit
import colorama
# Local dependencies
from hydrabot_py import config
from hydrabot_py.lib import HydraBot


# Global variables
hydrabot = None


# Called on programs shutdown
def clean_up():
    """Clean up after execution"""
    print('Cleaning up...')

    if hydrabot is not None:
        hydrabot.clean_up()


# Main method
def main():
    colorama.init(autoreset=True)

    # Create HydraBot instance based of configuration
    global hydrabot
    hydrabot = HydraBot(**config)

    # Register exit handler
    atexit.register(clean_up)


# Call main method by default
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Call exit function on keyboard interupt as well
        clean_up()
