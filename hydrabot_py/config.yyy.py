#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   CONFIGURATION - config.py

   This file only contains a CONFIG dictionary, explanations
   on possible values are given above each key
"""


CONFIG = {
    # Facebook E-Mail
    'fb_email': 'i.am.awesome.96@live.de',
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
        '⌛️ Time ⌛️ is just right ✔️✔️ to learn 📘 something about'
        + '💦😵💦 dehydration 💦😵💦, 👀 right?{{SPLIT}}'
        + 'https://www.youtube.com/watch?v=sDzsZkU_BnE',
        'Hey there!{{SPLIT}}'
        + 'Sorry, I didn\'t see 👀 you 👈 at first..{{SPLIT}}'
        + '{{DELAY}}{{SPLIT}}'
        + 'Are you here often?{{SPLIT}}'
        + 'I just wanted to say...{{SPLIT}}'
        + 'YoU bEtTeR dRiNk SoMe Of ThAt GoOd OlD wAtEr',
        'you{{SPLIT}}should{{SPLIT}}drink...{{SPLIT}}WATER!',
        'Remember to stay hydrated, baby!',
        'YOU BETTER DRINK WATER!!!',
        'ישוע רוצה שתשתה מים',
        'What on earth is even real?{{SPLIT}}'
        + '{{DELAY}}{{SPLIT}}'
        + 'Easy answer:{{SPLIT}}'
        + 'Dehydration is.{{SPLIT}}'
        + 'That\'s why you should have a schluck now!',
        'On the way to the sink yet? 💦',
        'Capitalism is determined to fail. Thursty yet? 😏',
        'Water is essential. It hydrates you, keeps you recharged '
        + 'naturally, flushes out toxins, regulates body temperature, '
        + 'maintains blood pressure and helps keep vital body '
        + 'functioning in check.',
        'Before you sleep, take a sip',
        'Water Water Water Water Water Water Water Water Water Water '
        + 'Water Water Water Water Water Water Water Water Water Water '
        + 'Water Water Water Water Water Water Water Water Water Water '
        + 'Water Water Water Water Water Water Water Water Water Water ',
        'Water?',
        'Water Water Water Water Water Water Water Water Water Water Water '
        + 'Water Water Water Water Water Water Water Water Water{{SPLIT}}'
        + 'Water Water Water Water Water Water Water Water Water Water Water '
        + 'Water Water Water Water Water Water Water Water Water',
        'Water is love. Water is life.',
        'I\'m just a bot programmed by Alex to tell you to drink water,\n'
        + 'still I feel how my course is of importance.{{SPLIT}}'
        + 'Therefore drink something!{{SPLIT}}'
        + '{{DELAY}}{{SPLIT}}'
        + 'baby-o...',
        'Beep bop. Beep?',
        '🦆{{SPLIT}}'
        + 'Hello{{SPLIT}}'
        + 'I am a very rich 💸💸 bot prince of Nigeria. 💯\n\n'
        + 'All my bitcoin wealth 💰, estimated 420,000 $ 😱 has been frozen ⛸ '
        + 'in a swiss bank account.\n\n'
        + 'In order to gain 🗝 access back, I need your help. 🆘🆘🆘'
        + '{{SPLIT}}{{DELAY}}{{SPLIT}}'
        + 'I talked 🤤 to my accountants, which led to us agreeing on offering '
        + 'you 1.337 % shares of my fortune, under one condition.{{SPLIT}}'
        + 'You need to drink 2️⃣ glasses 💦 of water...{{SPLIT}}'
        + 'RIGHT NOW. ⏰🔥',
        '"Water drink you must" (Yoda, 1083-1983)',
        'Knock knock? Just kidding, you should drink some.',
        'Waaaaaaaaaaaaaaaaaaaaaaaaaaattttttteeeeeeeeeeer',
        'Trink ein Wasser, Babygirl!',
        'sleepy?\ndrink water.\n\n'
        + 'annoyed?\ndrink water.\n\n'
        + 'angry?\ndrink water.',
        'L\'eau est une grande baguette',
        'Bebe un océano con un zapato',
        '🔫🤠{{SPLIT}}'
        + 'your dehydration...\n'
        + 'put it in the bag'
    ],
    # Start time
    #  Format: HH:MM
    'start_time': '12:10',
    # End time
    #  Format: HH:MM
    'end_time': '21:22',
    # Conversation emoji to randomly change to
    #  Whether this emoji will temporarily be set depends on
    #  configuration value "change_emoji_chance"
    'thread_emoji': '🚰',
    # Pool of emojis to choose from
    'emojis': [
        '🤼', '🍆', '🍆', '🦑', '😩', '💦', '💦', '👀',
        '🦆', '🦆', '🚑', '🚑', '🤖',
        '😵', '😘', '🔜', '💯', '💧', '(.)(.)', '🤤',
        '🚰', '🚰', '🚰', '💌', '🌭', '🔥', '😩',
        '🤼', '🍆', '🍆', '🦑', '😩', '💦', '💦',
        '😵', '😘', '🔜', '💯', '💧', '(.)(.)', '🤤',
        '🚰', '🚰', '🚰', '💌', '🌭', '🔥', '😩',
        'Jeffrey Epstein did not kill himself',
        '👉👌', '👉👌', '👉👌', '👉👌'
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
        'water+quote',
        'aquaman',
        'aquaman+comic',
        'poseidon'
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
    'image_chance_per_message': 1,
    # Emojis count range
    #  Format: "<default_number>"
    #  Format: "<min_number>-<max-number>"
    #  Example: "2-7" = Two to seven emojis
    'emojis_count_range': '2-7',
    # Chance of either using Google Image Search or Giphy for getting an image
    # None will lead to random choice
    #  The closer the number is to 0, the higher the chance for GIS gets
    #  The closer the number is to 1, the higher the chance for Giphy will be
    #  Example: 0 = 100% GIS/0% Giphy; 0.2 = 80% GIS/20% Giphy
    'image_gis_giphy_chance': 0.65,
    # Google Image Search API key
    'gis_api_key': 'AIzaSyCsPZsajF-NhdmxLQapAa0oiCcE4-C2d2Q',
    # Google Image Search Project CX
    'gis_project_cx': '008004703885484592765:ioyyzdaemzz',
    # Provide dummy URL to always use instead of actual search
    # 'image_dummy_url': 'https://upload.wikimedia.org/'
    # + 'wikipedia/en/thumb/6/64/Windows_XP_Luna.png/300px-Windows_XP_Luna.png',
    'image_dummy_url': None,
    # Giphy API key
    'giphy_api_key': 'VsRhX1RWPMjWUyDu5QNPfjO4a0PKmWEx',
    # Preview behaviour only, don't actually use FB
    'demo_mode': True,
    # Send messages immediately and ignore timings
    'test_mode': True,
    # Facebook user agent (None will lead to random user agent)
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}
