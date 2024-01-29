from ai_module.src.models.llm.chain.summary_chain import SummaryChain
from ai_module.src.database.elastic_search.custom_elastic_search import CustomElasticSearch
from ai_module.src.database.knowledge_graph.graph_construct import KnowledgeGraphDataBase
from ai_module.src.modules.file_to_db.file_processor import FileProcessor
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule
from ai_module.src.modules.add_column.data_extract_module import AddColumnModule


required_classes = {
    "SummaryChain": SummaryChain(),
    "CustomElasticSearch": CustomElasticSearch(
        index_name="refeat_ai", host="http://10.10.10.27:9200"
    ),
    "KnowledgeGraphDatabase": KnowledgeGraphDataBase(),
}


class AiModules:
    _instance = None
    file_processor: FileProcessor
    chat_agent: ChatAgentModule
    column_module: AddColumnModule

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialize(cls)
        return cls._instance
    
    def _initialize(cls):
        summary_chain = SummaryChain()
        es = CustomElasticSearch(index_name="refeat_ai", host="http://10.10.10.27:9200")
        graph = KnowledgeGraphDataBase()
        cls.file_processor: FileProcessor = FileProcessor(
            es=es,
            summary_chain=summary_chain,
            knowledge_graph_db=graph,
            json_save_dir="s3_mount/json/",
            screenshot_dir="s3_mount/screenshot/",
            html_save_dir="s3_mount/html/",
        )
        cls.chat_agent: ChatAgentModule = ChatAgentModule(
            verbose=True, es=es, knowledge_graph_db=graph
        )
        cls.column_module: AddColumnModule = AddColumnModule(es=es)
        

def get_ai_module() -> AiModules:
    return AiModules()
