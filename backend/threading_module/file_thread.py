from backend.db.database import get_db
from sqlalchemy.orm import Session
from ai_module.src.modules.file_to_db.file_processor import FileProcessor
from backend.db.repository import document
from ai_module.src.models.errors import error
from time import time

import cProfile

def trigger_file_thread(file_processor: FileProcessor, data, project_id, document_id, db: Session = get_db):
    # pr = cProfile.Profile()
    # pr.enable()
    print("start threading!!")
    start = time()
    try: 
        summary = file_processor.get_summary(data, lang='ko') # backend에서 가져가는 summary
        print("summary: ", time() - start)
        document.set_summary_done(db, document_id, summary)
        print('summary:', summary)
    except error.AIFailException as e:
        document.summary_fail(db, document_id)
        print(e)
        return
    
    try:
        file_processor.process_data(data)
        print("process data: ", time() - start)
    except error.AIFailException as e:
        document.embedding_fail(db, document_id)
        print(e)
        return
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
    # pr.disable()
    # pr.dump_stats('profile_results_document.prof')