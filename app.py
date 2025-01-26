import os
import streamlit as st
from streamlit_card import card
from storm_agent import initialize_runner


def sanitize_query(query):
    """Sanitize the user query to match the folder naming convention."""
    return query.replace(" ", "_").replace("?", "").replace("/", "_").replace("\\", "_")


def read_file(file_path):
    """Read a file with fallback for encoding errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()


def format_outline(outline_content):
    """Format the outline content into a structured hierarchy."""
    formatted_outline = []
    section_counters = {1: 0, 2: 0, 3: 0}

    for line in outline_content.splitlines():
        if line.startswith("# "):
            section_counters[1] += 1
            section_counters[2] = section_counters[3] = 0
            formatted_outline.append(f"{section_counters[1]}. {line[2:]}")
        elif line.startswith("## "):
            section_counters[2] += 1
            section_counters[3] = 0
            formatted_outline.append(f"  {section_counters[1]}.{section_counters[2]}. {line[3:]}")
        elif line.startswith("### "):
            section_counters[3] += 1
            formatted_outline.append(f"    {section_counters[1]}.{section_counters[2]}.{section_counters[3]}. {line[4:]}")
        else:
            formatted_outline.append(line)

    return "\n".join(formatted_outline)


def format_article(article_content):
    """
    Format the article content:
    - Remove '#' symbols, and return only the associated text.
    """
    formatted_article = []

    for line in article_content.splitlines():
        if line.startswith("#"):
            # Remove '#' and strip leading/trailing whitespace
            formatted_article.append(line.lstrip("#").strip())
        else:
            # Append lines that do not start with '#'
            formatted_article.append(line.strip())

    return "\n".join(formatted_article)


def display_card(title, content, description="Click to expand"):
    """Display content in a visually appealing card."""
    card(
        title=title,
        text=f"{description}\n\n{content[:200]}...",  # Show a preview
        image=None,
        styles={
            "card-style": {"border": "2px solid #4CAF50", "padding": "15px"},
            "title-style": {"color": "#4CAF50", "font-weight": "bold"},
        },
    )


def display_content(content):
    """Display the full content without pagination."""
    st.text_area("Content", content, height=400)

def streamlit_interface():
    st.set_page_config(page_title="Legal Dialogue Agent", layout="wide")
    st.title("Legal Dialogue Agent")
    st.write("An AI-powered agent to generate legal arguments and draft submissions.")

    # Initialize session state
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "agent_runner" not in st.session_state:
        st.session_state.agent_runner = None
    if "output_dir" not in st.session_state:
        st.session_state.output_dir = os.path.join(os.getcwd(), "output")

    # OpenAI API key input
    def on_api_key_entered():
        api_key = st.session_state.get("openai_api_key")
        if api_key:
            with st.spinner("Setting up the agent..."):
                try:
                    st.session_state.agent_runner = initialize_runner(
                        api_key, "multi_eurlex_structured.csv", st.session_state.output_dir
                    )
                    st.session_state.initialized = True
                    st.success("Agent initialized successfully!")
                except Exception as e:
                    st.error(f"Initialization error: {e}")

    st.sidebar.text_input("OpenAI API Key:", key="openai_api_key", type="password", on_change=on_api_key_entered)

    if not st.session_state.initialized:
        st.warning("Enter your API key to initialize the agent.")
        return

    # Query input
    user_query = st.text_input("What legal topic do you want to address?", key="user_query")

    if st.button("Submit"):
        if not user_query:
            st.warning("Please enter a query.")
            return

        sanitized_query = sanitize_query(user_query)
        with st.spinner("Processing your query..."):
            try:
                runner = st.session_state.agent_runner
                if not runner:
                    st.error("Agent not initialized.")
                    return

                runner.run(user_query)
                output_folder = os.path.join(st.session_state.output_dir, sanitized_query)

                if not os.path.exists(output_folder):
                    st.error("Output folder not found.")
                    return

                # Display Outline
                outline_path = os.path.join(output_folder, "storm_gen_outline.txt")
                if os.path.exists(outline_path):
                    outline_content = read_file(outline_path)
                    formatted_outline = format_outline(outline_content)
                    st.write("### Generated Outline:")
                    display_content(formatted_outline)  # Use display_content instead of pagination

                # Display Polished Article with formatting
                article_path = os.path.join(output_folder, "storm_gen_article_polished.txt")
                if os.path.exists(article_path):
                    article_content = read_file(article_path)
                    formatted_article = format_article(article_content)  # Format the article
                    st.write("### Polished Legal Article:")
                    display_content(formatted_article)  # Use display_content instead of pagination

            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    streamlit_interface()


# import os
# import time
# import streamlit as st
# from storm_agent import initialize_runner


# def sanitize_query(query):
#     """Sanitize the user query to match the folder naming convention."""
#     return query.replace(" ", "_").replace("?", "").replace("/", "_").replace("\\", "_")

# def read_file(file_path):
#     """Read a file with fallback for encoding errors."""
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             return file.read()
#     except UnicodeDecodeError:
#         with open(file_path, "r", encoding="utf-8", errors="replace") as file:
#             return file.read()


# def format_outline(outline_content):
#     """
#     Format the outline content:
#     - Convert '#' into structured Roman numeral-based hierarchy.
#     """
#     formatted_outline = []
#     section_counters = {1: 0, 2: 0, 3: 0}  # For main, sub, and sub-sub sections

