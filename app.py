import streamlit as st
import json

from streamlit import text_input

from utils import generate_graph_data
from llm_utils import call_llm
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(page_title="知识图谱生成", layout="wide")
# Set page title
st.title("知识图谱生成器")

# Add description
st.write("请输入用于生成知识图谱的文本")

# Add text input area
text_input = st.text_area("输入文本", height=200)

# Initialize session state
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = None
if 'agraph_config' not in st.session_state:
    st.session_state.agraph_config = None
if 'graph_ready' not in st.session_state:
    st.session_state.graph_ready = False

# Initialize session state for API key, supplier and temperature
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'current_supplier' not in st.session_state:
    st.session_state.current_supplier = 'deepseek'  # Default to zhipu
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.1  # Default temperature

def prepare_graph_visualization(nodes_data, edges_data):
    """Prepare graph visualization data and config"""
    # Convert to agraph format nodes and edges
    nodes = [
        Node(
            id=str(node['id']),  # Ensure id is string
            label=str(node['label']),
            size=25,
            color=f"#{hash(str(node['group'])) % 0xFFFFFF:06x}"
        ) for node in nodes_data
    ]
    
    edges = [
        Edge(
            source=str(edge['from']),  # Ensure source is string
            target=str(edge['to']),    # Ensure target is string
            label=str(edge['label'])
        ) for edge in edges_data
    ]

    # Configure graph display
    config = Config(
        width=1000,
        height=500,
        directed=True,
        physics=True,
        hierarchical=True,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=True,
        node={'labelProperty': 'label'},
        link={'labelProperty': 'label', 'renderLabel': True}
    )
    
    return nodes, edges, config

# Add extract button
def extract_knowledge():
    if not text_input:
        st.warning("请先输入文本，不输入文本下面就会报错哦~")
    else:
        # with st.spinner('Extracting knowledge graph...'):
        try:
            # Call OpenAI API to generate nodes and edges
            nodes_data, edges_data = generate_graph_data(text_input,st.session_state.current_supplier,st.session_state.language)
            
            if not nodes_data or not edges_data:
                st.warning("Failed to extract valid knowledge graph. Please modify your input text.")
                st.session_state.graph_ready = False
            else:
                # Store graph data in session state
                st.session_state.graph_data = (nodes_data, edges_data)
                # Prepare visualization data
                nodes, edges, config = prepare_graph_visualization(nodes_data, edges_data)
                st.session_state.agraph_config = {
                    'nodes': nodes,
                    'edges': edges,
                    'config': config
                }
                st.session_state.graph_ready = True
                # st.success("Knowledge extraction completed! Click 'Show Graph' to view the result.")
                
        except Exception as e:
            st.error(f"Error during knowledge extraction: {str(e)}")
            st.session_state.graph_ready = False
    return nodes_data, edges_data


if st.button("生成知识图谱"):
    with st.spinner('正在努力阅读中...'):
        nodes_data, edges_data = extract_knowledge()

# if st.button("Show Graph") or st.session_state.graph_ready:
    st.write("图片展示中...")
    with st.expander("Graph", expanded=True):
        st.write("Nodes:")
        st.write(nodes_data)
        st.write("Edges:")
        st.write(edges_data)
        # st.write(st.session_state.agraph_config['nodes'])
        # st.write(st.session_state.agraph_config['edges'])
        # st.write(st.session_state.agraph_config['config'])
    try:
        # Display graph using stored configuration
        return_value = agraph(
            nodes=st.session_state.agraph_config['nodes'],
            edges=st.session_state.agraph_config['edges'],
            config=st.session_state.agraph_config['config']
        )
            
    except Exception as e:
        st.error(f"Error displaying knowledge graph: {str(e)}")

if not st.session_state.graph_ready:
    st.warning("已经准备好给你画图了！")

def setup_sidebar():
    """Setup sidebar for API key inputs"""
    with st.sidebar:
        st.header("API 配置")

        # Add supplier selection dropdown
        supplier = st.selectbox(
            "请选择你要使用的模型",
            options=["zhipu", "azure" ,"deepseek"],
            index=2,  # Default to zhipu
            key="supplier_select"
        )
        st.session_state.current_supplier = supplier

        # Select output language

        language = st.selectbox(
            "选择您要输出的语言",
            index=0, key="language_select",
            options=["中文", "English" ],
            help="自主选择图谱中文字的语言"
        )
        st.session_state.language = language
        
        # Add temperature slider
        temperature = st.slider(
            "温度",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="温度越高随机性越高，反之则越保守。"
        )
        st.session_state.temperature = temperature



        st.markdown("---")  # Add a divider
        
        # Single API key input
        api_key = st.text_input(
            f"请输入 {supplier.upper()} 的 API Key",
            type="password",
            value=st.session_state.api_key,
            key="api_key_input"
        )
        if api_key:
            st.session_state.api_key = api_key

def main():
    setup_sidebar()
    # Rest of your application code...

if __name__ == "__main__":
    main()


