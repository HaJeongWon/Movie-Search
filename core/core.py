if __name__=="__main__":
    print("잘못된 접근입니다. main.py 파일을 실행하십시요.")
    exit()

import core.api as api,core.function as function


"""
core.py 역할

검색 처리, 인터넷 연결 확인 등 핵심 기능을 연결시킴(API를 부르고 GUI에 넘겨줄 가공 담당)
"""

def check_internet():
    """인터넷 연결 상태를 확인함"""
    return function.check_internet()

def search_movie(a,b):
    return api.search_movie(a,b)

def toggle_scroll(a):
    return function.toggle_scrollbar(a)

def json_to_dict(a):
    return function.json_to_dict(a)

