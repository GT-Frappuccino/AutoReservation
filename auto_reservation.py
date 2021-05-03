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
