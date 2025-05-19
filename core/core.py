import core.api as api,core.function as function
import logging

logger = logging.getLogger(__name__)

"""
core.py 역할

검색 처리, 인터넷 연결 확인 등 핵심 기능을 연결시킴(API를 부르고 GUI에 넘겨줄 가공 담당)
"""

def check_internet():
    return function.check_internet()

def search_movie(a,b):
    logger.info(a + "라는 이름을 가진 영화를 검색합니다")
    return api.search_movie(a,b)

def toggle_scroll(a):
    return function.toggle_scrollbar(a)

def json_to_dict(a):
    return function.json_to_dict(a)

