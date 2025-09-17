#!/usr/bin/env python3.11
"""
Fun Fact Generator API
Deployable to Azure Web Services
Uses the Useless Facts API to serve random fun facts
"""

from flask import Flask, jsonify, render_template
import requests
import os
from typing import Optional, Dict

app = Flask(__name__)

# Configuration
app.config['API_URL'] = "https://uselessfacts.jsph.pl/api/v2/facts/random"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


def get_random_fact() -> Optional[Dict]:
    """
    Fetch a random fun fact from the API
    Returns: Fact data or None if error occurs
    """
    headers = {
        'User-Agent': 'FunFactGenerator/1.0 (Python 3.11)',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(
            app.config['API_URL'],
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


@app.route('/')
def home():
    """Home page with HTML interface"""
    return render_template('index.html')


@app.route('/api/fact')
def api_fact():
    """API endpoint that returns a random fact as JSON"""
    fact_data = get_random_fact()

    if fact_data:
        return jsonify({
            'fact': fact_data.get('text', 'No fact text found'),
            'source': fact_data.get('source', 'Unknown'),
            'permalink': fact_data.get('permalink', ''),
            'status': 'success'
        })
    else:
        return jsonify({
            'error': 'Failed to fetch fact from upstream API',
            'status': 'error'
        }), 500


@app.route('/api/fact/text')
def api_fact_text():
    """API endpoint that returns just the fact text"""
    fact_data = get_random_fact()

    if fact_data and 'text' in fact_data:
        return fact_data['text']
    else:
        return "Failed to fetch fact", 500


if __name__ == '__main__':
    # Get port from environment variable or default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)