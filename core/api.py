if __name__=="__main__":
    print("잘못된 접근입니다. main.py 파일을 실행하십시요.")
    exit()

import requests,core.core as core
import logging

logger = logging.getLogger(__name__)

#https://developer.themoviedb.org/reference/search-movie
def search_movie(name, page = 1):
    logger.info("%s %s페이지 검색", name, page)

    url = f"https://api.themoviedb.org/3/search/movie?language=ko&page={page}&query={name}"

    with open("api/TMDB.txt", "r", encoding="utf-8") as f:
        api_key = f.read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.get(url, headers=headers, timeout=5)

    return core.json_to_dict(response.text)
        



