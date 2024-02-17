from ai_module.src.database.elastic_search.custom_elastic_search import CustomElasticSearch
from ai_module.src.database.knowledge_graph.graph_construct import KnowledgeGraphDataBase
from ai_module.src.modules.summary.summary_module import SummaryModule
from ai_module.src.modules.file_to_db.file_processor import FileProcessor
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule
from ai_module.src.modules.add_column.data_extract_module import AddColumnModule
from starlette.config import Config



class AiModules:
    _instance = None
    file_processor: FileProcessor
    chat_agent: ChatAgentModule
    column_module: AddColumnModule

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._initialize(cls)
            print("Models initialized!")
        return cls._instance
    
    def _initialize(cls):
        config = Config('.env')

        ELASTICSEARCH_URL = config('ELASTICSEARCH_URL')
        summary_module = SummaryModule()
        es = CustomElasticSearch(index_name="refeat_ai", host=ELASTICSEARCH_URL)
        graph = KnowledgeGraphDataBase()
        cls.file_processor: FileProcessor = FileProcessor(
            es=es,
            summary_module=summary_module,
            knowledge_graph_db=graph,
            json_save_dir="s3_mount/json/",
            screenshot_dir="s3_mount/screenshot/",
            html_save_dir="s3_mount/html/",
            pdf_save_dir="s3_mount/pdf/",
            favicon_save_dir="s3_mount/favicon/",
        )
        cls.chat_agent: ChatAgentModule = ChatAgentModule(
            verbose=True, es=es, knowledge_graph_db=graph
        )
        cls.column_module: AddColumnModule = AddColumnModule(es=es)
        
        

def get_ai_module() -> AiModules:
    return AiModules()
