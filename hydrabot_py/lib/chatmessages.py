#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   CHAT MESSAGES - chatmessages.py

   Here classes required to simplify the handling of different
   types of messages are handled
"""


# Dependencies
import random
import re
import time
# Local dependencies
from .chatmeta import ChatAction, ChatMessage
from .util import Util


class ChatMessageHolder:
    """Holds multiple ChatMessage instances and provides utility
    methods for them

    Args:
      \\*messages (*args): ChatMessage instances to be held
    """
    messages = None

    def __init__(self, *messages):
        self.messages = []

        for message in messages:
            if isinstance(message, ChatMessage):
                self.messages.append(message)

    def count(self):
        """Counts messages"""
        return len(self.messages)

    def get_messages(self, shuffle=False):
        """Get (shuffled) message list"""
        # Immediately return messages if shuffling isn't wanted
        if not shuffle:
            return self.messages

        messages_shuffled = self.messages.copy()
        random.shuffle(messages_shuffled)
        return messages_shuffled


class EmojiMessage(ChatMessage):
    """Represents an emoji message containing emoji texts

    Args:
      texts (str|list): Emoji text strings
    """
    texts = []

    def __init__(self, texts):
        super(EmojiMessage, self).__init__(texts)

    @staticmethod
    def generate_text(emojis_pool, emojis_count_range_text):
        """Generates a random emoji string"""
        emojis_count_range = Util.get_num_range(
            range_string=emojis_count_range_text,
            fill=True
        )

        # Random emoji count
        emoji_count = random.choice(emojis_count_range)
        emojis = []

        # Append random emojis to list
        while(len(emojis) < emoji_count):
            random_emoji = random.choice(emojis_pool)
            emojis.append(random_emoji)

        # Join emoji list to string
        return ''.join(emojis)


class TextMessage(ChatMessage):
    """Represents a text message containing normal texts

    Args:
      texts (str|list): Text strings
    """
    texts = []
    # Placeholder RegExp pattern
    placeholder_pattern = re.compile(r'\{{2}(\w+):?(.*?)\}{2}')

    def __init__(self, texts):
        processed_texts = []

        for text in texts if isinstance(texts, list) else [texts]:
            processed_texts.append(self.process_text(text))

        super(TextMessage, self).__init__(processed_texts)

    def process_text(self, text):
        """Processes placeholders in a text and allows for text splitting
        and insertation of special actions"""
        # Split text based on pattern
        text_list = text.split('{{SPLIT}}')
        processed_text_list = []

        # Iterate through single texts
        for single_text in text_list:
            skip_text = False

            # Find all placeholder occurances
            placeholder_matches = re.findall(
                self.placeholder_pattern,
                single_text
            )

            # Iterate through placeholder occurances
            for placeholder_match in placeholder_matches:
                placeholder_name, placeholder_value = placeholder_match

                # DELAY placeholder found
                if placeholder_name == 'DELAY':
                    processed_text_list.append(MessageDelay())
                    skip_text = True

                # Parameterized IMG placeholder found
                if placeholder_name == 'IMG' and len(placeholder_value):
                    print('Image')
                    # TODO: Add functionality
                    skip_text = True

            # Text is useable and didn't contain placeholders
            if not skip_text:
                processed_text_list.append(single_text)

        return processed_text_list


class ImageMessage(ChatMessage):
    """Represents an image message containing URL texts

    Args:
      texts (str|list): Image URL strings
    """
    texts = []

    def __init__(self, images):
        super(ImageMessage, self).__init__(images)


class MessageDelay(ChatAction):
    """Represents a message delay"""

    def __init__(self):
        super().__init__()

    # Define acion to execute
    def exec(self):
        # Sleep for five seconds
        time.sleep(5)
