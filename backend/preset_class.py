from ai_module.src.models.llm.chain.summary_chain import SummaryChain
from ai_module.src.database.elastic_search.custom_elastic_search import CustomElasticSearch
from ai_module.src.database.knowledge_graph.graph_construct import KnowledgeGraphDataBase

        
required_classes = {
    "SummaryChain": SummaryChain(),
    "CustomElasticSearch": CustomElasticSearch(index_name='refeat_ai', host="http://10.10.10.27:9200"),
    "KnowledgeGraphDatabase": KnowledgeGraphDataBase()
}
