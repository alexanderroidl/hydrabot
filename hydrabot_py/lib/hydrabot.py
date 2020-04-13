#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   HYDRABOT - hydrabot.py

   Contains core functionality for the bot.

   The HydraBot class in here holds everything together,
   it creates interaction between different layers of
   abstraction and let's the Bot's magic happen
"""


# Dependencies
from datetime import datetime, time, timedelta
import time as timeh
import random
import math
import logging
import sys
import re
# Local dependencies
from .timehelper import TimeHelper
from .types import tcolors
from .imagesearch import ImageSearch
from .chatbot import ChatBot
from .chatmessages import (
    ChatMessageHolder,
    TextMessage, EmojiMessage, ImageMessage
)




# The main bot class
class HydraBot:
    """Contains core functionality for the bot.

    This class is meant to be used as singleton,
    it creates interaction between different layers of
    abstraction and let's the Bot's magic happen

    Args:
      fb_email (str):
        Facebook users email
      fb_password (str):
        Facebook users password, None will lead to prompt
      fb_thread_id (str):
        Facebook thread ID, defaults to users own thread
      messages (list):
        Pool of message texts to choose from
      start_time (str):
        Format is HH:MM
      end_time (str):
        Format is HH:MM
      min_message_ratio (float):
        Minimum image chance per hour
        Example: 0.5=Half a message per hour -> One message in two hours
      max_message_ratio (float):
        Maximum image chance per hour
        Example: 1=One message per hour
      text_chance_per_message (float):
        Chance of sending text per message (0-1)
      emojis (list):
        Pool of emojis to choose from (defaults to empty list)
      emojis_count_range (str):
        Format: "<default_number>" or "<min_number>-<max-number>"
        Example: "2-7" = Two to seven emojis
        Defaults to "1"
      emojis_chance_per_message (float):
        Chance of sending emoji text (0-1), defaults to 0
      image_chance_per_message (float):
        Chance of sending an image (0-1), defaults to 0
      image_gis_giphy_chance (float):
        Chance of either using Google Image Search or Giphy for
        getting an image
        The closer the number is to 0, the higher the chance for GIS gets
        The closer the number is to 1, the higher the chance for Giphy will be
        Example: 0 = 100% GIS/0% Giphy; 0.2 = 80% GIS/20% Giphy
      announce_chance (float):
        Announce by waving before sending (0-1)
      thread_emoji: (str):
        Conversation emoji to randomly change to (None)
      change_emoji_chance (float):
        Chance of changing emoji for messaging duration (0-1), defaults to 0
      demo_mode (bool):
        Preview behaviour only (False)
      test_mode (bool):
        Send messages immediately and ignore timings (False)
      gis_api_key (str):
        Google Image Search API key (None)
      gis_project_cx (str):
        Google Image Search project CX (None)
      gis_search_phrases (list):
        Pool of GIS search phrases (empty)
      giphy_api_key (str):
        Giphy API key (None)
      giphy_search_phrases (list):
        Pool of Giphy search phrases (empty)
      image_dummy_url (str):
        Dummy Image URL to use instead of search (None)
      user_agent (str):
        User agent to use for login, None will lead to random agent
    """
    start_datetime = None
    end_datetime = None
    messages = None
    text_chance_per_message = None
    announce_chance = None
    thread_emoji = None
    change_emoji_chance = None
    emojis = None
    emojis_count_range_text = None
    emojis_chance_per_message = None
    image_chance_per_message = None
    min_messages_per_hour = None
    max_messages_per_hour = None

    chatbot = None
    round = 0
    round_messages = []
    round_intervals = []
    run_num = 0
    active = False
    timespan_sec = 0
    message_ratio = 0
    image_search = None
    demo_mode = None
    test_mode = None

    def __init__(self, fb_email, fb_password, fb_thread_id,
                 messages,
                 start_time, end_time,
                 min_message_ratio=0, max_message_ratio=None,
                 text_chance_per_message=1,
                 emojis=[], emojis_count_range='1-1',
                 emojis_chance_per_message=0,
                 image_chance_per_message=0, image_gis_giphy_chance=0,
                 announce_chance=0,
                 thread_emoji=None, change_emoji_chance=0,
                 demo_mode=False, test_mode=False,
                 gis_api_key=None, gis_project_cx=None, gis_search_phrases=[],
                 giphy_api_key=None, giphy_search_phrases=[],
                 image_dummy_url=None,
                 user_agent=None):
        if max_message_ratio is None:
            max_message_ratio = min_message_ratio

        self.messages = messages
        self.text_chance_per_message = text_chance_per_message
        self.emojis = emojis
        self.emojis_chance_per_message = emojis_chance_per_message
        self.min_messages_per_hour = min_message_ratio
        self.max_messages_per_hour = max_message_ratio
        self.announce_chance = announce_chance
        self.change_emoji_chance = change_emoji_chance
        self.gis_search_phrases = gis_search_phrases
        self.giphy_search_phrases = giphy_search_phrases
        self.image_chance_per_message = image_chance_per_message
        self.image_gis_giphy_chance = image_gis_giphy_chance
        self.image_dummy_url = image_dummy_url
        self.thread_emoji = thread_emoji
        self.change_emoji_chance = change_emoji_chance
        self.demo_mode = demo_mode
        self.test_mode = test_mode

        if not demo_mode:
            self.chatbot = ChatBot(
                email=fb_email,
                password=fb_password,
                thread_id=fb_thread_id,
                user_agent=user_agent
            )

        start_time, end_time = TimeHelper.strings_to_times(
            start_time,
            end_time
        )

        self.start_datetime, self.end_datetime = self.get_datetimes(
            start_time,
            end_time
        )

        self.timespan_sec, _, _ = self.calc_timings(
            self.start_datetime,
            self.end_datetime
        )

        self.emojis_count_range_text = emojis_count_range

        self.image_search = ImageSearch(
            gis_api_key=gis_api_key,
            gis_project_cx=gis_project_cx,
            gis_search_phrases=gis_search_phrases,
            giphy_api_key=giphy_api_key,
            giphy_search_phrases=giphy_search_phrases
        )

        self.config()
        self.start()

    def config(self):
        """Initial configuration for the bot"""
        # CONFIGURE LOGGERS
        # Add mode prefixes to logging format
        prefix = ''

        prefix += (' [DEMO]' if self.demo_mode else '')
        prefix += (' [TEST]' if self.test_mode else '')

        logging.basicConfig(
            filename='hydrabot.log',
            filemode='a',
            format='[%(asctime)s]{} %(message)s'.format(prefix),
            datefmt='%d.%m.%Y %H:%M',
            level=logging.INFO
        )

        # Silence Google API Client discovery logger
        logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)

        # Silence Google API Client discovery_cache logger
        logging.getLogger('googleapiclient.discovery_cache').setLevel(
            logging.ERROR
        )

        # Silence FB Client logger
        logging.getLogger('client').setLevel(logging.ERROR)

    def get_datetimes(self, start_time, end_time):
        """Get datetimes for given start and end time objects"""
        # Check whether time logic and given numbers correspond
        start_datetime, end_datetime = TimeHelper.combine(start_time, end_time)

        # Time was given across midnight, so we increase end time
        # by one day
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)

        # TODO: Check again whether that's required
        # if start_datetime < datetime.now():
        #     start_datetime += timedelta(days=1)
        #     end_datetime += timedelta(days=1)

        return start_datetime, end_datetime

    def calc_timings(self, start_time, end_time):
        """Calculate/generate required timings based off time objects"""
        timespan_sec = (end_time - start_time).total_seconds()
        timespan_hours = timespan_sec / 60 / 60
        min_message_ratio = timespan_hours * self.min_messages_per_hour

        # Calculated minimum amount of messages not met
        if min_message_ratio >= len(self.messages):
            raise ValueError(
                ('You provided {0} messages, at least {3} are required\n'
                    + '(Given timespan equals ~{1} hours, '
                    + 'min. ~{2} messages per hour wanted '
                    + '= {3} messages)').format(
                    len(self.messages),
                    str(math.floor(timespan_hours * 100) / 100),
                    str(math.floor(self.min_messages_per_hour * 100) / 100),
                    str(math.floor(min_message_ratio))
                ))

        return timespan_sec, timespan_hours, min_message_ratio

    def is_currently_active(self):
        """Indicates wherer current time is in between bot's
        designated timespan as boolean"""
        return TimeHelper.is_between(
            self.start_datetime, self.end_datetime, datetime.now()
        )

    def calculate_intervals(self, timespan_sec, message_ratio, message_count):
        """Calculate message intervals in seconds

        Args:
          timespan_sec (int): Timespan in seconds
          message_ratio (float): Message ratio per hour
          message_count (int): Message count per hour

        Returns:
          List of intervals in seconds
        """
        average_interval = math.floor(timespan_sec / message_ratio)
        def_interval = timespan_sec / message_count
        interval_treshold = def_interval - average_interval

        intervals = []
        while len(intervals) < message_count:
            random_treshold = random.uniform(0, interval_treshold)

            if bool(random.getrandbits(1)):
                random_treshold *= -1

            base = average_interval * random.uniform(0.4, 1.0)

            interval = base + random_treshold

            if len(intervals) > 0:
                interval = interval + intervals[-1]

            intervals.append(interval)

        return intervals

    def show_datetimes_for_intervals(self, intervals):
        """Prints interval in readable format

        Args:
          intervals (list): List of intervals in seconds
        """
        message_time_texts = []

        for seconds in intervals:
            time_now = datetime.now()
            target_datetime = time_now + timedelta(seconds=seconds)

            message_text = target_datetime.strftime('%H:%M')
            if target_datetime.date() > time_now.date():
                message_text = '(+1) ' + message_text
            message_text = tcolors.UNDERLINE + message_text + tcolors.ENDC

            message_time_texts.append(message_text)

        HydraBot.log_and_print('Calculated message times: '
                               + (', '.join(message_time_texts)))

    def round_start(self):
        """Start a new round"""
        # Caculate timespans
        start_time_diff_sec = TimeHelper.get_start_time_difference_sec(
            self.start_datetime,
            self.end_datetime
        )
        timespan_sec = self.timespan_sec - start_time_diff_sec
        timespan_hours = timespan_sec / 60 / 60
        max_messages_ratio = self.max_messages_per_hour

        # Adjust max messages if number was too high
        if timespan_hours * max_messages_ratio >= len(self.messages):
            max_messages_ratio = len(self.messages) - 1

        # Calculate ratio for messages
        message_ratio = timespan_hours * random.uniform(
            self.min_messages_per_hour,
            max_messages_ratio
        )

        message_count = math.floor(message_ratio)

        # Less than a single message in total
        if message_count < 1:
            message_count = 1
            message_ratio = 1

            HydraBot.log_and_print(
                tcolors.WARNING
                + 'Not enough time for minimum message amount given\n'
                + tcolors.OKGREEN
                + 'Forcing at least a single message...'
                + tcolors.ENDC
            )

        # Calculate intervals
        intervals = self.calculate_intervals(
            timespan_sec=timespan_sec,
            message_ratio=message_ratio,
            message_count=message_count
        )

        # Prepare shuffled messages
        messages = self.messages.copy()
        random.shuffle(messages)
        messages = messages[slice(0, message_count)]
        # Uncomment bottom line for always forcing first message
        # Useful to perpously debug a single message
        #messages[0] = self.messages[2]  # Debug

        # Set round variables
        self.round_messages = messages
        self.round_intervals = intervals

        # Info about intervals
        HydraBot.log_and_print(
            tcolors.OKGREEN
            + ('Generated {} message{}').format(
                message_count,
                's' if message_count > 1 else ''
            )
            + tcolors.ENDC
        )

        self.show_datetimes_for_intervals(intervals)

    @staticmethod
    def log_and_print(*args):
        """Log and print something"""
        print(*args)

        # Remove ANSI escape characters for logging
        ansi_re = re.compile(r'\x1b\[[0-9;]*m')
        logging.info(' '.join(re.sub(ansi_re, '', str(a))
                              for a in args).encode('utf-8'))

    @staticmethod
    def log_and_print_line():
        """Log and print long line"""
        HydraBot.log_and_print('=' * 25)

    def sleep(self, seconds):
        """Sleep if not in demo mode"""
        if not self.test_mode:
            timeh.sleep(seconds)

    def get_text_message(self, run_count):
        """(Maybe) provides a TextMessage instance"""
        message_uses_text = random.uniform(0, 1) < self.text_chance_per_message

        if not message_uses_text:
            return None

        return TextMessage(self.round_messages[run_count])

    def get_emoji_message(self):
        """(Maybe) provides an EmojiMessage instance"""
        # Randomly decide to use or skip emojis
        uses_emojis = random.uniform(0, 1) < self.emojis_chance_per_message

        # Message won't use emojis or none were provided
        if not (uses_emojis and len(self.emojis) > 0):
            return None

        # Generate random emoji text
        emoji_message_text = EmojiMessage.generate_text(
            emojis_pool=self.emojis,
            emojis_count_range_text=self.emojis_count_range_text
        )

        # Emoji text couldn't be generated
        if not (emoji_message_text and len(emoji_message_text)):
            return None

        return EmojiMessage(emoji_message_text)

    def get_image_message(self):
        """(Maybe) provides an ImageMessage instance"""
        image_search = self.image_search
        image_chance = self.image_chance_per_message
        message_uses_image = random.uniform(0, 1) < image_chance

        if not (message_uses_image and image_search.is_ready()):
            return None

        image_url, search_phrase, engine_name = image_search.get_random_url(
            gis_giphy_chance=self.image_gis_giphy_chance
        )

        # Inform about used search query
        HydraBot.log_and_print(
            tcolors.OKGREEN
            + ('Using image search query "{}" ({})'
                .format(search_phrase, engine_name))
            + tcolors.ENDC
        )

        return ImageMessage(image_url)

    def send_image_url(self, image_url):
        """Sends an image based off an URL"""
        if not self.demo_mode:
            self.chatbot.send_image_url(image_url)

        HydraBot.log_and_print('<{}>'.format(image_url))

    def announce(self):
        """Wave and wait a little"""
        HydraBot.log_and_print(
            tcolors.OKBLUE
            + '(waves and waits)'
            + tcolors.ENDC)

        if not self.demo_mode:
            self.chatbot.wave()
            self.sleep(12)

    def change_emoji(self):
        """Changes the conversation emoji and returns the previous one"""
        previous_emoji = ''

        if not self.demo_mode:
            previous_emoji = self.chatbot.get_emoji()
            self.chatbot.set_thread_emoji(self.thread_emoji)

        # Couldn't fetch previous emoji
        if previous_emoji is None:
            HydraBot.log_and_print(
                tcolors.FAIL
                + 'Couldn\'t fetch thread emoji :('
                + tcolors.ENDC
            )
        else:  # Successfully fetched old emoji
            HydraBot.log_and_print(
                tcolors.OKBLUE
                + '(changes emoji to {})'.format(self.thread_emoji)
                + tcolors.ENDC
            )

            self.sleep(5)

        return previous_emoji

    def run(self, run_count):
        """Send single message package

        Args:
          run_count (int): Number of bot runs
        """
        chat_message_holder = None

        # Iterate until at least one text, image or emoji message was generated
        while not (chat_message_holder and chat_message_holder.count()):
            chat_message_holder = ChatMessageHolder(
                self.get_text_message(run_count),
                self.get_image_message(),
                self.get_emoji_message()
            )

        # Log/print line
        HydraBot.log_and_print_line()

        # Maybe change conversation emoji
        changes_emoji = random.uniform(0, 1) < self.change_emoji_chance
        previous_emoji = None

        # Emoji for change was given and decided to perform change
        if changes_emoji and self.thread_emoji is not None:
            previous_emoji = self.change_emoji()

        # Maybe announce by waving before
        announces_itself = random.uniform(0, 1) < self.announce_chance
        if announces_itself:
            self.announce()

        # Perform schedules
        chat_messages = chat_message_holder.get_messages(shuffle=True)
        for chat_message in chat_messages:
            if not self.demo_mode:
                self.chatbot.send(chat_message)

            HydraBot.log_and_print(
                tcolors.OKBLUE
                + str(chat_message)
                + tcolors.ENDC
            )

        # Previous emoji was provided, therefore change it back
        if previous_emoji is not None:
            if not self.demo_mode:
                self.chatbot.set_thread_emoji(previous_emoji)

            HydraBot.log_and_print(
                tcolors.OKBLUE
                + '(changes emoji back)'
                + tcolors.ENDC
            )

        HydraBot.log_and_print_line()

    def start(self):
        """Get everything going"""
        # Variables to keep track of rounds
        done = False
        active = False
        run_num = 0

        # Main loop
        while True:
            current_day = datetime.now().date()
            if current_day > self.start_datetime.date():
                self.start_datetime += timedelta(day=1)
                self.end_datetime += timedelta(day=1)

                # TODO: Remove if working
                HydraBot.log_and_print('Day has increased ({})'.format(
                    str(current_day)
                ))
                HydraBot.log_and_print('Start=' + str(self.start_datetime))
                HydraBot.log_and_print('End=' + str(self.end_datetime))

            active_now = self.is_currently_active() or self.test_mode

            # A new round has begun
            if active_now is True and active_now != active:
                run_num = 0
                done = False
                active = active_now
                self.round_start()

            if active_now is False or done is True:
                # TODO: Sleep once for precise amount of time
                print('Inactive...')
                timeh.sleep(5)
                continue

            # Behaviour starts
            time_before_run = datetime.now()

            # Sleep
            time_to_sleep = 0

            # Inform about actions
            if self.demo_mode or self.test_mode:
                if self.demo_mode and self.test_mode:
                    action = 'demo and test'
                elif self.demo_mode:
                    action = 'demo'
                elif self.test_mode:
                    action = 'test'

                HydraBot.log_and_print(
                    'Will ' + tcolors.BOLD + action + tcolors.ENDC + ' now...')

            if not self.test_mode:
                time_to_sleep = self.round_intervals[run_num]
                time_now = datetime.now()

                time_when_send = time_now + timedelta(seconds=time_to_sleep)
                time_when_send_text = time_when_send.strftime('%H:%M')

                if time_when_send.date() > time_now.date():
                    time_when_send_text = '(+1) ' + time_when_send_text

                HydraBot.log_and_print(
                    'Will send in {} minutes... ({})'.format(
                        math.floor(time_to_sleep / 60),
                        time_when_send_text
                    )
                )

            self.sleep(time_to_sleep)

            # Will message now
            self.run(run_num)

            # Increase run count
            run_num += 1

            # Not the last run
            if run_num < len(self.round_intervals):
                # Substract time used for requests/calculations/etc
                # from next interval
                seconds_difference = TimeHelper.secs_since(time_before_run)
                self.round_intervals[run_num] -= seconds_difference
            else:
                done = True

                HydraBot.log_and_print(
                    tcolors.OKGREEN
                    + 'All messages sent, done for now'
                    + tcolors.ENDC
                )

                if self.test_mode:
                    HydraBot.log_and_print(
                        tcolors.FAIL
                        + 'Shutting down due to test mode'
                        + tcolors.ENDC
                    )

                    sys.exit()

    def clean_up(self):
        """Cleans up (suitable for program exit)"""
        # Logout from Facebook if possible and session isn't used
        if (not self.demo_mode
                and not self.chatbot.session_file_exists()):
            self.chatbot.logout()
