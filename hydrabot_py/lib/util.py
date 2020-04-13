#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   UTILITIES - util.py

   This file provides useful methods that don't relate
   to any specific class
"""


class Util:
    """Provides different utility methods"""

    @staticmethod
    def get_num_range(range_string, fill=False):
        """Creates a integer list of a number range represented by
        a string and optionally fill it up with numbers

        Args:
          range_string (str): String representing number range
          fill (bool): Fill up middle values? (False)

        Returns:
          range (list): List representing number range
        """
        # Split string and limit resulting list to max. two elements
        num_range = range_string.split('-')[:2]

        # Convert list elements to integer
        for i in range(len(num_range)):
            num_range[i] = int(num_range[i])

        # Fill list to at least two elements
        while len(num_range) < 2:
            # No element was given
            if not num_range[0]:
                # Add "1" as first one
                num_range.append(1)

            # Append first element again
            num_range.append(num_range[0])

        # Sort list
        num_range.sort()

        # Filling up
        if fill is True:
            _num_range = []

            for n in range(num_range[0], num_range[-1]+1):
                _num_range.append(n)

            num_range = _num_range

        return num_range
