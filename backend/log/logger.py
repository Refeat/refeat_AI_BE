import logging

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)
# 3. formatting 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 4. handler 설정
# console 출력
stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)
# 파일 출력
file_handler = logging.FileHandler('info.log', mode='a')
logger.addHandler(file_handler)