#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
   IMAGE SEARCH - imagesearch.py

    Allows for easy use of both Giphy and Google Image searches
"""


# Dependencies
import random
import giphy_client
import requests
import googleapiclient
from google_images_search import GoogleImagesSearch
# Local dependencies
from .types import hydra_image_engines, tcolors


class ImageSearch:
    """Allow for easy use of both Giphy and Google Image searches

    Args:
      gis_api_key (str): Google Image Search API key (None)
      gis_project_cx (str): Google Image Search project CX (None)
      gis_search_phrases (list): Pool of GIS search phrases (empty)
      giphy_api_key (str): Giphy API key
      giphy_search_phrases (list): Pool of Giphy search phrases (empty)
    """
    giphy = None
    giphy_api_key = None
    giphy_search_phrases = None
    gis = None
    gis_search_phrases = None

    def __init__(self,
                 gis_api_key=None, gis_project_cx=None, gis_search_phrases=[],
                 giphy_api_key=None, giphy_search_phrases=[]):
        # GIS API key and project CX were given
        if gis_api_key and gis_project_cx:
            self.gis = GoogleImagesSearch(gis_api_key, gis_project_cx)
            # ENABLE GOOGLE IMAGE SEARCH "START" PARAMETER
            self.gis._google_custom_search._search_params_keys['start'] = 0

        self.gis_search_phrases = gis_search_phrases

        # Giphy API key was provided
        if giphy_api_key:
            self.giphy = giphy_client.DefaultApi()
            self.giphy_api_key = giphy_api_key

        self.giphy_search_phrases = giphy_search_phrases


    def can_use_gis(self):
        """Indicates whether Google Image Search
        is available"""
        return bool(self.gis and self.gis_search_phrases)

    def can_use_giphy(self):
        """Indicates whether Giphy is available"""
        return bool(self.giphy and self.giphy_search_phrases)

    def is_ready(self):
        """Indicates as bool whether values required for Image Search
        to work were properly set"""
        return (self.can_use_gis() or self.can_use_giphy())

    # This is the actual method used for performing requests  to
    # seach online for an image
    def get_random_url(self, gis_giphy_chance=None):
        """Get random image URL

        Args:
          gis_giphy_chance (float):
            Chance of either using Google Image Search or Giphy for
            getting an image (defaults to random choice)
            The closer the number is to 0, the higher the chance for GIS gets
            The closer the number is to 1, the higher the chance for Giphy will be
            Example: 0 = 100% GIS/0% Giphy; 0.2 = 80% GIS/20% Giphy

        Returns:
            url (str): An image URL
        """
        # Use random bit if no specific chance for either Giphy or
        # GIS was given
        if gis_giphy_chance is None:
            gis_giphy_chance = random.getrandbits(1)

        image_url = None

        # Choose either Giphy or GIS based off chance
        image_engine = hydra_image_engines.GIPHY
        if random.uniform(0, 1) < 1 - gis_giphy_chance:
            image_engine = hydra_image_engines.GIS
        if (image_engine is hydra_image_engines.GIS and not self.can_use_gis()):
            image_engine = hydra_image_engines.GIPHY

            print(tcolors.FAIL
                  + 'GIS wasn\'t properly configured, therefore '
                  + 'switching to Giphy now...'
                  + tcolors.ENDC)
        elif (image_engine is hydra_image_engines.GIPHY and not self.can_use_giphy()):
            image_engine = hydra_image_engines.GIS

            print(tcolors.FAIL
                  + 'Giphy wasn\'t properly configured, therefore '
                  + 'switching to GIS now...'
                  + tcolors.ENDC)

        # Select random search query
        search_query_used = None

        # Perform image search
        while image_url is None:
            if image_engine is hydra_image_engines.GIPHY:
                try:
                    search_phrases = self.giphy_search_phrases
                    search_query_used = random.choice(search_phrases)

                    # Search Endpoint
                    giphy_response = self.giphy.gifs_search_get(
                        self.giphy_api_key,
                        search_query_used,
                        limit=100,
                        offset=random.randint(0, 100),
                    )

                    # No images could be retrieved, therefore skip to
                    # next iteration
                    if not len(giphy_response.data):
                        continue

                    # Choose random image based of response
                    found_giphy = random.choice(giphy_response.data)
                    # Set image URL to downsized version
                    image_url = found_giphy.images.downsized.url

                # Continue to next iteration if Giphy ApiException occured
                except giphy_client.rest.ApiException:
                    continue
            else:
                try:
                    search_phrases = self.gis_search_phrases
                    search_query_used = random.choice(search_phrases)

                    self.gis.search(search_params={
                        'q': search_query_used,
                        'num': 10,
                        'start': random.randint(0, 90)
                    })

                    search_results = self.gis.results()

                    # No image could be found
                    if not len(search_results):
                        continue

                    # Set image URL randomly based on results
                    image_url = random.choice(search_results).url

                # Continue to next iteration if common request exceptions
                # occured
                except (requests.exceptions.ReadTimeout,
                        requests.exceptions.ConnectionError):
                    continue

                # GIS HttpError exception normally indicated reaching of
                # maximum search queries per day
                except googleapiclient.errors.HttpError:
                    # Switch to Giphy instead
                    image_engine = hydra_image_engines.GIPHY

                    print(tcolors.FAIL
                          + 'GIS returned HTTP error, probably because '
                          + 'daily request limit has been reached. '
                          + 'Therefore switching to Giphy now...'
                          + tcolors.ENDC)

        # Get image engine name as string
        # TODO: Improve model logic to provide for this there instead
        image_engine_name = 'Giphy'
        if image_engine is hydra_image_engines.GIS:
            image_engine_name = 'Google Image Search'

        # Return tuple of found URL, plus useful information
        return image_url, search_query_used, image_engine_name
