import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
import core.core as core
import concurrent.futures
from customtkinter import CTkImage
import logging
import webbrowser

logger = logging.getLogger(__name__)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
POSTER_BASE_URL = r"https://image.tmdb.org/t/p/w342"
load_fail_img = Image.open(r"assets/load-fail.png")
loading_img = Image.open(r"assets/loading.png")

def start_gui():
    # 테마 설정
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # 메인 윈도우 생성
    global root
    root = ctk.CTk()
    root.title("Movie Search")
    root.geometry("800x650")  # 여기 크기로 통일
    root.resizable(False, False)

   # 0. 전체 묶을 프레임 (검색창 + 결과 텍스트 포함)
    global search_frame
    search_frame = ctk.CTkFrame(root, fg_color="transparent")
    search_frame.pack(pady=30)

    

    # 1. 검색창 + 버튼 (가로 정렬용 서브 프레임)
    input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
    input_frame.pack()

    # search_img = CTkImage(Image.open(r"assets\search-icon.png"), size=(20, 20))

    # icon_label = ctk.CTkLabel(search_frame, image=search_img, text="")  # 텍스트 없이 아이콘만
    # icon_label.grid(row=0, column=0)

    # 2. 검색창 (왼쪽)
    global entry
    entry = ctk.CTkEntry(input_frame, placeholder_text="영화 제목을 입력하세요", width=300, height=40, corner_radius=10, font=("맑은 고딕", 14))
    entry.grid(row=0, column=0, padx=(0, 10))
    entry.bind("<Return>", on_search_button_click)  # Enter 키로 검색

    # 3. 검색 버튼 (오른쪽)
    global search_button
    search_button = ctk.CTkButton(input_frame, text="검색", command=on_search_button_click, width=120, height=40, corner_radius=10,font=ctk.CTkFont(weight="bold"))
    search_button.grid(row=0, column=1)

    # 4. 결과 텍스트 (세로로 아래에 배치)
    global result_label
    result_label = ctk.CTkLabel(search_frame, text="", text_color="black")
    result_label.pack(pady=10)  # 검색창과 결과 사이 여백

    global scrollable_result_frame
    scrollable_result_frame = ctk.CTkScrollableFrame(search_frame, width=600, height=400)
    scrollable_result_frame.pack()

    bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
    bottom_frame.pack(side="bottom",pady=5 , fill="x")

        # column 3개 구성
    bottom_frame.grid_columnconfigure(0, weight=1)  # 왼쪽
    bottom_frame.grid_columnconfigure(1, weight=1)  # 가운데
    bottom_frame.grid_columnconfigure(2, weight=1)  # 오른쪽

    # 인터넷 상태 표시용 라벨
    global status_label
    status_label = ctk.CTkLabel(bottom_frame, text="연결 상태 확인 중...", anchor="e")
    status_label.grid(row=0, column=1, sticky="ew")

        # 내부 아이템도 grid로 정렬
    Icons8_credit_label = ctk.CTkLabel(bottom_frame, text="Icons by Icons8", font=("맑은 고딕", 14, "bold"), fg_color="transparent",text_color="#4B3E3E")
    Icons8_credit_label.grid(row=0, column=2, sticky="e", padx=5)
    Icons8_credit_label.bind("<Button-1>", lambda e: open_link("https://icons8.kr/"))


    
    check_internet()

    # 루프 실행
    root.mainloop()

def open_link(url, event=None):
    webbrowser.open_new(url)

def check_internet():
    # 상태 체크 시작
    if core.check_internet():
        status_label.configure(text="🟢 서버 연결 상태: 정상", text_color="green")
    else:
        status_label.configure(text="🔴 서버 연결 상태: 비정상", text_color="red")

    root.after(5000, check_internet)  # 5초마다 다시 체크

def movie_search():
    global page
    result_label.configure(text="검색 중입니다...")
    search_button.configure(state="disabled")
    # root.update_idletasks()  # UI 강제 반영

    # 스레드 실행을 한 틱(10ms) 밀어서 UI 먼저 그리게 함
    global search_keyword 
    root.after(10, lambda: threaded_search(search_keyword, page))


# 검색어 처리 함수
def on_search_button_click(event=None): 
    global page
    page = 1
    global search_keyword
    search_keyword = entry.get()

    if search_keyword.strip() == "":

        result_label.configure(text="영화 제목을 입력하세요.")
    else:

        logger.info(f"영화 검색 요청: {search_keyword}")
        
        movie_search()   

def threaded_search(search_keyword, page):
    future = executor.submit(core.search_movie, search_keyword, page)
    root.after(100, lambda: check_result(future))

