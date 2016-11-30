"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 django rest framework에서 model과 view사이의 연결통로 및 적절한 컨트롤러 역할을 한다.
 외래키의처리 데이터형식설정 create, update등 model과 view의 사이에서 적절한 다리역할을 한다.

 공통적으로 나타나는 클래스
 Meta class - 기본적인 반환형과 현재 serializer클래스가 사용하는 model을 설정한다.
"""

from bs4 import BeautifulSoup
import requests

class EclassCheck:
    def check(self, ID, PW):
        #### LOGIN INFO ####
        login_info={
                'id':ID, # YourID 2014112025
                'password':PW # YourPW wlsduddl14!
        }

        # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
        login_url='http://lib.dongguk.edu/studyroom/mainFullView?type=pc' # 로그인 검증 페이지
        session = requests.session()
        r = session.post(login_url, data=login_info, timeout=10)

        #### LOGIN CHECK ####
        main_url = 'http://lib.dongguk.edu/studyroom/mainFullView?type=pc'
        r = session.get(main_url)
        data = r.content.decode('euc-kr')
        soup = BeautifulSoup(data, "html.parser")

        try :  # 로그인 실패시 예외처리
                userName = soup.find('div', {'class': 'logout'}).find('span', {'class': 'name'}).text
                userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
                session.close()
                return userName  # user 이름 가져오기
        except  AttributeError:
                return False