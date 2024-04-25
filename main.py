import time
import pyperclip
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import db
from webdriver_manager.chrome import ChromeDriverManager as ChromeDriverManager


# 자동화 메시지 방지
PROFILE = r'C:\remote-profile'  # Profile path
PORT = 9222  # Remote debugging port number
cmd = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd += f' --user-data-dir="{PROFILE}"'  # user-data-dir 지정
cmd += f' --remote-debugging-port={PORT}'  # remote debugging port 지정
subprocess.Popen(cmd)  # chrome 실행

options = ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920, 1080')
options.add_argument('headless')
options.add_experimental_option('debuggerAddress', f'127.0.0.1:{PORT}')  # 디버깅 포트로 연결
# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

#driver = webdriver.Chrome(options=options)

# 로그인 시작
driver.get(
    "https://account.weverse.io/ko/login/redirect?client_id=weverse&redirect_uri=https%3A%2F%2Fweverse.io%2FloginResult%3Ftopath%3D%252F")

time.sleep(1)
email = driver.find_element(By.CSS_SELECTOR,
                            '#__next > div > div.sc-8ab46e1a-2.eZEkTN > div > form > div.sc-ed52fcbe-0.dFIKnH > div.sc-ed52fcbe-8.eoxMAH > input').send_keys("5845434@gmail.com")
time.sleep(1)
password = driver.find_element(By.CSS_SELECTOR,
                               '#__next > div > div.sc-8ab46e1a-2.eZEkTN > div > form > div.sc-d0f94a43-0.bCrkf > div > div.sc-ed52fcbe-8.eoxMAH > input').send_keys("wldms6564!")


token = "7129846223:AAFd5Eqmf3oT8wNrYhDWMlUvsDVCaLRMPkw"
count = 0
namechange = 0
# 붙여넣기로 로그인
def copy_input(element, input):
    pyperclip.copy(input)
    element.click()
    #time.sleep(1)
    element.send_keys(Keys.CONTROL, 'v')


# try:
#     login_button = driver.find_element(By.CSS_SELECTOR,
#                                        "#__next > div > div.sc-8ab46e1a-2.eZEkTN > div > form > div.sc-58a7e114-0.cqmXWr > button")
#     login_button.click()
try:
    #print('=====except=======문')
    # copy_input(email, "5845434@gmail.com")
    # copy_input(password, "wldms6564!")
    login_button = driver.find_element(By.CSS_SELECTOR,
                                       "#__next > div > div.sc-8ab46e1a-2.eZEkTN > div > form > div.sc-58a7e114-0.cqmXWr > button")
    login_button.click()

except:
    1

# 닉네임이 변경된경우 프로필 페이지에서 새 닉네임 찾기
def find_id(team, id):
    address = "https://weverse.io/"+team+"/profile/"+id
    driver.get(address)
    try:
        time.sleep(2)
        test = driver.find_element(By.CSS_SELECTOR,"#root > div.App > div > div.body > div.CommunityNavigationLayoutView_content__\+9zMw > div > div.CommunityProfileContainerView_content__jvm33 > div.CommunityProfileInfoView_container__tirO7 > div.CommunityProfileInfoView_content_wrap__Ag9Gn > div.CommunityProfileInfoView_name_wrap__UtUx5 > h3")
    except:
        print('============= 닉네임 변경된경우 element를 찾지못함 ============= ')
        time.sleep(5)
        test = driver.find_element(By.CSS_SELECTOR,
                                   "#root > div.App > div > div.body > div.CommunityNavigationLayoutView_content__\+9zMw > div > div.CommunityProfileContainerView_content__jvm33 > div.CommunityProfileInfoView_container__tirO7 > div.CommunityProfileInfoView_content_wrap__Ag9Gn > div.CommunityProfileInfoView_name_wrap__UtUx5 > h3")

    return test.text

# 최근 알림 8건을 가져와 이전 알림과 비교해 새 알림이 있는지 확인
def new_notification(noti, data):
    new_data = []
    cnt = 0
    for i in data:
        if cnt == 6:
            break
        # 라이브, 공지, 미디어, 샵 제외
        if 'notice' not in i.attrs['href']:
            if 'media' not in i.attrs['href']:
                if 'live' not in i.attrs['href']:
                    if 'shop' not in i.attrs['href']:
                        #print(i.attrs['href'])
                        #print(i.get_text(strip=True))
                        new_data.append([i.attrs['href'], i.get_text(strip=True)])
                        cnt += 1
    #print('=====================================')
    new_data = new_data[1::]
    new_data = new_data[::-1]

    new_noti = []
    check = []

    for i in new_data:
        id = ''
        content = ''
        x = ''
        # 포스트
        if 'artist' in i[0] or 'fanpost' in i[0]:
            team = i[0].split('/')[1]
            nickname = i[1][1::].split('artist')[0]
            #print(team, nickname)
            temp = db.select_id(team, nickname)
            #print(team, nickname, 'temp:', temp)
            # 닉네임이 변경된 경우
            if temp == 0:
                temp = db.select_team_id(team)
                for j in temp:
                    v = find_id(team, j)
                    if v == nickname:
                        id = j
                        #print(j)
                        # 닉네임 업데이트
                        db.update_nickname(nickname, j)
                        time.sleep(1)
                        address = "https://weverse.io/"
                        driver.get(address)
                        global count
                        count = 0
                        global namechange
                        namechange = 'Y'
                        break
            else:
                id = temp

            if 'comment' in i[0]:
                x = i[1](strip=True).replace('artist', '')
                #print(x[x.index("댓글")::])
                content = x[x.index("댓글")::].replace('\n', '')
            else:
                x = i[1].replace('artist', '')
                #print(x[x.index("포스트")::])
                content = x[x.index("포스트")::].replace('\n', '')
        # 모먼트
        elif 'moment' in i[0]:
            #print(i.attrs['href'].split('/')[1], i.attrs['href'].split('/')[3])
            id = i[0].split('/')[3]
            x = i[1].replace('artist', '')
            if '모먼트' in x:
                #print(x[x.index("모먼트")::])
                content = x[x.index("모먼트")::].replace('\n', '')
            elif '댓글' in x:
                #print(x[x.index("댓글에")::])
                content = x[x.index("댓글에")::].replace('\n', '')
        #잠깐 주석
        #print('line166:', id, content, x)
        db.insert_noti(id, content, x)

        if id+content != '':
            new_noti.insert(0, id+content)
            cnt += 1

    if set(noti) == set(new_noti):
        #print('noti와 new noti가 같음')
        return 0
    else:
        result = [x for x in new_noti if x not in noti]
        #result = list(set(new_noti)-set(noti))
        #print('result', result)
        #result = result[::-1]
        return result


