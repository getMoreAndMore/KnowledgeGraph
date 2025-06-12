import streamlit as st
import json
from llm_utils import call_llm

def detect_language(text):
    """Detect the primary language of the input text"""
    # Simple language detection based on character sets
    chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
    english_chars = len([c for c in text if c.isascii() and c.isalpha()])
    
    return 'chinese' if chinese_chars > english_chars else 'english'

def get_system_prompt(language):
    """Get system prompt based on language"""
    if language == '中文':
        return """You are a professional text analysis assistant. Please analyze the input text and extract key concepts and their relationships.

You must output ONLY a JSON object in the following format, with NO additional text or explanation:

{
    "nodes": [
        {
            "id": "1",           // Must be a unique string
            "label": "概念1",     // Concept name in Chinese
            "group": "类别1"      // Category in Chinese
        }
    ],
    "edges": [
        {
            "from": "1",         // Must match an existing node id
            "to": "2",           // Must match an existing node id
            "label": "包含"       // Relationship description in Chinese
        }
    ]
}

Requirements:
1. Output ONLY the JSON object, no other text
2. All node IDs must be unique strings
3. All 'from' and 'to' in edges must reference existing node IDs
4. All labels and descriptions MUST be in Chinese
5. The output must be valid JSON format
6. Extract at least 3 key concepts and their relationships
7. Group similar concepts under the same category
8. Use natural and idiomatic Chinese expressions
9. Ensure relationship descriptions are clear and meaningful

DO NOT include any explanations or markdown formatting in the output."""
    else:
        return """You are a professional text analysis assistant. Please analyze the input text and extract key concepts and their relationships.

You must output ONLY a JSON object in the following format, with NO additional text or explanation:

{
    "nodes": [
        {
            "id": "1",           // Must be a unique string
            "label": "Concept1", // Concept name in English
            "group": "Group1"    // Category in English
        }
    ],
    "edges": [
        {
            "from": "1",         // Must match an existing node id
            "to": "2",           // Must match an existing node id
            "label": "contains"  // Relationship description in English
        }
    ]
}

Requirements:
1. Output ONLY the JSON object, no other text
2. All node IDs must be unique strings
3. All 'from' and 'to' in edges must reference existing node IDs
4. All labels and descriptions MUST be in English
5. The output must be valid JSON format
6. Extract at least 3 key concepts and their relationships
7. Group similar concepts under the same category
8. Use natural and idiomatic English expressions
9. Ensure relationship descriptions are clear and meaningful

DO NOT include any explanations or markdown formatting in the output."""

def generate_graph_data(text,model,language):
    """Call OpenAI API to generate graph nodes and edges data"""
    
    # Detect the language of input text
    # language = detect_language(text)
    
    # Get appropriate system prompt based on language
    system_msg = get_system_prompt(language)
    
    user_msg = "Please analyze the following text and generate relationship graph data:\n" + text
    
    try:
        # Call OpenAI API
        output = call_llm(system_msg, user_msg,model)
        if not output:
            raise ValueError("API returned empty response")
            
        # Clean potential extra content from output
        output = output.strip()
        if output.startswith("```json"):
            output = output[7:]
        if output.endswith("```"):
            output = output[:-3]
        output = output.strip()
        
        # Parse JSON data
        result = json.loads(output)
        
        # Validate data format
        if not isinstance(result, dict):
            raise ValueError("Response is not a JSON object")
        if 'nodes' not in result or 'edges' not in result:
            raise ValueError("Missing required 'nodes' or 'edges' fields")
        if not isinstance(result['nodes'], list) or not isinstance(result['edges'], list):
            raise ValueError("'nodes' or 'edges' is not an array")
        if len(result['nodes']) < 3:
            raise ValueError("At least 3 nodes are required")
            
        # Validate nodes and edges data
        node_ids = set()
        groups = set()
        for node in result['nodes']:
            if not all(k in node for k in ('id', 'label', 'group')):
                raise ValueError("Invalid node format - missing required fields")
            if not all(isinstance(node[k], str) for k in ('id', 'label', 'group')):
                raise ValueError("Node fields must be strings")
            if str(node['id']) in node_ids:
                raise ValueError(f"Duplicate node ID found: {node['id']}")
            node_ids.add(str(node['id']))
            groups.add(node['group'])
            
        if len(groups) < 2:
            raise ValueError("Nodes should be categorized into at least 2 groups")
            
        for edge in result['edges']:
            if not all(k in edge for k in ('from', 'to', 'label')):
                raise ValueError("Invalid edge format - missing required fields")
            if not all(isinstance(edge[k], str) for k in ('from', 'to', 'label')):
                raise ValueError("Edge fields must be strings")
            if str(edge['from']) not in node_ids:
                raise ValueError(f"Edge references non-existent source node: {edge['from']}")
            if str(edge['to']) not in node_ids:
                raise ValueError(f"Edge references non-existent target node: {edge['to']}")
        
        return result['nodes'], result['edges']
        
    except json.JSONDecodeError as je:
        st.error(f"JSON parsing error: {str(je)}\nActual output: {output}")
        return [], []
    except Exception as e:
        st.error(f"Error generating graph data: {str(e)}")
        return [], [] 