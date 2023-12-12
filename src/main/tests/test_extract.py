#!/usr/bin/env python3
import unittest
import nba_api
from get_data import ExtractAndSaveNbaData
from nba_api.stats.endpoints import commonallplayers 
import json

from unittest.mock import Mock, patch, MagicMock


def test_nba():
    
    with patch('nba_api.stats.endpoints.commonallplayers.CommonAllPlayers.get_json', return_value = '{"key": "value"}') as nba_api_players:
        ExtractAndSaveNbaData("2021").get_players()

        


