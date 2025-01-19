import streamlit as st
from storm_agent import initialize_runner, run_pipeline
from vector_handler import initialize_vectorm
from utils import validate_api_key

# Streamlit Interface
def main():
    """
    Main Streamlit app to interact with the STORM-based legal agent.
    """
    st.set_page_config(page_title="Legal Dialogue Agent", layout="wide")

    # App title and description
    st.title("Legal Dialogue Agent")
    st.write("An AI-powered agent to generate legal arguments and draft submissions based on user queries.")

    # Input OpenAI API Key
    openai_api_key = st.sidebar.text_area("Enter your OpenAI API key:")

    if openai_api_key:
        # Validate API Key
        if not validate_api_key(openai_api_key):
            st.error("Invalid API key. Please provide a valid OpenAI API key.")
            return

    # Initialize STORM and VectorRM
    st.write("Setting up the agent...")
    csv_paths = initialize_vectorm("./datasets")
    output_dir = "./output"  # Path to store output
    runner = initialize_runner(openai_api_key, csv_paths, output_dir)
    st.success("Agent initialized successfully!")

    # User query input
    user_query = st.text_input("What legal topic or issue do you want to address?")

    if st.button("Submit") and user_query:
        st.write("Processing your query...")
        try:
            # Running the pipeline with user query
            article_output_dir = run_pipeline(runner, user_query)
            st.write(f"Generated article stored in: {article_output_dir}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    
    
    
# import streamlit as st
# from storm_agent import initialize_runner, run_pipeline

# # Streamlit UI
# st.title("STORM Wiki Generator")

# api_key = st.text_input("Enter your OpenAI API Key", type="password")
# topic = st.text_input("Enter a topic for the article")
# dataset_path = st.text_input("Path to your dataset")
# output_dir = st.text_input("Path to save output files")
# start_button = st.button("Generate Article")

# if start_button:
#     if not api_key or not topic or not dataset_path or not output_dir:
#         st.error("Please provide all required inputs.")
#     else:
#         with st.spinner("Initializing pipeline..."):
#             runner = initialize_runner(api_key, dataset_path, output_dir)
        
#         with st.spinner(f"Generating article for '{topic}'..."):
#             output_path = run_pipeline(runner, topic)
        
#         st.success("Article generated successfully!")
#         st.write(f"Check the results in: {output_path}")
