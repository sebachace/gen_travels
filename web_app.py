from flask import Flask, render_template, request, jsonify
from agent import GeminiAgent
import os

app = Flask(__name__)
agent = None

# Ensure required directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("tools", exist_ok=True)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to process queries through the Gemini agent"""
    global agent
    
    # Get the prompt from the request
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Process with agent
    try:
        if agent is None:
            agent = GeminiAgent()
        
        result = agent.process_query(prompt)
        
        response_data = {
            'response': result['response'],
            'tool_used': result.get('tool_used'),
            'tool_details': None
        }
        
        # Add tool-specific details if applicable
        if result.get('tool_used') == 'poi_search' and result.get('tool_result'):
            poi_result = result['tool_result']
            city_name = result.get('city_name', 'the location')
            
            response_data['tool_details'] = {
                'found': poi_result.get('found', False),
                'city_name': city_name,
                'city_coordinates': poi_result.get('city_coordinates'),
                'nearby_pois': poi_result.get('nearby_pois', []),
                'message': poi_result.get('message')
            }
            
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models')
def models():
    """API endpoint to get available models"""
    global agent
    
    try:
        if agent is None:
            agent = GeminiAgent()
        
        models = agent.gemini.get_model_info()
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tools')
def tools():
    """API endpoint to get available tools"""
    global agent
    
    try:
        if agent is None:
            agent = GeminiAgent()
        
        tool_names = list(agent.tools.keys())
        return jsonify({'tools': tool_names})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize Gemini agent
    try:
        agent = GeminiAgent()
        print("Connected to Gemini API successfully.")
        print(f"Available models: {agent.gemini.get_model_info()}")
        print("Loaded agent with tools: poi_search")  # Updated tool name
    except Exception as e:
        print(f"Warning: {str(e)}")
        print("Will attempt to initialize agent when first request is made.")
    
    # Run the Flask app
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from agent import GeminiAgent
import os

app = Flask(__name__)
agent = None

# Ensure required directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("tools", exist_ok=True)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to process queries through the Gemini agent"""
    global agent
    
    # Get the prompt from the request
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Process with agent
    try:
        if agent is None:
            agent = GeminiAgent()
        
        result = agent.process_query(prompt)
        
        response_data = {
            'response': result['response'],
            'tool_used': result.get('tool_used'),
            'tool_details': None
        }
        
        # Add tool-specific details if applicable
        if result.get('tool_used') == 'city_search' and result.get('tool_result'):
            city_result = result['tool_result']
            response_data['tool_details'] = {
                'found': city_result.get('found', False),
                'exact_match': city_result.get('exact_match'),
                'similar_matches': city_result.get('similar_matches', []),
                'message': city_result.get('message')
            }
            
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models')
def models():
    """API endpoint to get available models"""
    global agent
    
    try:
        if agent is None:
            agent = GeminiAgent()
        
        models = agent.gemini.get_model_info()
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tools')
def tools():
    """API endpoint to get available tools"""
    global agent
    
    try:
        if agent is None:
            agent = GeminiAgent()
        
        tool_names = list(agent.tools.keys())
        return jsonify({'tools': tool_names})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize Gemini client
    try:
        client = GeminiClient()
        print("Connected to Gemini API successfully.")
    except Exception as e:
        print(f"Warning: {str(e)}")
        print("Will attempt to initialize client when first request is made.")
    
    # Run the Flask app
    app.run(debug=True)