#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   CHATBOT - chatbot.py

   Manages communications with Facebook Messenger API
   (https://github.com/rehabstudio/fbmessenger)
"""


# Dependencies
from getpass import getpass
import json
import os
import time
from fbchat import Client
from fbchat.models import Message, TypingStatus, ThreadType
# Local dependencies
from .chatmeta import ChatAction
from .chatmessages import TextMessage, ImageMessage, EmojiMessage


# Remember to use time.sleep occasionally to mimic user behaviour!
class ChatBot(Client):
    """Manages communications with Facebook Messenger API

    Args:
      email (str): Facebook users email
      password (str): Facebook users password, None will lead to prompt (None)
      session_file (str): Default session file path, defaults to "session.json"
      thread_id (str): Facebook thread ID, None -> users own thread (None)
      thread_type (ThreadType): Type of thread (ThreadType.USER)
      **kwargs (kwargs): Optional arguments for fbchat's Client class
    """
    session_file = None
    thread_id = None

    def __init__(self, email, password=None, session_file='session.json',
                 thread_id=None, thread_type=ThreadType.USER,
                 **kwargs):
        if password is None:
            password = getpass('Please enter the password for "{}":'.format(
                email
            ))

        self.session_file = session_file
        session_cookies = self.load_session() if session_file else None

        # Initialize super instance
        super().__init__(
            email=email,
            password=password,
            session_cookies=session_cookies,
            **kwargs
        )

        # Use user's own thread ID if none was given
        if thread_id is None:
            thread_id = self.uid

        self.thread_id = thread_id
        self.setDefaultThread(thread_id, thread_type)

        # Save session if filename was provided
        if session_file:
            self.save_session()

    def session_file_exists(self):
        """Returns bool indicating whether session file exists"""
        return os.path.exists(self.session_file)

    def load_session(self, session_file=None):
        """Loads session from JSON file

        Args:
          session_file (string): Path to session file, None uses default (None)

        Returns:
          session_cookies (dict): Session cookies
        """
        session_cookies = None

        # No session file parameter given, therefore use class property instead
        if session_file is None:
            session_file = self.session_file

        # Session file was found
        if self.session_file_exists():
            with open(session_file, 'r') as f:
                # Load JSON from file contents
                session_cookies = json.load(f)

        return session_cookies

    def save_session(self, session_file=None):
        """Saves current session to JSON file

        Args:
          session_file (string): Path to session file, None uses default (None)
        """
        # No session file parameter given, therefore use class property instead
        if session_file is None:
            session_file = self.session_file

        # Open file for writing
        with open(session_file, 'w') as fp:
            # Write JSON to file
            session_cookies = self.getSession()
            json.dump(session_cookies, fp)

    def set_typing(self, status):
        """Set typing status

        Args:
          status (bool): Indicates whether to set typing on or off
        """
        self.setTypingStatus(
            TypingStatus.TYPING if status else TypingStatus.STOPPED
        )

    def send_image_url(self, url):
        """Send image from URL"""
        self.sendRemoteFiles([url])

    def get_thread_emoji(self):
        """Get current emoji"""
        time.sleep(1)
        thread = self.fetchThreadInfo(self.thread_id)

        if self.thread_id not in thread:
            return None

        return thread[self.thread_id].emoji

    def set_thread_emoji(self, emoji):
        """Set thread emoji"""
        time.sleep(1)
        self.changeThreadEmoji(emoji)

    def send_chat_message(self, chatmessage):
        """Sends a ChatMessage instance"""
        time.sleep(2)

        # Iterate through single message texts
        for text in chatmessage.texts:
            # Single text is chat action
            if isinstance(text, ChatAction):
                text.exec()  # Execute chat action
                continue

            # ChatMessage is text or emoji message
            if isinstance(chatmessage, (TextMessage, EmojiMessage)):
                self.set_typing(True)
                time.sleep(len(text) * 0.3)
                self.set_typing(False)
                self.send(Message(text=text))

            # ChatMessage is an image message
            if isinstance(chatmessage, ImageMessage):
                self.send_image_url(text)
                time.sleep(2)

            time.sleep(2)
