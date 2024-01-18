from threading import Thread
from typing import List
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule
from time import time


def get_chat_stream(chat_agent: ChatAgentModule, query: str, file_uuid:List[str]=None, project_id=None, chat_history: List[List[str]]=[]):
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
    
    
    
class StreamingQueue:
    def __init__(self):
        self.main_queue = list()
        self.end_flag = False

    def __len__(self):
        return len(self.main_queue)

    def append(self, new_text):
        # print(new_text)
        self.main_queue.append(new_text)

    def get(self):
        """
        return and delete first object of queue
        """
        return self.main_queue.pop(0)

    def end_job(self):
        self.end_flag = True

    def is_end(self):
        return self.end_flag and len(self.main_queue) == 0

    def is_empty(self):
        return len(self.main_queue) == 0

    def is_streaming_end(self):
        return self.end_flag and len(self.main_queue) > 0
    
    def __str__(self) -> str:
        if len(self.main_queue)>0:
            return self.main_queue[-1]
        else:
            return "empty"

    def refresh(self):
        return ""