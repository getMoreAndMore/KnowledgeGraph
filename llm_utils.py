import os
import json
import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage

# Initialize session state for API key, supplier and temperature
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'current_supplier' not in st.session_state:
    st.session_state.current_supplier = 'deepseek'  # Default to ds
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.1  # Default temperature

# Azure OpenAI Configuration
AZURE_CONFIGS = {
    "xxx"
}

def call_llm(system_msg, user_msg, supplier=st.session_state.current_supplier):
    st.info(system_msg, icon="🔥")
    st.info(user_msg, icon="🔥")
    if not st.session_state.api_key:
        raise ValueError(f"{supplier.upper()} API Key not set. Please enter it in the sidebar.")

    try:
        if supplier == "azure":
            os.environ["AZURE_OPENAI_API_KEY"] = st.session_state.api_key
            os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_CONFIGS["base_url"]
            llm = AzureChatOpenAI(
                openai_api_version=AZURE_CONFIGS['api_version'],
                azure_endpoint=AZURE_CONFIGS["base_url"],
                azure_deployment=AZURE_CONFIGS["model_deployment"],
                model=AZURE_CONFIGS["model_name"],
                validate_base_url=False,
                temperature=st.session_state.temperature,  # Use temperature from session state
                max_tokens=None,
                timeout=None,
                max_retries=2
            )

            messages = [
                ('system', system_msg),
                ('human', user_msg)
            ]
        elif supplier == "zhipu":
            llm = ChatZhipuAI(
                model='glm-4-flash',
                temperature=st.session_state.temperature,  # Use temperature from session state
                api_key=st.session_state.api_key
            )
            
            messages = [
                SystemMessage(system_msg),
                HumanMessage(user_msg)
            ]
        elif supplier == "deepseek":
            os.environ["DEEPSEEK_API_KEY"] = st.session_state.api_key
            llm = ChatDeepSeek(
                model="deepseek-chat",
                temperature=st.session_state.temperature,
            )
            messages = [
                SystemMessage(system_msg),
                HumanMessage(user_msg)
            ]
        else:
            raise ValueError(f'Invalid LLM supplier: {supplier}')

        # Call LLM
        res = llm.invoke(messages)
        if not res or not res.content:
            raise ValueError("API returned empty response")
            
        output = res.content
        # output = output[7:]
        output = output.strip()
        if output.startswith("```json"):
            output = output[len("```json"):].strip()
        if output.endswith("```"):
            output = output[:-3].strip()
        # Validate JSON format and structure
        try:
            data = json.loads(output)
        except json.JSONDecodeError as e:
            st.write("JSON 解析失败：", e)
        if not isinstance(data, dict):
            raise ValueError("API response is not a valid JSON object")
        
        if 'nodes' not in data or 'edges' not in data:
            raise ValueError("API response missing required 'nodes' or 'edges' fields")
            
        if not isinstance(data['nodes'], list) or not isinstance(data['edges'], list):
            raise ValueError("'nodes' and 'edges' must be arrays")
            
        if len(data['nodes']) < 3:
            raise ValueError("At least 3 nodes are required")
            
        # Print output for debugging
        st.write("Extraction result:")
        st.info(output, icon="🎯")

        return output
            
    except json.JSONDecodeError as je:
        st.error(f"Invalid JSON format in API response: {str(je)}")
        return '{"nodes": [], "edges": []}'
    except ValueError as ve:
        st.error(str(ve))
        return '{"nodes": [], "edges": []}'
    except Exception as e:
        st.error(f"API call error: {str(e)}")
        return '{"nodes": [], "edges": []}' 