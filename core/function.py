if __name__=="__main__":
    print("잘못된 접근입니다. main.py 파일을 실행하십시요.")
    exit()

import socket, requests
import json
import logging

logger = logging.getLogger(__name__)

def toggle_scrollbar(a):
    # 텍스트가 넘치는지 체크
    total_lines = int(a.index('end-1c').split('.')[0])
    visible_lines = int(a['height'])
    
    return total_lines > visible_lines

def try_tcp_connect(ip, port, timeout = 1):
    socket.create_connection((ip, port), timeout)

def is_tmdb_alive():
    try:
        response = requests.get("https://api.themoviedb.org/3/configuration", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        logger.warning("TMDB API server is down")
        return False
    
def check_internet():
    try:
        try_tcp_connect("8.8.8.8", 53) # 구글 DNS
       
        return not is_tmdb_alive()
    except Exception as e:
        logger.warning(e)
        return False
    
def json_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error("JSON 파싱 에러: "+ e)
        return None
        