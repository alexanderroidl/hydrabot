#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   TIME HELPER - timehelper.py

    Provides utilities for calculating/converting time
    and datetime objects from/to different formats
"""


# Dependencies
import math
from datetime import datetime, date


class TimeHelper:
    """Provides utilities for calculating/converting time
    and datetime objects from/to different formats"""

    @staticmethod
    def is_between(begin_time, end_time, compare_time):
        """Indicates whever specific time is between two time objects"""
        if begin_time < end_time:
            return compare_time >= begin_time and compare_time <= end_time
        else:  # crosses midnight
            return compare_time >= begin_time or compare_time <= end_time

    @staticmethod
    def combine(*argv):
        """Combines time objects with current datetime"""
        times = []

        for arg in argv:
            combined_time = datetime.combine(date.today(), arg)
            times.append(combined_time)

        return tuple(times)

    @staticmethod
    def secs_since(earlier_datetime):
        """Calculates seconds passed from now since earlier datetime"""
        secs = (datetime.now() - earlier_datetime).total_seconds()
        return math.floor(secs)

    @staticmethod
    def strings_to_times(*argv):
        """Convert time strings to time objects"""
        times = []

        for arg in argv:
            converted_time = datetime.strptime(arg, '%H:%M').time()
            times.append(converted_time)

        return tuple(times)

    @staticmethod
    def get_start_time_difference_sec(start_datetime, end_datetime):
        """Get time passed since start time in seconds

        Args:
          start_datetime (datetime)
          end_datetime (datetime)

        Returns:
          difference_in_sec (int)
        """
        start_difference_sec = 0
        datetime_now = datetime.now()

        # Calculate time difference if round was started
        # between designated times
        if (datetime_now > start_datetime
                and datetime_now < end_datetime):
            start_difference_sec = TimeHelper.secs_since(start_datetime)

        return start_difference_sec
