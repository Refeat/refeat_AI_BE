from backend.db.database import get_db
from sqlalchemy.orm import Session
from ai_module.src.modules.file_to_db.file_processor import FileProcessor
from backend.repository import document
from time import time


def trigger_file_thread(file_processor: FileProcessor, data, project_id, document_id, db: Session = get_db):
    
    print("start threading!!")
    start = time()
    file_processor.process_data(data)
    print("process data: ", time() - start)
    summary = file_processor.get_summary(data) # backend에서 가져가는 summary
    print("summary: ", time() - start)
    document.set_summary_done(db, document_id, summary)
    print('summary:', summary)
    save_path = file_processor.get_save_path(data)
    print("path: ", time() - start)
    file_processor.save_data(data, save_path)
    print("data: ", time() - start)
    file_processor.save_to_db(save_path, project_id)
    print("db: ", time() - start)
    file_processor.save_graph()
    print("save graph: ", time() - start)
    document.set_embedding_done(db, document_id)
    print("finish embedding")