def check_result(future):
    if future.done():
        movie = future.result()
        render_future = executor.submit(handle_result, movie)
        root.after(100, lambda: check_rendering(render_future))

    else:
        root.after(100, lambda: check_result(future))

def check_rendering(render_future):
    if not render_future.done():
        root.after(100, lambda: check_rendering(render_future))

def async_load_image(url, label):
    
    try:
        response = requests.get(url)
        image_data = Image.open(BytesIO(response.content))
        poster_image = CTkImage(light_image=image_data, size=(100, 150))
        label.configure(image=poster_image, text="")
        # label.image = poster_image
        label.bind("<Button-1>",lambda event, a=url.replace("w342", "w780"): show_large_image(a)) # 큰 포스터는 고화질로
    
    except Exception as e:
        logger.error(f"이미지 요청 실패: {e}")
        label.configure(image=CTkImage(load_fail_img, size=(100, 100)), text="")
        # label.configure(text="로드 실패")
    # scrollable_result_frame.update()
    global search_button
    search_button.configure(state="normal")
    
def create_movie_card(i):

    # 전체 프레임
    movie_frame = ctk.CTkFrame(scrollable_result_frame, corner_radius=8, fg_color="#f9f9f9")
    movie_frame.pack(pady=10, padx=(10,8), fill="x")
    movie_frame.pack_propagate(False)
    movie_frame.bind("<Button-1>", lambda event, movie=i: window_result_screen(movie))

            # 내부 정렬을 위해 grid 사용
    movie_frame.grid_columnconfigure(1, weight=1)
    movie_frame.grid_rowconfigure(0, weight=1)
    create_img_frame(movie_frame, i)
    create_text_frame(movie_frame, i)

def create_img_frame(movie_frame,i):
    # 이미지 프레임
    img_frame = ctk.CTkFrame(movie_frame, width=100, height=150, corner_radius=8)
    img_frame.grid(row=0, column=0, padx=10, pady=10)
    img_frame.pack_propagate(False)

    if i['poster_path'] != None: # poster_path가 None인 경우도 있음(ex) titanic 이 경우 if 절 없앨시 검색 결과가 나오지 않음

        poster_url = POSTER_BASE_URL + i['poster_path']
        image_label = ctk.CTkLabel(img_frame, image=CTkImage(loading_img, size=(96, 96)),text="")
        image_label.pack(fill="both", expand=True)
        executor.submit(async_load_image, poster_url, image_label)
    else:
        image_label = ctk.CTkLabel(img_frame)
        image_label.configure(image=CTkImage(load_fail_img, size=(100, 100)), text="")
        # image_label = ctk.CTkLabel(img_frame, text="로드 실패")
        image_label.pack(fill="both", expand=True)
    
def create_text_frame(movie_frame,i):
     # 텍스트 프레임
    text_frame = ctk.CTkFrame(movie_frame, fg_color="transparent")
    text_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    text_frame.grid_columnconfigure(0, weight=1)
    text_frame.bind("<Button-1>", lambda event, movie=i: window_result_screen(movie))

            # 제목
    title = i['title']
    title_label = ctk.CTkLabel(text_frame, text=title, font=("맑은 고딕", 23, "bold"), anchor="w")
    title_label.pack(anchor="w")
    title_label.bind("<Button-1>", lambda event, movie=i: window_result_screen(movie))

def submit_grouped(indexes,movie):
    for i in indexes:
        executor.submit(create_movie_card, movie['results'][i])

def handle_result(movie):
    if movie['total_results']==1:
        result_label.configure(text=f"검색이 완료되었습니다")
        window_result_screen(movie['results'][0])

    elif movie['total_results']==0:
        result_label.configure(text=f"검색 결과 없음")

    else:
        if movie['total_results']>20:
            result_overflow =True
        else:
            result_overflow =False
        result_label.configure(text=f"{movie['total_results']}개의 검색 결과 생성 중...")

        for i in scrollable_result_frame.winfo_children():
            i.destroy()

        # for i in movie['results']:
        #     create_movie_card(i)
        executor.submit(submit_grouped, range(0, len(movie['results']), 3),movie)
        executor.submit(submit_grouped, range(1, len(movie['results']), 3),movie)
        executor.submit(submit_grouped, range(2, len(movie['results']), 3),movie)

        if result_overflow:
            result_label.configure(text=f"{movie['total_results']}개의 검색 결과[{page}페이지]")
        else:
            result_label.configure(text=f"{movie['total_results']}개의 검색 결과")
        

def page_change(page_up,page):
    if page_up:
        page+=1
        movie_search()



