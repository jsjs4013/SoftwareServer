from bs4 import BeautifulSoup
import requests

class EclassCheck:
    def check(self, ID, PW):
        #### LOGIN INFO ####
        login_info={
                'userDTO.userId':ID, # YourID 2014112025
                'userDTO.password':PW # YourPW wlsduddl14!
        }

        # 실제 로그인 하는 부분. Dict 형태로 로그인 정보를 담아 request 보냄. Request 생성 시 두번째 인자가 들어오게 되면 자동으로 Post Request로 인식
        login_url='https://eclass.dongguk.edu/User.do?cmd=loginUser' # 로그인 검증 페이지
        session = requests.session()
        r = session.post(login_url, data=login_info)

        #### LOGIN CHECK ####
        main_url = 'https://eclass.dongguk.edu/Main.do?cmd=viewEclassMain&mainMenuId=menu_00050&subMenuId=&menuType=menu'
        r = session.get(main_url)
        data = r.content.decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")

        try :  # 로그인 실패시 예외처리
                userName = soup.find('span', {'class': 'user'}).find('strong').text
                userName = userName.strip()  # 양쪽 끝의 공백 문자 제거
                session.close()
                return userName  # user 이름 가져오기
        except  AttributeError:
                return False