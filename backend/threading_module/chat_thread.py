from threading import Thread
from typing import List
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule
from .streaming_queue import StreamingQueue
from sqlalchemy.orm import Session
from backend.repository import chat
import time
import asyncio


def get_chat_stream(chat_agent: ChatAgentModule, query: str, file_uuid:List[str]=None, project_id=None, chat_history: List[List[str]]=[], db:Session=None):
    print("get_chat_stream", query, file_uuid, project_id, chat_history)
    queue = StreamingQueue()
    content = ""
    def chat_thread_task():
        chat_agent.run(query, file_uuid, project_id, chat_history, queue)
        queue.end_job()
        
    t = Thread(target=chat_thread_task)
    t.start()
    
    while True:
        time.sleep(0.1)
        if not queue.is_document_end():
            continue
        else:
            yield str(queue.document_info)
            print(queue.document_info)
            break
    
    while True:
        time.sleep(0.1)
        if queue.is_end():
            print("streaming is ended")
            break
        ## 4개
        while not queue.is_empty():
            next_token = queue.get()
            # if type(next_token) == list:

            print(next_token, end=" ")
            yield next_token
    chat.add_ai_chat(db, project_id, queue.content, queue.document_info)

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
    
    yield "{'5a9ff9c0-490c-4413-8ce7-50eb36e9789a': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770},'5a9ff9c0-490c-4413-8ce7-50eb36e9789b': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770},'5a9ff9c0-490c-4413-8ce7-50eb36e9789c': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770}}"
    time.sleep(1)
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
    
    
def get_dummy_stream_error():
    queue = StreamingQueue()
    content = ""
    def chat_thread_task():
        generate_dummy_stream(queue)
        queue.end_job()
        
    start = time.time()
    count = 0
    t = Thread(target=chat_thread_task)
    t.start()
    yield "{'5a9ff9c0-490c-4413-8ce7-50eb36e9789a': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770},'5a9ff9c0-490c-4413-8ce7-50eb36e9789b': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770},'5a9ff9c0-490c-4413-8ce7-50eb36e9789c': {'left_x': 70, 'top_y': 67, 'right_x': 526, 'bottom_y': 770}}"
    time.sleep(1)
    
    while True:
        time.sleep(0.1)
        if queue.is_end():
            print("streaming is ended")
            break
        ## 4개
        while not queue.is_empty():
            next_token = queue.get()
            content += next_token
            if count > 10:
                raise Exception("error")
            count += 1
            print(next_token)
            yield next_token
            
    t.join()
    
def generate_dummy_stream(queue: StreamingQueue):
    for i in range(20):
        queue.append(str(i))
        time.sleep(0.2)
    
    
