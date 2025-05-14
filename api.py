import socket, requests
import json

def try_tcp_connect(ip, port, timeout = 1):
    socket.create_connection((ip, port), timeout)

def check_internet():
    try:
        try_tcp_connect("8.8.8.8", 53) # 구글 DNS


        # success = False
        # TMDB
        # for func in [try_tcp_connect("13.225.117.77", 80),try_tcp_connect("13.225.117.101", 80),try_tcp_connect("13.225.117.78", 80),try_tcp_connect("13.225.117.96", 80)]:  # 함수 목록
        #     try:
        #         func()  # 함수 실행
        #         success = True
        #         break  # 하나라도 성공하면 바로 종료
        #     except Exception as e:
        #         continue  # 실패해도 다음 시도

        # if not success:
        #     print("TMDB")
        #     raise Exception("모두 실패")  # 여기서만 except로 감




        # success = False
        # # ChatGPT
        # for func in [try_tcp_connect("172.64.154.211", 80), try_tcp_connect("104.18.33.45", 80)]:  # 함수 목록
        #     try:
        #         func()  # 함수 실행
        #         success = True
        #         break  # 하나라도 성공하면 바로 종료
        #     except Exception as e:
        #         continue  # 실패해도 다음 시도

        # if not success:
        #     print("ChatGPT")
        #     raise Exception("모두 실패")  # 여기서만 except로 감
        
        # success = False
        

        return True
    except Exception as e:
        print(e)
        return False


#https://developer.themoviedb.org/reference/search-movie
def search_movie(name):
    
    url = "https://api.themoviedb.org/3/search/movie?language=ko&query="+name

    with open("api-key/TMDB.txt", "r", encoding="utf-8") as f:
        api_key = f.read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.get(url, headers=headers)

    return json_to_dict(response.text)
        

def json_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print("JSON 파싱 에러:", e)
        return None

