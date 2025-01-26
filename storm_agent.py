import logging
from qdrant_client import QdrantClient
import streamlit as st
from knowledge_storm.lm import AzureOpenAIModel, OpenAIModel
from knowledge_storm.storm_wiki.engine import STORMWikiLMConfigs, STORMWikiRunner, STORMWikiRunnerArguments
from knowledge_storm.utils import QdrantVectorStoreManager
from knowledge_storm.rm import VectorRM

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_lm_configs():
    """Initializes the language model configurations."""
    openai_kwargs = {
        'api_key': st.secrets["OPENAI_API_KEY"],
        'temperature': 1.0,
        'top_p': 0.9,
    }

    ModelClass = OpenAIModel if st.secrets['OPENAI_API_TYPE'] == 'openai' else AzureOpenAIModel
    model_name_map = {
        'conv_simulator': 'gpt-3.5-turbo' if st.secrets['OPENAI_API_TYPE'] == 'openai' else 'gpt-35-turbo',
        'outline_gen': 'gpt-4o',
        'article_gen': 'gpt-4o',
        'article_polish': 'gpt-4o',
    }

    if st.secrets ["OPENAI_API_TYPE"] == 'azure':
        openai_kwargs['api_base'] = st.secrets["AZURE_API_BASE"]
        openai_kwargs['api_version'] = st.secrets ["AZURE_API_VERSION"]

    lm_configs = STORMWikiLMConfigs()
    lm_configs.set_conv_simulator_lm(ModelClass(model=model_name_map['conv_simulator'], max_tokens=500, **openai_kwargs))
    lm_configs.set_question_asker_lm(ModelClass(model=model_name_map['conv_simulator'], max_tokens=500, **openai_kwargs))
    lm_configs.set_outline_gen_lm(ModelClass(model=model_name_map['outline_gen'], max_tokens=400, **openai_kwargs))
    lm_configs.set_article_gen_lm(ModelClass(model=model_name_map['article_gen'], max_tokens=700, **openai_kwargs))
    lm_configs.set_article_polish_lm(ModelClass(model=model_name_map['article_polish'], max_tokens=4000, **openai_kwargs))

    return lm_configs


def initialize_vector_store():
    """Creates or updates the vector store based on the provided arguments."""
    csv_file_path = "multi_eurlex_structured.csv"
    if not csv_file_path:
        print("No CSV file provided. Skipping vector store initialization.")
        return

    kwargs = {
        'file_path': csv_file_path,
        'content_column': 'content',
        'title_column': 'title',
        'url_column': 'url',
        'desc_column': 'description',
        'batch_size': 32,  # Replace with your desired batch size
        'vector_db_mode': "online",
        'collection_name': "storm_agent",
        'embedding_model': "all-MiniLM-L6-v2",  # Use string instead of model instance
        'device': "cpu",
    }

    try:
        client = QdrantClient(
        url=st.secrets["QDRANT_URL"],
        api_key=st.secrets["QDRANT_API_KEY"]
)
        vector_db = QdrantVectorStoreManager._check_create_collection(
            client=client,
            collection_name="storm_agent",
            model="all-MiniLM-L6-v2"
        )
        print("Vector store initialized successfully.")
        return vector_db
    except Exception as e:
        print(f"Failed to initialize vector store: {e}")
        return None


def initialize_runner(api_key, csv_file_path, output_dir):
    """
    This STORM Wiki pipeline powered by GPT-3.5/4 and local retrieval model that uses Qdrant.
    You need to set up the following environment variables to run this script:
        - OPENAI_API_KEY: OpenAI API key
        - OPENAI_API_TYPE: OpenAI API type (e.g., 'openai' or 'azure')
        - QDRANT_API_KEY: Qdrant API key (needed ONLY if online vector store was used)

    You will also need an existing Qdrant vector store either saved in a folder locally offline or in a server online.
    If not, then you would need a CSV file with documents, and the script is going to create the vector store for you.
    The CSV should be in the following format:
    content  | title  |  url  |  description
    I am a document. | Document 1 | docu-n-112 | A self-explanatory document.
    I am another document. | Document 2 | docu-l-13 | Another self-explanatory document.

    Notice that the URL will be a unique identifier for the document so ensure different documents have different urls.

    Output will be structured as below
    args.output_dir/
        topic_name/  # topic_name will follow convention of underscore-connected topic name w/o space and slash
            conversation_log.json           # Log of information-seeking conversation
            raw_search_results.json         # Raw search results from search engine
            direct_gen_outline.txt          # Outline directly generated with LLM's parametric knowledge
            storm_gen_outline.txt           # Outline refined with collected information
            url_to_info.json                # Sources that are used in the final article
            storm_gen_article.txt           # Final article generated
            storm_gen_article_polished.txt  # Polished final article (if args.do_polish_article is True)
    """
    # Initialize the language model configurations
    lm_configs = initialize_lm_configs()

    # Initialize the vector store (vector database)
    vector_store_manager = initialize_vector_store()

    # Initialize the retrieval model (VectorRM)
    rm = VectorRM(
        collection_name="storm_agent",
        embedding_model="all-MiniLM-L6-v2",  # Pass the model name as a string
        device="cpu",
        k=3,
    )
    
    rm.init_online_vector_db(url=st.secrets["QDRANT_URL"], api_key=st.secrets["QDRANT_API_KEY"])
    # Debugging: Log the state of the retrieval model
    print(f"Initialized retrieval model (rm): {rm}")
    print(f"Methods in retrieval model (rm): {dir(rm)}")

    # Ensure vector store and retrieval model are correctly initialized
    if not rm or not vector_store_manager:
        print("Retrieval model or vector store is not properly initialized.")
        raise ValueError("Retrieval model or vector store is not properly initialized.")
    
    # Debugging: Log the vector store manager
    print(f"Vector store manager: {vector_store_manager}")

    # Initialize the STORMWikiRunner with the appropriate arguments
    runner = STORMWikiRunner(
        STORMWikiRunnerArguments(
            output_dir=output_dir,
            max_conv_turn=3,
            max_perspective=3,
            search_top_k=3,
            max_thread_num=3
        ),
        lm_configs,
        rm
    )

    # Debugging: Log the attributes of the runner object to check if 'rm' is assigned
    print(f"STORMWikiRunner attributes: {dir(runner)}")

    return runner