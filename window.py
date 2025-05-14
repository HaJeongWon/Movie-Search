import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import core

# 테스트용
dummy_movie_info = {
    "poster_url": r"https://upload.wikimedia.org/wikipedia/ko/4/42/%EC%9E%90%EC%A0%84%EC%B0%A8%EC%99%95_%EC%97%84%EB%B3%B5%EB%8F%99_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg",
    "title": "자전차왕 엄복동",
    "overview": "일제 강점기, 엄복동은 조선의 희망이 된다.",
    "rating": "6.7",

}

def check_internet():
    # 상태 체크 시작
    if core.check_internet():
        status_label.configure(text="🟢 이용 가능", text_color="green")
    else:
        status_label.configure(text="🔴 인터넷 확인 필요", text_color="red")
    root.after(5000, check_internet)  # 5초마다 다시 체크

# 검색어 처리 함수
def search_movie(event=None): 

    query = entry.get()
    #query = entry.get("1.0", "end").strip()
    if query.strip() == "":
        result_label.configure(text="영화 제목을 입력하세요.")
    else:

        
        result_label.configure(text=f"정보를 불러오는 중..")#(text=f"입력한 제목: {query}")
        root.update()  # 즉시 화면 반영
        print(f"Searched movie: {query}")  # 실제 API 붙일 자리
        # print(core.search_movie(query))

        
        movie_dict = core.search_movie(query)
        #print(movie_dict)
        """
        필요한 정보들:
            "poster_url": r"",
            "title": "",
            "overview": "",
            "rating": "",

        """

        if movie_dict['total_results']==1:
            movie_info={
                "poster_url": r"https://image.tmdb.org/t/p/w342/"+movie_dict['results'][0]['poster_path'],
                "title": movie_dict['results'][0]['original_title'],
                "overview": movie_dict['results'][0]['overview'],
                "rating": movie_dict['results'][0]['vote_average'],

            }
            window_result_screen(movie_info)
        elif movie_dict['total_results']==0:
            result_label.configure(text=f"검색 결과 없음")
        else:
            result_label.configure(text=f"{movie_dict['total_results']}개의 검색 결과")

# def loading_screen():
#     search_frame.pack_forget() # 기존 검색창 숨기기

#     global load_frame
#     load_frame = ctk.CTkFrame(root, fg_color="transparent")
#     load_frame.pack(fill="both", expand=True, pady=20)

#     label = ctk.CTkLabel(load_frame, text="잠시만 기다려주세요...", font=ctk.CTkFont(size=16, weight="bold"))
#     label.pack(pady=30)

def show_large_image(poster_url):
    # print(poster_url)
    response = requests.get(poster_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((900, 1350))  # 큰 사이즈로 조정

    top = ctk.CTkToplevel()
    top.title("큰 포스터")
    top.resizable(False, False)
    
    photo = ImageTk.PhotoImage(img)
    label = ctk.CTkLabel(top, image=photo, text="")
    label.image = photo  # 참조 유지
    label.pack()
def window_result_screen(movie_info):
    search_frame.pack_forget()

    poster_url = movie_info['poster_url']
    title = movie_info['title']
    overview = movie_info['overview']
    rating = movie_info['rating']

    # 결과 전체 프레임
    global result_frame
    result_frame = ctk.CTkFrame(root, fg_color="transparent")
    result_frame.pack(fill="both", expand=True, pady=20)

    # 카드형 중앙 컨테이너
    card_frame = ctk.CTkFrame(result_frame, corner_radius=15, fg_color="#f9f9f9")
    card_frame.pack(padx=40, pady=30)

    # 좌우 나누는 content_frame
    content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
    content_frame.grid(row=0, column=0, padx=20, pady=20)
    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=2)

    # 왼쪽: 포스터
    image_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    image_frame.grid(row=0, column=0, sticky="n", padx=10)

    try:
        response = requests.get(poster_url)
        image_data = Image.open(BytesIO(response.content)).resize((320, 480))
        poster_image = ImageTk.PhotoImage(image_data)
        image_label = ctk.CTkLabel(image_frame, image=poster_image, text="")
        image_label.image = poster_image
        image_label.pack(padx=(10,0),pady=(20,0))
        image_label.bind("<Button-1>", lambda event: show_large_image(
            poster_url.replace("https://image.tmdb.org/t/p/w342/", "https://image.tmdb.org/t/p/w780/")
        ))
    except:
        error_label = ctk.CTkLabel(image_frame, text="이미지 로드 실패")
        error_label.pack()

    # 오른쪽: 텍스트
    text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    text_frame.grid(row=0, column=1, sticky="nw", padx=30)

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
        scrollbar.pack(side="left", fill="y")
        scrollbar.configure(width=12) 
        overview_textbox.configure(yscrollcommand=scrollbar.set)
    

    
def go_back():
    result_frame.destroy()
    search_frame.pack()



def start_gui():
    # 테마 설정
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # 메인 윈도우 생성
    global root
    root = ctk.CTk()
    root.title("Movie Search")
    root.geometry("800x600")  # 여기 크기로 통일

   # 0. 전체 묶을 프레임 (검색창 + 결과 텍스트 포함)
    global search_frame
    search_frame = ctk.CTkFrame(root, fg_color="transparent")
    search_frame.pack(pady=30)

    # 1. 검색창 + 버튼 (가로 정렬용 서브 프레임)
    input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
    input_frame.pack()

    # 2. 검색창 (왼쪽)
    global entry
    entry = ctk.CTkEntry(input_frame, placeholder_text="영화 제목을 입력하세요", width=300, height=40, corner_radius=10, font=("맑은 고딕", 14))
    # entry = ctk.CTkTextbox(input_frame, width=300, height=40, corner_radius=10, font=("맑은 고딕", 14))
    entry.grid(row=0, column=0, padx=(0, 10))
    entry.bind("<Return>", search_movie)  # Enter 키로 검색

    # 3. 검색 버튼 (오른쪽)
    search_button = ctk.CTkButton(input_frame, text="검색", command=search_movie, width=120, height=40, corner_radius=10,font=ctk.CTkFont(weight="bold"))
    search_button.grid(row=0, column=1)

    # 4. 결과 텍스트 (세로로 아래에 배치)
    global result_label
    result_label = ctk.CTkLabel(search_frame, text="", text_color="black")
    result_label.pack(pady=(10, 0))  # 검색창과 결과 사이 여백

    # # 필요한 UI 요소 미리 선언 (update_result용)
    # poster_label = ctk.CTkLabel(root, text="")
    # poster_label.pack(pady=10)

    # title_label = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=20, weight="bold"))
    # title_label.pack()

    # plot_text = ctk.CTkTextbox(root, height=100, width=600)
    # plot_text.pack(pady=10)

    # rating_label = ctk.CTkLabel(root, text="")
    # rating_label.pack(pady=5)

    # summary_text = ctk.CTkTextbox(root, height=200, width=700)
    # summary_text.pack(pady=20)

    # 인터넷 상태 표시용 라벨
    global status_label
    status_label = ctk.CTkLabel(root, text="연결 상태 확인 중...", anchor="e")
    status_label.pack(side="bottom", pady=5)

    check_internet()

    # 루프 실행
    root.mainloop()
