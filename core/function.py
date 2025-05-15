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

def is_chatgpt_alive():
    try:
        headers = {
            "Authorization": "Bearer YOUR_OPENAI_API_KEY",  # ← 너의 실제 키로 교체
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",  # 또는 gpt-4
            "messages": [{"role": "user", "content": "ping"}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers, timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        logger.warning("ChatGPT API server is down")
        return False
    
def check_internet():
    try:
        try_tcp_connect("8.8.8.8", 53) # 구글 DNS

        # if not (is_chatgpt_alive() and is_tmdb_alive()):
        #     # print(is_chatgpt_alive())
        #     # print(is_tmdb_alive())
        #     return False

        return True
    except Exception as e:
        logger.warning(e)
        return False
    
def json_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error("JSON 파싱 에러: "+ e)
        return None
        