#     for line in outline_content.splitlines():
#         if line.startswith("# "):  # Main section
#             section_counters[1] += 1
#             section_counters[2] = 0  # Reset sub-section counter
#             section_counters[3] = 0  # Reset sub-sub-section counter
#             formatted_outline.append(f"{section_counters[1]}. {line[2:]}")
#         elif line.startswith("## "):  # Sub-section
#             section_counters[2] += 1
#             section_counters[3] = 0  # Reset sub-sub-section counter
#             formatted_outline.append(
#                 f"    {section_counters[1]}.{section_counters[2]}. {line[3:]}"
#             )
#         elif line.startswith("### "):  # Sub-sub-section
#             section_counters[3] += 1
#             formatted_outline.append(
#                 f"        {section_counters[1]}.{section_counters[2]}.{section_counters[3]}. {line[4:]}"
#             )
#         else:  # Regular text or unexpected format
#             formatted_outline.append(line)

#     return "\n".join(formatted_outline)


# def format_article(article_content):
#     """
#     Format the article content:
#     - Remove '#' symbols, and return only the associated text.
#     """
#     formatted_article = []

#     for line in article_content.splitlines():
#         if line.startswith("#"):
#             # Remove '#' and strip leading/trailing whitespace
#             formatted_article.append(line.lstrip("#").strip())
#         else:
#             # Append lines that do not start with '#'
#             formatted_article.append(line.strip())

#     return "\n".join(formatted_article)


# def streamlit_interface():
#     """
#     Streamlit interface for the legal dialogue agent.
#     """
#     st.set_page_config(page_title="Legal Dialogue Agent", layout="wide")

#     # App title and description
#     st.title("Legal Dialogue Agent")
#     st.write("An AI-powered agent to generate legal arguments and draft submissions based on user queries.")

#     # Initialize session state variables
#     if "initialized" not in st.session_state:
#         st.session_state.initialized = False
#     if "agent_runner" not in st.session_state:
#         st.session_state.agent_runner = None
#     if "output_dir" not in st.session_state:
#         st.session_state.output_dir = os.path.join(os.getcwd(), "output")

#     # Callback function to initialize the agent when API key is entered
#     def on_api_key_entered():
#         openai_api_key = st.session_state.openai_api_key
#         if openai_api_key:
#             with st.spinner("Setting up the agent..."):
#                 try:
#                     csv_file_path = "multi_eurlex_structured.csv"

#                     # Initialize the agent runner
#                     st.session_state.agent_runner = initialize_runner(
#                         openai_api_key, csv_file_path, st.session_state.output_dir
#                     )

#                     st.session_state.initialized = True
#                     placeholder = st.empty()
#                     placeholder.success("Agent initialized successfully!")
#                     time.sleep(5)
#                     placeholder.empty()
#                 except Exception as e:
#                     st.error(f"Error during initialization: {e}")

#     # Input OpenAI API Key with an on_change callback
#     st.sidebar.text_input(
#         "Enter your OpenAI API key:",
#         key="openai_api_key",
#         on_change=on_api_key_entered,
#         type="password"
#     )

#     if not st.session_state.initialized:
#         st.warning("Please enter your OpenAI API key to initialize the agent.")
#         return

#     # User query input
#     user_query = st.text_input("What legal topic or issue do you want to address?", key="user_query")

#     if st.button("Submit"):
#         if not user_query:
#             st.warning("Please enter a query before submitting.")
#             return

#         # Sanitize the query to match folder naming conventions
#         sanitized_query = sanitize_query(user_query)

#         # Run the pipeline
#         with st.spinner("Processing your query..."):
#             try:
#                 runner = st.session_state.agent_runner
#                 if runner is None:
#                     st.error("The runner is not initialized.")
#                     return

#                 # Run the agent pipeline
#                 runner.run(user_query)

#                 # Construct output folder path
#                 output_folder = os.path.join(st.session_state.output_dir, sanitized_query)

#                 # Check if the folder exists
#                 if not os.path.exists(output_folder):
#                     st.error(f"Output folder for the query '{sanitized_query}' was not found.")
#                     return

#                 # Read and display the storm_gen_outline.txt
#                 outline_file_path = os.path.join(output_folder, "storm_gen_outline.txt")
#                 if os.path.exists(outline_file_path):
#                     outline_content = read_file(outline_file_path)
#                     formatted_outline = format_outline(outline_content)
#                     st.markdown("### Generated Outline:")
#                     st.markdown(f"```\n{formatted_outline}\n```")
#                 else:
#                     st.warning("storm_gen_outline.txt not found.")

#                 # Read and display the storm_gen_article_polished.txt
#                 polished_article_path = os.path.join(output_folder, "storm_gen_article_polished.txt")
#                 if os.path.exists(polished_article_path):
#                     polished_article_content = read_file(polished_article_path)
#                     formatted_article = format_article(polished_article_content)
#                     st.markdown("### Polished Legal Article:")
#                     st.markdown(f"```\n{formatted_article}\n```")
#                 else:
#                     st.warning("storm_gen_article_polished.txt not found.")

#             except Exception as e:
#                 st.error(f"An error occurred: {e}")


# if __name__ == "__main__":
#     streamlit_interface()






