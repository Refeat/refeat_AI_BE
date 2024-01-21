from threading import Thread
from typing import List
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule
from .streaming_queue import StreamingQueue
import time


def get_chat_stream(chat_agent: ChatAgentModule, query: str, file_uuid:List[str]=None, project_id=None, chat_history: List[List[str]]=[]):
    print("get_chat_stream", query, file_uuid, project_id, chat_history)
    queue = StreamingQueue()
    content = ""
    def chat_thread_task():
        chat_agent.run(query, file_uuid, project_id, chat_history, queue)
        queue.end_job()
        
    start = time()
    t = Thread(target=chat_thread_task)
    t.start()
    
    while True:
        if queue.is_end():
            print("streaming is ended")
            break
        ## 4개
        if not queue.is_empty():
            next_token = queue.get()
            content += next_token
            print(next_token)
            yield next_token
            
    t.join()
    
def get_dummy_stream():
    queue = StreamingQueue()
    content = ""
    def chat_thread_task():
        generate_dummy_stream(queue)
        queue.end_job()
        
    start = time.time()
    t = Thread(target=chat_thread_task)
    t.start()
    
    while True:
        if queue.is_end():
            print("streaming is ended")
            break
        ## 4개
        if not queue.is_empty():
            next_token = queue.get()
            content += next_token
            print(next_token)
            yield next_token
            
    t.join()
    
def generate_dummy_stream(queue: StreamingQueue):
    for i in range(20):
        queue.append(str(i))
        time.sleep(0.2)
    
    
