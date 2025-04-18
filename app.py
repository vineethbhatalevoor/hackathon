from flask import Flask, request, jsonify
import os
import requests  # For Groq API interactions

app = Flask(__name__)

# Default Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Groq-Powered News Summarizer!'})

# Favicon Handler
@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

# Text Summarization Route
@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        text = data.get('text')
        groq_api_key = os.environ.get('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({'error': 'API key is missing. Set the GROQ_API_KEY environment variable.'}), 400
        
        # Correct indentation and remove extra parentheses
        response = requests.post(
            'https://api.groq.com/v1/summarize-text',  # Replace with the correct endpoint
            json={'text': text},
            headers={'Authorization': f"Bearer {groq_api_key}"}
        )

        if response.status_code == 200:
            summary = response.json().get('summary', 'No summary available.')
            return jsonify({'summary': summary})
        else:
            return jsonify({'error': 'Groq API error.', 'details': response.json()}), response.status_code
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)