from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from pynput.mouse import Listener
import pyperclip
#from bs4 import BeautifulSoup

d = webdriver.Chrome(executable_path=r'chromedriver.exe')
d.maximize_window()

# web주소
# d.get('https://booking.naver.com/booking/6/bizes/167336') # test
d.get('https://booking.naver.com/booking/6/bizes/223362') # 아루히
time.sleep(1)

d.find_element_by_class_name('btn_srch').click()
time.sleep(1)
# id, pw 입력할 곳 찾기
tag_id = d.find_element_by_name('id')
tag_pw = d.find_element_by_name('pw')
tag_id.clear()
time.sleep(1)

# id 입력
tag_id.click()
pyperclip.copy('khyoon714')
tag_id.send_keys(Keys.CONTROL, 'v')
#time.sleep(1)

# pw 입력
tag_pw.click()
pyperclip.copy('rlrPrhdgkrrhk')
tag_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(0.5)

d.find_element_by_id('log.login').click()
time.sleep(2)

 #####

calendar_rows = d.find_element_by_class_name('tb_body').find_elements_by_tag_name('tr')
input_possible_day = [1, 1, 0, 0, 0, 0, 1] # 가능한 요일 1 / 불가능한 요일 0 입력 (일월화수목금토)
dates=[[],[],[],[],[],[],[]]

# 가능한 요일만 dates에 추가
for r in range(len(calendar_rows)):
    cols_in_a_row = calendar_rows[r].find_elements_by_tag_name('td')
    for c in range(len(cols_in_a_row)):
        if input_possible_day[c]:
            dates[c].append(cols_in_a_row[c])
dates = sum(dates, []) # 2차원 -> 1차원

dates_unselectable = d.find_elements_by_class_name('calendar-unselectable')
# selectable 날짜만 남기기
for i in dates_unselectable:
    for j in dates:
        if i == j:
            dates.remove(i)

input_unwanted_date = [9, 16, 22, 8] # 원하지 않는 날짜 입력
dates_unwanted = []
for da in dates:
    for date in input_unwanted_date:
        if da.find_element_by_class_name('num').get_attribute('innerHTML') == str(date):
            dates_unwanted.append(da)

# 원하지 않는 날짜 제외하기
for i in dates_unwanted:
    for j in dates:
        if i == j:
            dates.remove(i)
for i in range(len(dates)):
    print(dates[i].find_element_by_class_name('num').get_attribute('innerHTML'))   

#####

time_select = d.find_element_by_class_name('time_select')
time_select_anchor_fn = d.find_elements_by_class_name('select_anchor')[1].find_element_by_tag_name('i') # 시간 접었다 펼치는 버튼
input_time_to_reserve = {'오전': 1, '오후': 1} # 원하는 예약 시간대 입력
input_people_num = 1 # 원하는 사람 수 입력
time.sleep(0.5)


# dates 날짜, 시간대 순으로 가능한 날이 있는지 찾기
for s in dates:
    s.click()
    time.sleep(0.5)
    time_items = []
    if input_time_to_reserve['오전']:
        time_items.extend(time_select.find_element_by_class_name('am').find_elements_by_class_name('item'))
    if input_time_to_reserve['오후']:
        time_items.extend(time_select.find_element_by_class_name('pm').find_elements_by_class_name('item'))
    for i in range(len(time_items)):
        print(time_items[i].find_element_by_class_name('anchor').get_attribute('innerHTML'))   

    found = False
    for i in time_items: # 제일 처음 존재하는 빈 시간대 찾기
        if not i.find_element_by_class_name('none'): # 해당 시간대가 예약 가능하다면
            i.click() # 가능한 시간대 클릭
            time.sleep(0.05)
            
            # 현재 선택된 인원 수
            anchor_people_num = int(d.find_element_by_class_name('anchor_people').find_element_by_class_name('text_overflow').find_element_by_tag_name('span').get_attribute('innerHTML')[0])
            
            # 최소, 최대 수용 가능 인원 수
            if d.find_element_by_class_name('info_people').find_element_by_tag_name('span').get_attribute('innerHTML')[0] == '~':
                acceptable_min_people_num = 0
            else: 
                acceptable_min_people_num = int(d.find_element_by_class_name('info_people').find_element_by_tag_name('span').get_attribute('innerHTML')[0])
            acceptable_max_people_index = int(d.find_element_by_class_name('info_people').find_element_by_tag_name('span').get_attribute('innerHTML').index('명')-1)
            acceptable_max_people_num = int(d.find_element_by_class_name('info_people').find_element_by_tag_name('span').get_attribute('innerHTML')[acceptable_max_people_index])

            # 원하는 사람 수만큼 예약이 가능한지 확인하고 방문 인원 조정
            if (acceptable_max_people_num >= input_people_num and acceptable_min_people_num <= input_people_num): # 원하는 사람 수 예약 가능
                found = True
                btn_minus = d.find_elements_by_class_name('btn_plus_minus')[0]# 사람 수 + 버튼
                btn_plus = d.find_elements_by_class_name('btn_plus_minus')[1] # 사람 수 - 버튼
                number_to_change_people_num = input_people_num - anchor_people_num 
                if number_to_change_people_num > 0:
                    for i in range(number_to_change_people_num):
                        btn_plus.click()
                elif number_to_change_people_num < 0:
                    for i in range(number_to_change_people_num):
                        btn_minus.click()
            else: # 원하는 사람 수로 예약이 불가할 경우, 시간 탭을 펼쳐서 다음 가능 시간대를 찾음
                time_select_anchor_fn.click()
                time.sleep(0.05)
                
            if found:
                break
    if found:
        break
        
# 찾았는지 출력
if found:
    print('found!')
else: 
    print('not found ㅠㅠ')
