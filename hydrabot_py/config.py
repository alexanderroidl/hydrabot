#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   CONFIGURATION - config.py

   This file only contains a CONFIG dictionary, explanations
   on possible values are given above each key
"""


CONFIG = {
    # Facebook E-Mail
    'fb_email': '<YOUR_EMAIL_HERE>',
    # Facebook password (None will lead to password prompt)
    'fb_password': None,
    # Facebook thread ID (None will lead to user himself)
    #  What it is and how to retrieve it:
    #  https://fbchat.readthedocs.io/en/stable/intro.html#threads
    'fb_thread_id': None,
    # Message collection
    #  {{SPLIT}} splits a message into several messages
    #  {{DELAY}} causes a five second DELAY between messages
    'messages': [
        'I thought you needed to watch that now:{{SPLIT}}'
        + 'https://www.youtube.com/watch?v=iIQrPKqisZE',
        'Remember to stay hydrated!',
        'On the way to the sink yet? 💦',
        'Water is essential. It hydrates you, keeps you recharged '
        + 'naturally, flushes out toxins, regulates body temperature, '
        + 'maintains blood pressure and helps keep vital body '
        + 'functioning in check.',
        'Before you sleep, take a sip',
        'Water is love. Water is life.',
        'I\'m just a bot programmed by Alex Roidl to tell you to drink water,\n'
        + 'still I feel how my course is of importance.{{SPLIT}}'
        + 'Therefore drink something!',
        'Beep bop. Beep?',
        '"Water drink you must" (Yoda, 1083-1983)',
        'sleepy?\ndrink water.\n\n'
        + 'annoyed?\ndrink water.\n\n'
        + 'angry?\ndrink water.'
    ],
    # Start time
    #  Format: HH:MM
    'start_time': '00:00',
    # End time
    #  Format: HH:MM
    'end_time': '23:59',
    # Conversation emoji to randomly change to
    #  Whether this emoji will temporarily be set depends on
    #  configuration value "change_emoji_chance"
    'thread_emoji': '🚰',
    # Pool of emojis to choose from
    'emojis': [
        '💦', '💦', '💧', '👀', '🦑', '🚰'
    ],
    # Search phrases for Google Image Search
    'gis_search_phrases': [
        'drink+water',
        'drink+water',
        'drink+water',
        'science+water',
        'water',
        'water',
        'water',
        'water+quote',
        'water+quote'
    ],
    # Search phrases for Giphy
    'giphy_search_phrases': [
        'drink+water',
        'drink+water',
        'spit+drink',
        'wink',
        'wink',
        'robot',
        'stay+hydrated'
    ],
    # Minimum image chance per hour
    #  e.g. 1/2 = One message per two hours
    'min_message_ratio': 1/3,
    # Maximum image chance per hour
    #  e.g. 2 = Two message per hour
    'max_message_ratio': 1/2,
    # Announce by waving before sending (0-1)
    'announce_chance': 0.4,
    # Chance of changing emoji for messaging duration (0-1)
    'change_emoji_chance': 0.25,
    # Chance of sending text per message (0-1)
    'text_chance_per_message': 0.9,
    # Chance of sending emoji text (0-1)
    'emojis_chance_per_message': 0.5,
    # Chance of sending an image (0-1)
    'image_chance_per_message': 0,
    # Emojis count range
    #  Format: "<default_number>"
    #  Format: "<min_number>-<max-number>"
    #  Example: "2-7" = Two to seven emojis
    'emojis_count_range': '1-4',
    # Chance of either using Google Image Search or Giphy for getting an image
    # None will lead to random choice
    #  The closer the number is to 0, the higher the chance for GIS gets
    #  The closer the number is to 1, the higher the chance for Giphy will be
    #  Example: 0 = 100% GIS/0% Giphy; 0.2 = 80% GIS/20% Giphy
    'image_gis_giphy_chance': 0.65,
    # Google Image Search API key
    'gis_api_key': None,
    # Google Image Search Project CX
    'gis_project_cx': None,
    # Provide dummy URL to always use instead of actual search
    # 'image_dummy_url': 'https://upload.wikimedia.org/'
    # + 'wikipedia/en/thumb/6/64/Windows_XP_Luna.png/300px-Windows_XP_Luna.png',
    'image_dummy_url': None,
    # Giphy API key
    'giphy_api_key': None,
    # Preview behaviour only, don't actually use FB
    'demo_mode': False,
    # Send messages immediately and ignore timings
    'test_mode': False,
    # Facebook user agent (None will lead to random user agent)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}
