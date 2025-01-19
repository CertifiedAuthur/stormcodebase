# from knowledge_storm.storm_wiki.engine import STORMWikiRunner, STORMWikiLMConfigs, STORMWikiRunnerArguments
# from knowledge_storm.storm_wiki.modules.knowledge_curation import KnowledgeCurationModule
# from knowledge_storm.storm_wiki.modules.outline_generation import OutlineGenerationModule
# from knowledge_storm.storm_wiki.modules.article_generation import ArticleGenerationModule
# from knowledge_storm.storm_wiki.modules.article_polish import ArticlePolishingModule


# storm = STORMWikiRunner()

# def initialize_agent(api_key: str, vectorm):
#     """
#     Initialize the STORM agent with OpenAI API key and a VectorRM retriever.
#     """
#     curator = KnowledgeCurationModule(retriever=vectorm)
#     outliner = OutlineGenerationModule()
#     generator = ArticleGenerationModule(api_key=api_key)
#     polisher = ArticlePolishingModule(api_key=api_key)
#     return STORMWikiRunner(curator, outliner, generator, polisher)


# def process_query(storm, query: str) -> str:
#     """
#     Process the user query through the STORM pipeline.
#     """
#     curated_knowledge = storm.curate(query)  # Step 1: Knowledge curation
#     outline = storm.generate_outline(curated_knowledge)  # Step 2: Generate outline
#     article = storm.generate_article(outline)  # Step 3: Generate detailed content
#     polished_article = storm.polish(article)  # Step 4: Polish the final article
#     return polished_article



from knowledge_storm.storm_wiki.engine import STORMWikiRunner, STORMWikiLMConfigs, STORMWikiRunnerArguments
from knowledge_storm.rm import VectorRM
import os

def initialize_runner(api_key: str, dataset_path: str, output_dir: str):
    # Initialize retriever
    retriever = VectorRM(
        collection_name="storm_agent",
        embedding_model="sentence-transformers/all-MiniLM-L12-v2",
        device="cpu"
    )
    retriever.init_online_vector_db(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    # Initialize language model configurations
    lm_configs = STORMWikiLMConfigs()
    lm_configs.init_openai_model(openai_api_key=api_key, azure_api_key=None, openai_type="openai")

    # Initialize runner arguments
    args = STORMWikiRunnerArguments(output_dir=output_dir)

    # Initialize runner
    return STORMWikiRunner(args=args, lm_configs=lm_configs, rm=retriever)

def run_pipeline(runner, topic):
    runner.run(topic=topic, do_research=True, do_generate_outline=True,
               do_generate_article=True, do_polish_article=True)
    return runner.article_output_dir
