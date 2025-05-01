import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        if api_key == "your_api_key_here":
            raise ValueError("Please replace 'your_api_key_here' in the .env file with your actual Gemini API key")
        
        print(f"Initializing Gemini client with API key: {api_key[:4]}...{api_key[-4:]}")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        print("Fetching available models...")
        # Get available models and select an appropriate one
        self.available_models = self.list_available_models()
        
        if not self.available_models:
            raise ValueError("No models returned from the API. Please check your API key and access.")
            
        print(f"Found {len(self.available_models)} models.")
        self.model = self.get_default_model()
        print(f"Initialization complete. Ready to use Gemini.")
    
    def generate_text(self, prompt, max_tokens=1024, temperature=0.7):
        """
        Generate text using the Gemini API
        
        Args:
            prompt (str): The prompt to send to Gemini
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Controls randomness (0.0 to 1.0)
            
        Returns:
            str: Generated response text
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            return response.text
        except Exception as e:
            error_msg = str(e)
            
            # Check for common errors and provide more helpful messages
            if "404" in error_msg and "not found" in error_msg:
                # Try to refresh the model if there's a model issue
                try:
                    print("Attempting to refresh model selection...")
                    self.model = self.get_default_model()
                    # Try again with the new model
                    response = self.model.generate_content(
                        prompt,
                        generation_config={
                            "max_output_tokens": max_tokens,
                            "temperature": temperature
                        }
                    )
                    return response.text
                except Exception as retry_error:
                    return (f"Error: Could not find a working Gemini model. Please check:\n"
                            f"1. Your API key is correct and has access to Gemini\n"
                            f"2. You're using the correct API version\n"
                            f"Original error: {error_msg}\n"
                            f"Retry error: {str(retry_error)}")
            elif "api_key" in error_msg.lower():
                return "Error: Invalid API key. Please check your GEMINI_API_KEY in the .env file."
            else:
                return f"Error generating response: {error_msg}"
    
    def list_available_models(self):
        """Lists all available models from the API"""
        try:
            models = genai.list_models()
            # Filter for generative models only
            return [model for model in models]
        except Exception as e:
            print(f"Error retrieving models: {str(e)}")
            return []
    
    def get_default_model(self):
        """Get the most appropriate default model based on availability"""
        gemini_model_names = [
            "gemini-1.5-flash",
            "gemini-1.0-flash",
            "gemini-flash"
        ]
        
        # Check which model names are available
        available_model_names = [model.name for model in self.available_models]
        
        # Print available models for debugging
        print(f"Available models: {available_model_names}")
        
        # Find the first matching model name
        for model_name in gemini_model_names:
            for available_name in available_model_names:
                if model_name in available_name:
                    print(f"Selected model: {available_name}")
                    return genai.GenerativeModel(available_name)
        
        # If no specific match is found, try to find any gemini model
        for available_name in available_model_names:
            if "gemini" in available_name.lower():
                print(f"Selected model: {available_name}")
                return genai.GenerativeModel(available_name)
        
        # If no gemini model is found, raise an error
        raise ValueError("No Gemini models available. Please check your API key and access.")
    
    def get_model_info(self):
        """Returns information about available models"""
        try:
            return [model.name for model in self.available_models]
        except Exception as e:
            return f"Error retrieving model information: {str(e)}"