async def send_msg(id, msg):
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(id, msg)



time.sleep(2)
noti_button = driver.find_element(By.CSS_SELECTOR,
                                  "#root > div.App > div > div.GlobalLayoutView_header__1UkFL > header > div > div.HeaderView_action__QDUUD > div > button")


while 1:
    # 데이터 스크래핑 시작
    time.sleep(1)
    #print('닉네임바뀌었는지:', namechange)
    if namechange == 'Y':
        time.sleep(2)
        noti_button = driver.find_element(By.CSS_SELECTOR,
                                          "#root > div.App > div > div.GlobalLayoutView_header__1UkFL > header > div > div.HeaderView_action__QDUUD > div > button")
    if count == 0 or namechange == 'Y':
        try:
            time.sleep(1)
            noti_button.click()
            namechange = 0
        except:
            print('=========== noti_button.click()의 element를 못찾는 에러 발생하여 except문 실행 ==========')
            time.sleep(5)
            noti_button.click()
            namechange = 0
    else:
        try:
            time.sleep(1)
            noti_button.click()
            noti_button.click()
        except:
            print('=========== noti_button.click() * 2의 element를 못찾는 에러 발생하여 except문 실행 ==========')
            noti_button = driver.find_element(By.CSS_SELECTOR,
                                              "#root > div.App > div > div.GlobalLayoutView_header__1UkFL "
                                              "> header > div > div.HeaderView_action__QDUUD "
                                              "> div.HeaderNotificationWrapperView_notification__hCLgg > button")
            time.sleep(3)
            noti_button.click()
            time.sleep(3)
            noti_button.click()
    try:
        time.sleep(2)
        data = driver.find_element(By.CSS_SELECTOR,
                               "#root > div.App > div > div.GlobalLayoutView_header__1UkFL > header > div > div.HeaderView_action__QDUUD > div.HeaderNotificationWrapperView_notification__hCLgg > div > div > div.HeaderNotificationView_notification_area__oJsnB > div > div:nth-child(1) > ul > li:nth-child(1) > a > div.HeaderNotificationListView_notification_content_wrap__\+MRNf > div > div.HeaderNotificationListView_notification_content__g\+RAu > span")
    except:
        time.sleep(5)
        print('=========== data = driver의 element를 못찾는 에러 발생하여 except문 실행 ==========')
        data = driver.find_element(By.CSS_SELECTOR,
                                   "#root > div.App > div > div.GlobalLayoutView_header__1UkFL > header > div > div.HeaderView_action__QDUUD > div.HeaderNotificationWrapperView_notification__hCLgg > div > div > div.HeaderNotificationView_notification_area__oJsnB > div > div:nth-child(1) > ul > li:nth-child(1) > a > div.HeaderNotificationListView_notification_content_wrap__\+MRNf > div > div.HeaderNotificationListView_notification_content__g\+RAu > span")
    session = requests.Session()
    response = session.get('https://weverse.io/')
    html = response.text

    # Selenium에서 세션 쿠키 가져오기
    selenium_cookies = driver.get_cookies()

    # requests 세션 초기화
    session = requests.Session()

    # Selenium에서 가져온 세션 쿠키를 requests 세션에 추가
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # requests를 사용하여 추가 요청을 보냄
    response = session.get('https://weverse.io/')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = soup.select('a')
    #data = data[::-1]
    noti = db.select_noti()
    # print("=========================================")
    # print(noti)
    # print("+++++++++++++++++++++++++++++++++++++++++")
    # print(data)
    # print("=========================================")

    temp = new_notification(noti, data)

    #print("=========================================")
    if temp == 0 or len(temp) == 0:
        print('새 알림이 없습니다.', count, time.strftime('%Y.%m.%d %H:%M:%S'))
    else:
        print('새 알림이 있습니다.', count, time.strftime('%Y.%m.%d %H:%M:%S'))
        for i in temp:
            print(i)
            #print(i[:32])
            time.sleep(1)
            temp2 = db.select_sub_userid(i[:32])
            for j in temp2:
                print('메시지보낼 이용자:', j)
                asyncio.run(send_msg(j, db.select_origin_content(i)))
    count += 1
    time.sleep(4)
