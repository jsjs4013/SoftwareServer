import urllib
import http.cookiejar
import ssl
from bs4 import BeautifulSoup

class EclassCheck:
    def check(self):
        #### LOGIN INFO ####
        # 헤더에 실어보낼 값
        login_info={
                'userDTO.userId':'2014112025', # YourID
                'userDTO.password':'wlsduddl14!' # YourPW
        }

        #### LOGIN OPERATION ####
        # 로그인 정보를 가지고 사이트를 돌아다녀야 하므로 opener에 쿠키 저장소를 설정해두고 로그인을 시도해야함
        cj = http.cookiejar.LWPCookieJar() # CookieJar() : 쿠키를 저장하는 곳
        https_sslv23_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)) # python의 ssl protocol_SSLv23을 적용하기 위한 handler
        opener = urllib.request.build_opener(https_sslv23_handler,urllib.request.HTTPCookieProcessor(cj)) # SSL과 Cookie를 사용하는 opener 생성. HTTPCookieProcessor : build_opener의 쿠키 저장소를 설정
        urllib.request.install_opener(opener) # install_opener : 위에서 설정한 opener 설정을 전역적으로 사용

        # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
        login_url='https://eclass.dongguk.edu/User.do?cmd=loginUser' # 로그인 검증 페이지
        params=urllib.parse.urlencode(login_info) # login_info를 바탕으로 Request 할 수 있게 변환
        req=urllib.request.Request(login_url,params.encode('utf-8')) # Request 생성. Request의 인자를 string 형식으로 직접보낼 수 없음. 'utf-8'로 인코딩 해야 함.
        res = urllib.request.urlopen(req) # Request 전송
        #res = opener.open(login_url)

        try:
            #### LOGIN CHECK : user 이름 가져오기 ####
            main_url = 'https://eclass.dongguk.edu/Main.do?cmd=viewEclassMain&mainMenuId=menu_00050&subMenuId=&menuType=menu'
            res = opener.open(main_url)
            data = res.read().decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")

            try :  # 로그인 실패시 예외처리
                    userName = soup.find('span', {'class': 'user'}).find('strong').text
                    userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
                    #print(userName)
                    return userName
            except  AttributeError:
                    #print('입력하신 아이디 혹은 비밀번호가 일치하지 않습니다.')
                    return False
        except urllib.request.Timeout as err:
            pass


        #logout_url = 'https://eclass.dongguk.edu/User.do?cmd=logoutUser'