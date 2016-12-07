"""
 Author - 문주원(Moon Joowon)
 StudentID - 2014112022
 Major - Computer science engineering

 학교도서관페이지에 로그인을하여 우리학교 학생임을 인증시켜주기위해 필요한 파일이다.
"""

from bs4 import BeautifulSoup
import requests

"""
 학교 홈페이지에 로그인하여 학교의 관게자임을 서버가 인식하기위하여 필요한 클래스이다.
 메인 서버에서 학교홈페이지로 session을 저장하여 POST형식으로 id와 password를 보낸다.
 session을 활용하여 로그인이 완료되었는지 확인한다.
"""
class EclassCheck:
    def check(self, ID, PW):
        #### LOGIN INFO ####
        login_info={
                'id':ID,
                'password':PW
        }

        # 로그인 검증 페이지
        login_url='http://lib.dongguk.edu/studyroom/mainFullView?type=pc'
        session = requests.session()
        r = session.post(login_url, data=login_info, timeout=30)

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