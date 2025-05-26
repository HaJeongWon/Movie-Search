import ui.window as window
import logging, os


path="api/TMDB.txt"

os.makedirs(os.path.dirname(path), exist_ok=True)  # 폴더 없으면 생성

if not os.path.isfile(path) or os.path.getsize(path) == 0:
    print("TMDB API 키가 존재하지 않거나 비어 있습니다.")
    api_key = input("TMDB API 키를 입력하세요: ").strip()
    with open(path, "w") as f:
        f.write(api_key)


# 로그 설정
logging.basicConfig(
    level=logging.INFO,  # 로그 레벨: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("movie_app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("프로그램 시작")

if __name__ == "__main__":
    ui = window.Window()
    ui.start_gui()

logging.info("프로그램 종료")