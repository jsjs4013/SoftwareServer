import urllib
import http.cookiejar
import ssl
from bs4 import BeautifulSoup
import requests

class EclassCheck:
    def check(self, ID, PW):
        #### LOGIN INFO ####
        login_info={
                'id':ID, # YourID 2014112025
                'password':PW # YourPW wlsduddl14!
        }

        #### LOGIN OPERATION ####
        # 로그인 정보를 가지고 사이트를 돌아다녀야 하므로 opener에 쿠키 저장소를 설정해두고 로그인을 시도해야함
        cj = http.cookiejar.LWPCookieJar() # CookieJar() : 쿠키를 저장하는 곳
        https_sslv23_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)) # python의 ssl protocol_SSLv23을 적용하기 위한 handler
        opener = urllib.request.build_opener(https_sslv23_handler,urllib.request.HTTPCookieProcessor(cj)) # SSL과 Cookie를 사용하는 opener 생성. HTTPCookieProcessor : build_opener의 쿠키 저장소를 설정
        urllib.request.install_opener(opener) # install_opener : 위에서 설정한 opener 설정을 전역적으로 사용

        # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
        main_url='http://lib.dongguk.edu/studyroom/mainFullView?type=pc' # 로그인 검증 페이지
        params=urllib.parse.urlencode(login_info) # login_info를 바탕으로 Request 할 수 있게 변환
        req=urllib.request.Request(main_url,params.encode('utf-8')) # Request 생성. Request의 인자를 string 형식으로 직접보낼 수 없음. 'utf-8'로 인코딩 해야 함.
        req = urllib.request.urlopen(req)

        #### LOGIN CHECK ####
        res = opener.open(main_url)
        data = res.read().decode('euc-kr')
        soup = BeautifulSoup(data, "html.parser")

        try :  # 로그인 실패시 예외처리
                userName = soup.find('div', {'class': 'logout'}).find('span', {'class': 'name'}).text
                userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
                return userName  # user 이름 가져오기
        except  AttributeError:
                return False


# from bs4 import BeautifulSoup
# import requests
#
# class EclassCheck:
#     def check(self, ID, PW):
#         #### LOGIN INFO ####
#         login_info={
#                 'id':ID, # YourID 2014112025
#                 'password':PW # YourPW wlsduddl14!
#         }
#
#         # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
#         login_url='http://lib.dongguk.edu/studyroom/mainFullView?type=pc' # 로그인 검증 페이지
#         session = requests.session()
#         r = session.post(login_url, data=login_info)
#
#         #### LOGIN CHECK ####
#         main_url = 'http://lib.dongguk.edu/studyroom/mainFullView?type=pc'
#         r = session.get(main_url)
#         data = r.content.decode('euc-kr')
#         soup = BeautifulSoup(data, "html.parser")
#
#         try :  # 로그인 실패시 예외처리
#                 # userName = soup.find('span', {'class': 'user'}).find('strong').text
#                 userName = soup.find('div', {'class': 'logout'}).find('span', {'class': 'name'}).text
#                 userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
#                 session.close()
#                 return userName  # user 이름 가져오기
#         except  AttributeError:
#                 return False