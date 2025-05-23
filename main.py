import ui.window as window
import logging

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