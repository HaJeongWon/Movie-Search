import requests,core.core as core



#https://developer.themoviedb.org/reference/search-movie
def search_movie(name):
    
    url = "https://api.themoviedb.org/3/search/movie?language=ko&query="+name

    with open("api-key/TMDB.txt", "r", encoding="utf-8") as f:
        api_key = f.read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.get(url, headers=headers, timeout=5)

    return core.json_to_dict(response.text)
        



