#!/usr/bin/env python3

from flask import Flask, jsonify
from ..analytics.analytics_interface import AnalyticsInterface

app = Flask(__name__)

# Endpoint to get all books
@app.route('/api/overall_player_stats', methods=['GET'])
def get_overall_player_stats():
    df = AnalyticsInterface.overall_player_season_stats()
    df_json = df.to_json(orient='records')
    return df_json

if __name__ == '__main__':
    app.run(debug=True)