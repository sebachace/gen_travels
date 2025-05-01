"""
Gemini Agent Module

This module implements an agentic interface for Gemini that can use tools
to perform actions beyond simple text generation.
"""
import re
import os
from typing import Dict, List, Optional, Any, Union
from gemini_client import GeminiClient
from tools.poi_search import PointOfInterestTool  # Updated import path

class GeminiAgent:
    """
    An agent that uses Gemini AI to process queries and can use tools
    to perform external actions.
    """
    
    def __init__(self):
        """Initialize the Gemini agent with available tools."""
        self.gemini = GeminiClient()
        self.tools = {
            "poi_search": PointOfInterestTool()  # Consistent tool name
        }
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query, detecting if tools need to be used and
        generating an appropriate response.
        
        Args:
            query: The user's input query
            
        Returns:
            Dict containing the processed response
        """
        # First, determine if we need to use a tool
        tool_result = self._detect_and_use_tool(query)
        
        # If a tool was used, incorporate the tool's output into the response
        if tool_result and tool_result.get("tool_used"):
            # Generate a response that includes the tool's output
            enhanced_prompt = self._create_enhanced_prompt(query, tool_result)
            response_text = self.gemini.generate_text(enhanced_prompt)
            
            return {
                "response": response_text,
                "tool_used": tool_result.get("tool_used"),
                "tool_result": tool_result.get("result")
            }
        
        # If no tool was needed, just use Gemini directly
        response_text = self.gemini.generate_text(query)
        return {
            "response": response_text,
            "tool_used": None,
            "tool_result": None
        }
    
    def _detect_and_use_tool(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Detect if a tool should be used based on the query
        and use it if appropriate.
        
        Args:
            query: The user's input query
            
        Returns:
            Dict with tool results or None if no tool was used
        """
        # Check for POI search queries
        poi_patterns = [
            r"(?:what|which|show|find|search for|are there any) (?:points of interest|attractions|places to visit|sights|landmarks|locations) (?:in|near|around) ([A-Za-z\s]+)",
            r"(?:what's|what is|what are) (?:near|around|in) ([A-Za-z\s]+)",
            r"(?:places|attractions|sights|landmarks|locations) (?:to see|to visit|of interest) (?:in|near|around) ([A-Za-z\s]+)",
            r"(?:can you find|show me|tell me about) (?:things to do|places to go|attractions|points of interest) (?:in|near|around) ([A-Za-z\s]+)",
            r"(?:what|where) (?:can i|should i|to) (?:see|visit|do) (?:in|near|around) ([A-Za-z\s]+)",
            r"(?:i'm|i am) (?:visiting|going to|in) ([A-Za-z\s]+)",
            r"(?:tourist|travel|visit) (?:attractions|spots|destinations) (?:in|near|around) ([A-Za-z\s]+)",
            r"(?:what is|what's) (?:in|near) ([A-Za-z\s]+)"
        ]
        
        # Try each pattern
        city_name = None
        for pattern in poi_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                city_name = match.group(1).strip()
                break
        
        # If no match found yet, try a simpler pattern that just extracts city names
        if not city_name:
            # List of common city names to check directly
            common_cities = [
                "Paris", "New York", "Rome", "London", "Tokyo", "Sydney", 
                "Los Angeles", "Berlin", "Madrid", "Moscow", "Beijing", 
                "Cairo", "Rio de Janeiro", "Toronto", "Dubai", "Singapore", 
                "Istanbul", "Mumbai", "Chicago", "Bangkok"
            ]
            
            # Check if any common city is mentioned in the query
            for city in common_cities:
                if re.search(r'\b' + re.escape(city) + r'\b', query, re.IGNORECASE):
                    city_name = city
                    break
        
        # If we found a potential city name
        if city_name:
            # Don't process very short names (likely false positives)
            if len(city_name) <= 2:
                return None
                
            # Use the POI search tool
            poi_tool = self.tools["poi_search"]
            result = poi_tool.find_nearby_pois(city_name)  # Using correct method name
            
            return {
                "tool_used": "poi_search",  # Consistent tool name
                "city_name": city_name,
                "result": result
            }
        
        # No tool needed
        return None
    
    def _create_enhanced_prompt(self, original_query: str, tool_result: Dict[str, Any]) -> str:
        """
        Create an enhanced prompt that includes tool output for Gemini.
        
        Args:
            original_query: The user's original query
            tool_result: The result from using a tool
            
        Returns:
            An enhanced prompt for Gemini
        """
        if tool_result["tool_used"] == "poi_search":  # Consistent tool name
            tool_output = tool_result["result"]["message"]
            
            # Create a detailed prompt for Gemini
            return (
                f"The user asked: '{original_query}'\n\n"
                f"I searched for points of interest and found: \n{tool_output}\n\n"
                f"Please create a helpful, conversational response that incorporates this information. "
                f"Highlight the most interesting attractions if there are many options, and provide some "
                f"brief context about the city and what makes these attractions special. Keep your response "
                f"friendly and enthusiastic."
            )
        
        # Default case if unknown tool
        return original_query