import socket

def toggle_scrollbar(a):
    # 텍스트가 넘치는지 체크
    total_lines = int(a.index('end-1c').split('.')[0])
    visible_lines = int(a['height'])
    
    return total_lines > visible_lines

def try_tcp_connect(ip, port, timeout = 1):
    socket.create_connection((ip, port), timeout)

def check_internet():
    try:
        try_tcp_connect("8.8.8.8", 53) # 구글 DNS


        # success = False
        # TMDB
        # for func in [try_tcp_connect("13.225.117.77", 80),try_tcp_connect("13.225.117.101", 80),try_tcp_connect("13.225.117.78", 80),try_tcp_connect("13.225.117.96", 80)]:  # 함수 목록
        #     try:
        #         func()  # 함수 실행
        #         success = True
        #         break  # 하나라도 성공하면 바로 종료
        #     except Exception as e:
        #         continue  # 실패해도 다음 시도

        # if not success:
        #     print("TMDB")
        #     raise Exception("모두 실패")  # 여기서만 except로 감




        # success = False
        # # ChatGPT
        # for func in [try_tcp_connect("172.64.154.211", 80), try_tcp_connect("104.18.33.45", 80)]:  # 함수 목록
        #     try:
        #         func()  # 함수 실행
        #         success = True
        #         break  # 하나라도 성공하면 바로 종료
        #     except Exception as e:
        #         continue  # 실패해도 다음 시도

        # if not success:
        #     print("ChatGPT")
        #     raise Exception("모두 실패")  # 여기서만 except로 감
        
        # success = False
        

        return True
    except Exception as e:
        print(e)
        return False
        