def show_large_image(poster_url):
    logging.info(f"큰 포스터를 엽니다[url:{poster_url}]")
    response = requests.get(poster_url)
    img = Image.open(BytesIO(response.content))


    top = ctk.CTkToplevel()
    top.title("큰 포스터")
    top.attributes('-topmost', True)  # 항상 위로 (일시적)
    top.resizable(False, False)
    
    photo = CTkImage(light_image=img, size=(666, 999))
    label = ctk.CTkLabel(top, image=photo, text="")
    label.image = photo  # 참조 유지
    label.pack()

def create_result_frame(movie_info):
    # 결과 전체 프레임
    global result_frame
    result_frame = ctk.CTkFrame(root, fg_color="transparent")
    # 카드형 중앙 컨테이너
    card_frame = ctk.CTkFrame(result_frame, corner_radius=15, fg_color="#f9f9f9")
    card_frame.pack(padx=40, pady=30)

   

    # 좌우 나누는 content_frame
    content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
    content_frame.grid(row=0, column=0, padx=20, pady=20)
    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=2)
    create_poster_section(movie_info['poster_url'],content_frame)
    create_text_section(movie_info['title'], movie_info['rating'],movie_info['overview'],content_frame)

    go_back_button = ctk.CTkButton(card_frame, text="뒤로가기", corner_radius=10,font=ctk.CTkFont(weight="bold"), width=200, height=40)
    go_back_button.bind("<Button-1>",go_back)
    go_back_button.grid(row=1, column=0, pady=(0,10))

    global search_frame
    search_frame.pack_forget()
    result_frame.pack(fill="both", expand=True, pady=20)

def create_poster_section(poster_url,content_frame): 
    # 왼쪽: 포스터
    image_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    image_frame.grid(row=1, column=0, sticky="n", padx=10)
    
    try:
        response = requests.get(poster_url)
        image_data = Image.open(BytesIO(response.content))
        poster_image = CTkImage(light_image=image_data, size=(160, 240))
        image_label = ctk.CTkLabel(image_frame, image=poster_image, text="")
        image_label.image = poster_image
        image_label.pack(padx=(10,0),pady=(20,0))
        image_label.bind("<Button-1>", lambda event: show_large_image(
            poster_url.replace("w342", "w780") # 큰 포스터는 고화질로
        ))
    except Exception as e:
        logger.error(f"이미지 요청 실패: {e}")
        error_label = ctk.CTkLabel(image_frame,image=CTkImage(load_fail_img, size=(160, 160)), text="")
        error_label.pack()
    
def create_text_section(title, rating, overview,content_frame): 
# 오른쪽: 텍스트
    text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    text_frame.grid(row=1, column=1, sticky="nw", padx=30)

    title_label = ctk.CTkLabel(text_frame, text=title, font=("맑은 고딕", 26, "bold"))
    title_label.pack(anchor="w", pady=(0, 10))

    rating_label = ctk.CTkLabel(text_frame, text=f"★ {rating} / 10",
                                font=("맑은 고딕", 20, "bold"), text_color="#ffaa00")
    rating_label.pack(anchor="w", pady=(0, 10))

        # 먼저 overview용 하위 프레임 생성
    overview_frame = ctk.CTkFrame(master=text_frame, fg_color="transparent")
    overview_frame.pack(anchor="w", pady=10)

    # 텍스트박스 (문자 단위 줄바꿈)
    overview_textbox = ctk.CTkTextbox(
        master=overview_frame,
        font=("맑은 고딕", 15),
        wrap="char",
        width=450,
        height=200,
        bg_color="#f5f5f5"
    )
    overview_textbox.insert("1.0", overview)
    overview_textbox.configure(state="disabled")
    overview_textbox.pack(side="left", padx=(0, 5))

    if core.toggle_scroll(overview_textbox):
        # 스크롤바 옆에 붙이기
        scrollbar = ctk.CTkScrollbar(master=overview_frame, command=overview_textbox.yview,fg_color="#cccccc",corner_radius=10)
        scrollbar.configure(width=12) 
        overview_textbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="left", fill="y")
    
    
    
def window_result_screen(movie):
    
    
    logger.info(f"영화의 자세한 정보를 불러옵니다[id:{str(movie['id'])}]")

    movie_info={"title": movie['title'],
                "overview": movie['overview'],
                "rating": movie['vote_average'],}
    movie_info["poster_url"] = POSTER_BASE_URL + movie['poster_path'] if movie['poster_path'] else None

    
    create_result_frame(movie_info)

def go_back(event = None):
    result_frame.destroy()
    search_frame.pack(pady=30)
    search_button.configure(state="normal")


