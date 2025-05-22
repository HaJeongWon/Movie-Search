import requests,core.core as core



#https://developer.themoviedb.org/reference/search-movie
def search_movie(name, page = 1):
    url = f"https://api.themoviedb.org/3/search/movie?language=ko&page={page}&query={name}"

    with open("api/TMDB.txt", "r", encoding="utf-8") as f:
        api_key = f.read()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.get(url, headers=headers, timeout=5)

    return core.json_to_dict(response.text)
        



