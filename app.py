from agent import GeminiAgent
import os

def ensure_directories():
    """Ensure required directories exist"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("tools", exist_ok=True)

def main():
    print("Welcome to the Gemini AI Agent CLI Application")
    print("---------------------------------------------")
    print("This agent can help you find points of interest near cities around the world!")
    print("Try asking: 'What are some attractions in Paris?' or 'What can I visit in Tokyo?'")
    
    # Ensure directories exist
    ensure_directories()
    
    # Initialize the Gemini agent
    try:
        agent = GeminiAgent()
        print("Connected to Gemini API successfully.")
        print(f"Available models: {agent.gemini.get_model_info()}")
        print("Loaded agent with tools: poi_search")
    except Exception as e:
        print(f"Error initializing Gemini agent: {str(e)}")
        return
    
    # Main interaction loop
    while True:
        print("\nEnter your prompt (or 'quit' to exit):")
        user_input = input("> ")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Thank you for using the Gemini AI application. Goodbye!")
            break
        
        if not user_input.strip():
            print("Please enter a valid prompt.")
            continue
        
        print("\nProcessing query...\n")
        
        # Process query with the agent
        result = agent.process_query(user_input)
        
        # Display tool usage if applicable
        if result.get("tool_used"):
            print(f"🔍 Agent used tool: {result['tool_used']}")
            
            if result["tool_used"] == "poi_search" and result.get("tool_result"):
                poi_result = result["tool_result"]
                if poi_result.get("found", False):
                    city_name = result.get("city_name", "the location")
                    if poi_result.get("city_coordinates"):
                        lat, lon = poi_result["city_coordinates"]
                        print(f"📍 Located {city_name} at coordinates: {lat:.4f}, {lon:.4f}")
                    
                    if poi_result.get("nearby_pois"):
                        print(f"🏛️  Found {len(poi_result['nearby_pois'])} points of interest within 2km:")
                        for i, poi in enumerate(poi_result["nearby_pois"], 1):
                            print(f"   {i}. {poi['name']} ({poi['distance_km']} km)")
                    else:
                        print(f"❌ No points of interest found near {city_name}.")
            
            print()  # Extra line for readability
        
        # Display the response
        print("Gemini's response:")
        print("-----------------")
        print(result["response"])
        print("-----------------")
        
from agent import GeminiAgent
import os

def ensure_directories():
    """Ensure required directories exist"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("tools", exist_ok=True)

def main():
    print("Welcome to the Gemini AI Agent CLI Application")
    print("---------------------------------------------")
    
    # Ensure directories exist
    ensure_directories()
    
    # Initialize the Gemini agent
    try:
        agent = GeminiAgent()
        print("Connected to Gemini API successfully.")
        print(f"Available models: {agent.gemini.get_model_info()}")
        print("Loaded agent with tools: poi_search")
    except Exception as e:
        print(f"Error initializing Gemini agent: {str(e)}")
        return
    
    # Main interaction loop
    while True:
        print("\nEnter your prompt (or 'quit' to exit):")
        user_input = input("> ")
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Thank you for using the Gemini AI application. Goodbye!")
            break
        
        if not user_input.strip():
            print("Please enter a valid prompt.")
            continue
        
        print("\nProcessing query...\n")
        
        # Process query with the agent
        result = agent.process_query(user_input)
        
        # Display tool usage if applicable
        if result.get("tool_used"):
            print(f"[Agent used tool: {result['tool_used']}]")
            if result["tool_used"] == "city_search" and result.get("tool_result"):
                city_result = result["tool_result"]
                if city_result.get("found", False):
                    print(f"[Found city: {city_result.get('exact_match')}]")
                elif city_result.get("similar_matches"):
                    print(f"[Similar cities: {', '.join(city_result.get('similar_matches'))}]")
        
        # Display the response
        print("\nGemini's response:")
        print("-----------------")
        print(result["response"])
        print("-----------------")

if __name__ == "__main__":
    main()