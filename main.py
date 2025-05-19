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

logging.info("Start program")

if __name__ == "__main__":
    window.start_gui()

# 창을 끄면 멀티스레드도 같이 꺼지게 만듦
window.executor.shutdown(wait=False)
