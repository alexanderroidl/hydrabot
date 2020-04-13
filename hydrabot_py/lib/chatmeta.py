#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   CHAT META - chatmeta.py

   Provides abstract and meta classes
"""


# Dependencies
from abc import ABC, abstractmethod


class ChatMessage(ABC):
    """A chat message abstract base class

    Args:
      texts (str|list): Text strings
    """

    def __init__(self, texts):
        # Converts texts parameter to list if it wasn't already
        self.texts = texts if isinstance(texts, list) else [texts]

        # Initialize ABC parent class
        super().__init__()

    @property
    @abstractmethod
    def texts(self):
        """Property to hold text list"""
        pass

    # Convert instance to string
    def __str__(self):
        texts_string = '\n'

        for single_text in self.texts:
            if not isinstance(single_text, list):
                single_text = [single_text]

            for single_text_part in single_text:
                texts_string += '   {}\n'.format(str(single_text_part))

        return '<{0}>{1}</{0}>'.format(
            self.__class__.__name__, texts_string
        )


class ChatAction(ABC):
    """A chat action abstract base class"""

    def __init__(self):
        # Initialize ABC parent class
        super().__init__()

    @abstractmethod
    def exec(self):
        """Defines calls to perform upon execution"""
        pass

    # Convert instance to string
    def __str__(self):
        return '<<{0}>>'.format(self.__class__.__name__)
