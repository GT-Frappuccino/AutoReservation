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
