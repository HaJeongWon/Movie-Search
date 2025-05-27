if __name__=="__main__":
    print("잘못된 접근입니다. main.py 파일을 실행하십시요.")
    exit()

import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
import core.core as core
import concurrent.futures
from customtkinter import CTkImage
import logging
import webbrowser
from PIL import Image
import certifi


class Window:
    def __init__(self): # 생성자(인스턴스 생성시 즉시 실행됨)
        self.logger = logging.getLogger(__name__)
        self.POSTER_BASE_URL = r"https://image.tmdb.org/t/p/w342"
        self.load_fail_img = Image.open(r"assets/load-fail.png")
        self.loading_img = Image.open(r"assets/loading.png")

        self.root = ctk.CTk()
        self.result_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

        self.page = 0
        self.search_keyword = self.before_keyword = ""
        self.result_overflow = False

        self.GENRE_MAP = {
            28: "액션", 
            12: "모험", 
            16: "애니메이션", 
            35: "코미디", 
            80: "범죄", 
            99: "다큐멘터리", 
            18: "드라마", 
            10751: "가족", 
            14: "판타지", 
            36: "역사", 
            27: "공포", 
            10402: "음악", 
            9648: "미스터리", 
            10749: "로맨스", 
            878: "SF", 
            10770: "TV 영화", 
            53: "스릴러", 
            10752: "전쟁", 
            37: "서부"
        }
        
        

    def start_gui(self): # 시작 창
        # 테마 설정
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        # 메인 윈도우 생성
        
        
        self.root.title("Movie Search")
        self.root.geometry("800x650")  # 여기 크기로 통일
        self.root.resizable(False, False)

        # 0. 전체 묶을 프레임 (검색창 + 결과 텍스트 포함)   
        self.search_frame = ctk.CTkFrame(self.root, fg_color="transparent")   
        self.search_frame.pack(pady=30)

    
        # 1. 검색창 + 버튼 (가로 정렬용 서브 프레임)
        self.input_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        self.input_frame.pack()

        # 2. 검색창 (왼쪽)
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="영화 제목을 입력하세요", width=300, height=40, corner_radius=10, font=("맑은 고딕", 14))
        self.entry.grid(row=0, column=0, padx=(0, 10))
        self.entry.bind("<Return>", self.on_search_button_click)  # Enter 키로 검색

        # 3. 검색 버튼 (오른쪽)  
        self.search_button = ctk.CTkButton(self.input_frame, text="검색", command=self.on_search_button_click, width=120, height=40, corner_radius=10,font=ctk.CTkFont(weight="bold"))
        self.search_button.grid(row=0, column=1)

        # 4. 결과 텍스트 (세로로 아래에 배치)
        self.result_label = ctk.CTkLabel(self.search_frame, text="", text_color="black")
        self.result_label.pack(pady=10)  # 검색창과 결과 사이 여백

        
        self.scrollable_result_frame = ctk.CTkScrollableFrame(self.search_frame, width=600, height=400)
        self.scrollable_result_frame.pack()


        self.page_frame = ctk.CTkFrame(self.search_frame, width=400, height=100, bg_color="transparent",fg_color="transparent")
        self.page_frame.grid_columnconfigure(0, weight=1)  # 왼쪽
        self.page_frame.grid_columnconfigure(1, weight=1)  # 가운데
        self.page_frame.grid_columnconfigure(2, weight=1)  # 오른쪽

        pre_button = ctk.CTkButton(self.page_frame,text="이전", bg_color="transparent", width=100, height=40, corner_radius=10,font=ctk.CTkFont(weight="bold"))
        pre_button.grid(row=0, column=0, sticky="w", padx=(10,5))
        pre_button.bind("<Button-1>", lambda e: self.page_change(False))

        self.page_info = ctk.CTkLabel(self.page_frame, text=f"{self.page}",width=150, font=("맑은 고딕", 26, "bold"), bg_color="transparent")
        self.page_info.grid(row=0, column=1, sticky="ew", padx=5)

        next_button = ctk.CTkButton(self.page_frame, text="다음", bg_color="transparent", width=100, height=40, corner_radius=10,font=ctk.CTkFont(weight="bold"))
        next_button.grid(row=0, column=2, sticky="e", padx=(5,10))
        next_button.bind("<Button-1>", lambda e: self.page_change(True))

        self.bottom_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.bottom_frame.pack(side="bottom",pady=5 , fill="x")

        # column 3개 구성
        self.bottom_frame.grid_columnconfigure(0, weight=1)  # 왼쪽
        self.bottom_frame.grid_columnconfigure(1, weight=1)  # 가운데
        self.bottom_frame.grid_columnconfigure(2, weight=1)  # 오른쪽

        # 인터넷 상태 표시용 라벨
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="연결 상태 확인 중...", anchor="e")
        self.status_label.grid(row=0, column=1, sticky="ew")

        # 내부 아이템도 grid로 정렬
        Icons8_credit_label = ctk.CTkLabel(self.bottom_frame, text="Icons by Icons8", font=("맑은 고딕", 14, "bold"), fg_color="transparent",text_color="#4B3E3E")
        Icons8_credit_label.grid(row=0, column=2, sticky="e", padx=5)
        Icons8_credit_label.bind("<Button-1>", lambda e: self.open_link("https://icons8.kr/"))

        self.check_internet()

        # 루프 실행
        self.root.mainloop() # 화면 구성요소 바꾸면 리렌더링 시키 위한 코드

    def open_link(self, url, event=None):
        webbrowser.open_new(url)

    def check_internet(self):
        # 상태 체크 시작
        if core.check_internet():
            self.status_label.configure(text="🟢 서버 연결 정상", text_color="green")
        else:
            self.status_label.configure(text="🔴 서버 연결 비정상", text_color="red")

        self.root.after(5000, self.check_internet)  # 5초마다 다시 체크

    def movie_search(self):
        self.result_label.configure(text="검색 중입니다...")
        self.search_button.configure(state="disabled")

        # 스레드 실행을 한 틱(10ms) 밀어서 UI 먼저 그리게 함
        self.root.after(10, lambda: self.threaded_search(self.search_keyword, self.page))


    # 검색어 처리 함수
    def on_search_button_click(self, event=None): 
        self.page = 1 # 페이지 초기화
        self.before_keyword = self.search_keyword
        self.search_keyword = self.entry.get()
        

        if self.search_keyword.strip() == "":
            self.result_label.configure(text="영화 제목을 입력하세요.")

        else:
            self.logger.info(f"영화 검색 요청: {self.search_keyword}")
            self.movie_search()   

    def threaded_search(self, search_keyword, page): # 검색 결과 가져올때 프리징 발생(멀티스레드 사용해서 해결)
        future = self.executor.submit(core.search_movie, search_keyword, page)
        self.root.after(100, lambda: self.check_result(future))

    def check_result(self, future):
        if future.done(): # 멀티스레드 작업이 끝나면
            movie = future.result()
            render_future = self.executor.submit(self.handle_result, movie)
            self.root.after(100, lambda: self.check_rendering(render_future))

        else:
            self.root.after(100, lambda: self.check_result(future))

    def check_rendering(self, render_future):
        if not render_future.done():
            self.root.after(100, lambda: self.check_rendering(render_future))

    def async_load_image(self, url, label):
        try:
            response = requests.get(url, verify=certifi.where())
            image_data = Image.open(BytesIO(response.content))
            poster_image = CTkImage(light_image=image_data, size=(100, 150))
            label.configure(image=poster_image, text="")
            label.bind("<Button-1>",lambda event, a=url.replace("w342", "w780"): self.show_large_image(a)) # 큰 포스터는 고화질로
        
        except Exception as e:
            self.logger.error(f"이미지 요청 실패: {e}")
            label.configure(image=CTkImage(self.load_fail_img, size=(100, 100)), text="")

        self.search_button.configure(state="normal")
        
    def create_movie_card(self, i):
        # 전체 프레임
        movie_frame = ctk.CTkFrame(self.scrollable_result_frame, corner_radius=8, fg_color="#f9f9f9")
        movie_frame.pack_propagate(False)
        movie_frame.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))

        # 내부 정렬을 위해 grid 사용
        movie_frame.grid_columnconfigure(1, weight=1)
        movie_frame.grid_rowconfigure(0, weight=1)
        self.create_img_frame(movie_frame, i)
        self.create_text_frame(movie_frame, i)
        
        return movie_frame

    def create_img_frame(self, movie_frame,i):
        # 이미지 프레임
        img_frame = ctk.CTkFrame(movie_frame, width=100, height=150, corner_radius=8)
        img_frame.grid(row=0, column=0, padx=10, pady=10)
        img_frame.pack_propagate(False)

        if i['poster_path'] != None: # poster_path가 None인 경우도 있음(ex) titanic 이 경우 if 절 없앨시 검색 결과가 나오지 않음
            poster_url = self.POSTER_BASE_URL + i['poster_path']
            image_label = ctk.CTkLabel(img_frame, image=CTkImage(self.loading_img, size=(96, 96)),text="")
            image_label.pack(fill="both", expand=True)
            self.executor.submit(self.async_load_image, poster_url, image_label)

        else:
            image_label = ctk.CTkLabel(img_frame)
            image_label.configure(image=CTkImage(self.load_fail_img, size=(100, 100)), text="")
            image_label.pack(fill="both", expand=True)
        
    def create_text_frame(self, movie_frame,i):
        # 텍스트 프레임
        text_frame = ctk.CTkFrame(movie_frame, fg_color="transparent")
        text_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))

        
        # 제목
        title = i['title']
        title_label = ctk.CTkLabel(text_frame, text=title, font=("맑은 고딕", 26, "bold"), anchor="w")
        title_label.pack(anchor="w")
        title_label.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))
    
        i['release_date'] = i['release_date'].replace("-","")

        i['release_date'] = i['release_date'][:4]+"년 "+i['release_date'][4:6]+"월 "+i['release_date'][6:]+"일"
        release_date=i['release_date']
        release_date_label = ctk.CTkLabel(text_frame, text=f"개봉일: {release_date}", font=("맑은 고딕", 18, "bold"), anchor="w")
        
        release_date_label.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))


        genre_frame=ctk.CTkFrame(text_frame, fg_color="transparent")
        
        for a, b in enumerate(i['genre_ids']):
            genre = self.get_genre_names(b)
            genre_label_container = ctk.CTkFrame(genre_frame, corner_radius=10, fg_color="#61a1d2")
            genre_label_container.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))

            genre_label = ctk.CTkLabel(genre_label_container, text=genre, font=("맑은 고딕", 17, "bold"),text_color="white")
            genre_label.bind("<Button-1>", lambda event, movie=i: self.window_result_screen(movie))
            genre_label.pack(padx=10, pady=2, anchor="w")

            genre_label_container.grid(row=0, column=a,padx=2,sticky="w")

        
            release_date_label.pack(anchor="w",pady=5)
            genre_frame.pack(anchor="w",pady=5)

    def get_genre_names(self, genre_ids):
        return self.GENRE_MAP.get(genre_ids, "Unknown")

    def submit_grouped(self, indexes,movie):
        for i in indexes:
            self.executor.submit(self.create_movie_card, movie['results'][i],i)

    def handle_result(self, movie):
        
        self.total_results = movie['total_results']

        if self.total_results == 0:
            self.result_label.configure(text="검색된 영화가 없습니다")
            self.search_keyword = self.before_keyword # 검색된 영화가 없을 시 전 검색 내용으로 저장
            return

        if self.result_overflow:
            self.page_frame.pack_forget()
            self.result_overflow = False

        self.scrollable_result_frame.pack_forget()

        
        for i in self.scrollable_result_frame.winfo_children(): # 화면에서 destory 했더니 렌더링 중에 프레임이 사라져서 에러 엄청 뜸
            # 일단 화면에서 숨기고 메모리에서 삭제 안 시켜서 오류 방지(메모리 누수 지점)
            i.pack_forget()
        
        

        if self.total_results > 20:
            self.result_overflow = True

        if self.result_overflow:
            self.result_label.configure(text=f"{self.total_results}개의 검색 결과 중 20개의 결과 생성 중...")
            total_page = (self.total_results + 19) // 20
            self.page_info.configure(text=f"{self.page} / {total_page}")

        else:
            self.result_label.configure(text=f"{self.total_results}개의 검색 결과 생성 중...")
            self.page_frame.pack_forget()

        self.results_to_render = movie['results']
        self.render_index = 0
        self.root.after(0, self.render_next_card)

            

    def render_next_card(self):
        if self.render_index < len(self.results_to_render):
            movie = self.results_to_render[self.render_index]
            card = self.create_movie_card(movie)
            card.pack(pady=10, padx=(10,8), fill="x")
            self.render_index += 1
            self.root.after(10, self.render_next_card)  # 10ms 후 다음 카드 렌더링
        else:
            self.result_label.configure(text=f"{self.total_results}개 중 {len(self.results_to_render)}개의 검색 결과")
            self.scrollable_result_frame.pack()
            if self.result_overflow:
                self.page_frame.pack(pady=(10, 0))

    def page_change(self, page_up):
        if page_up:
            self.page+=1
            self.movie_search()
        else:
            self.page-=1
            self.movie_search()
        self.page_info.configure(text="로딩..")



    def show_large_image(self, poster_url): # 포스터를 큰 화면으로 여는 함수
        self.logger.info(f"큰 포스터를 엽니다[url:{poster_url}]")
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

    def create_result_frame(self, movie_info): # 결과창
        # 카드형 중앙 컨테이너
        card_frame = ctk.CTkFrame(self.result_frame, corner_radius=15, fg_color="#f9f9f9")
        card_frame.pack(padx=20, pady=(20,0))

        self.movie_contents_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        self.movie_contents_frame.pack(padx = 10, pady = (10,0))

        # 좌우 나누는 poster_info_frame
        self.poster_info_frame = ctk.CTkFrame(self.movie_contents_frame, fg_color="transparent")
        self.poster_info_frame.pack(padx=5, pady=5,fill="x")
        self.poster_info_frame.columnconfigure(0, weight=1)
        self.poster_info_frame.columnconfigure(1, weight=1)
        self.create_poster_section(movie_info)
        self.create_movie_info(movie_info)
        self.overview(movie_info)

        go_back_button = ctk.CTkButton(card_frame, text="뒤로가기", corner_radius=10,font=ctk.CTkFont(weight="bold"), width=200, height=40)
        go_back_button.bind("<Button-1>",self.go_back)
        go_back_button.pack(pady=(0,10))


        self.search_frame.pack_forget()
        self.result_frame.pack(fill="both", expand=True, pady=20)


    def create_poster_section(self, movie_info): # 결과창에서 포스터 부분을 담당하는 함수
        # 왼쪽: 포스터
        poster_url = movie_info['poster_url']
        image_frame = ctk.CTkFrame(self.poster_info_frame, fg_color="transparent")
        image_frame.grid(row=1, column=0, sticky="wn", padx=(10,0))
        
        try:
            response = requests.get(poster_url)
            image_data = Image.open(BytesIO(response.content))
            poster_image = CTkImage(light_image=image_data, size=(170, 255))
            image_label = ctk.CTkLabel(image_frame, image=poster_image, text="")
            image_label.image = poster_image
            image_label.pack(padx=(20,0),pady=(10,0))
            image_label.bind("<Button-1>", lambda event: self.show_large_image(
                poster_url.replace("w342", "w780") # 큰 포스터는 고화질로
            ))

        except Exception as e:
            self.logger.error(f"이미지 요청 실패: {e}")
            error_label = ctk.CTkLabel(image_frame,image=CTkImage(self.load_fail_img, size=(180, 270)), text="")
            error_label.pack()
        
    def create_movie_info(self,movie_info): # 결과창에서 텍스트 부분을 담당하는 함수
        # 오른쪽: 텍스트
        title = movie_info['title']
        rating = movie_info['rating']
        text_frame = ctk.CTkFrame(self.poster_info_frame, fg_color="transparent")
        text_frame.grid(row=1, column=1, sticky="nw")
        title_label = ctk.CTkLabel(text_frame, text=title, font=("맑은 고딕", 34, "bold"))
        title_label.pack(anchor="w", pady=10)

        rating_label = ctk.CTkLabel(text_frame, text=f"★ {rating} / 10",font=("맑은 고딕", 22, "bold"), text_color="#ffaa00")
        rating_label.pack(anchor="w", pady=10)

        release_date_label = ctk.CTkLabel(text_frame, text=f'개봉일: {movie_info["release_date"]}', font=("맑은 고딕", 22, "bold"), anchor="w")
        release_date_label.pack(anchor="w", pady=10)

        genre_list=[]
        for i in movie_info["genre_ids"]:
            genre_list += [self.get_genre_names(i)]
        genres_label = ctk.CTkLabel(text_frame,text=f'장르: {", ".join(genre_list)}', font=("맑은 고딕", 22, "bold"), anchor="w")
        genres_label.pack(anchor="w", pady=10)

    def overview(self, movie_info):
        # 먼저 overview용 하위 프레임 생성
        overview_frame = ctk.CTkFrame(master=self.movie_contents_frame, fg_color="transparent")
        overview_frame.pack(padx=30,pady=10)


        # 텍스트박스 (문자 단위 줄바꿈)
        overview_textbox = ctk.CTkTextbox(
            master=overview_frame,
            font=("맑은 고딕", 18, "bold"),
            wrap="char",
            width=600,
            height=200,
            bg_color="#f5f5f5"
        )


        overview_textbox.insert("1.0", movie_info["overview"])
        overview_textbox.configure(state="disabled")
        overview_textbox.pack(side="left", padx=(0, 5))

        if core.toggle_scroll(overview_textbox): # 텍스트가 정해진 라벨 크기보다 더 클 때 스크롤을 생성하는 함수
            # 스크롤바 옆에 붙이기
            scrollbar = ctk.CTkScrollbar(master=overview_frame, command=overview_textbox.yview,fg_color="#cccccc",corner_radius=10)
            scrollbar.configure(width=12) 
            overview_textbox.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="left", fill="y")
        
        
        
    def window_result_screen(self, movie):
        self.logger.info(f"영화의 자세한 정보를 불러옵니다[id:{str(movie['id'])}]")
        
        movie_info={"title": movie['title'],
                    "overview": movie['overview'],
                    "rating": movie['vote_average'],
                    "release_date":movie['release_date'],
                    "genre_ids": movie["genre_ids"]
                    }
        movie_info["poster_url"] = self.POSTER_BASE_URL + movie['poster_path'] if movie['poster_path'] else None
        
        self.create_result_frame(movie_info)

    def go_back(self, event = None): # 뒤로가기 함수(결과창->검색창)
        self.result_frame.pack_forget()
        for i in self.result_frame.winfo_children():
            i.destroy()
        self.search_frame.pack(pady=30)
        self.search_button.configure(state="normal")


    def __del__(self):
        # 창을 끄면 멀티스레드도 같이 꺼지게 만듦
        self.executor.shutdown(wait=False)