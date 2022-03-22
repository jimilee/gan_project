import subprocess
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from urllib import request
import os
import shutil
import chromedriver_autoinstaller

try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동


option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)

driver.implicitly_wait(10)
search = "cryptoskulls"
# driver = webdriver.Chrome('C:/chrome/chromedriver.exe')
driver.get('https://opensea.io/collection/cryptoskulls')
# elem = driver.find_element_by_name("q")
# elem.send_keys(search)
# elem.send_keys(Keys.RETURN)
print(' open driver ')
SCROLL_PAUSE_TIME = 3

# get scroll
driver.execute_script("window.scrollTo(0, 1000);")

SAVE_FLAG = False
def timeout(limit_time): #timeout
    start = time.time()
    while True:
        if time.time() - start > limit_time or SAVE_FLAG:
            raise Exception


count = 0

img_folder = './img2'

if not os.path.isdir(img_folder):  # 없으면 새로 생성하는 조건문
    os.mkdir(img_folder)
# #main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child(3) > div > article > a > div.Blockreact__Block-sc-1xf18x6-0.AssetCardContentreact__StyledContainer-sc-a8q9zx-0.dNtdmG.egubqN > div > div > div > img
# images = driver.find_element(by=By.CSS_SELECTOR, value=".Image--image")
count = 0
img_cnt = 0
while True:
    SAVE_FLAG = False
    timer = threading.Thread(target=timeout, args=(5,))
    try:
        count += 1
        if count > 6:
            print('scroll...')
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            count = 0
        time.sleep(2)
        timer.start()
        print(count)
        #이미지의 XPath 를 붙여넣기 해준다. >> F12 를 눌러서 페이지 소스의 Element에서 찾아보면됨.
        imgUrl = driver.find_element(by= By.XPATH,
                                     value='//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div/'
                                           'div[{0}]/div/article/a/div[1]/div/div/div/img'.format(count)
                                              ).get_attribute("src")
        request.urlretrieve(imgUrl, "img2/"+ search + "_{0:04}".format(img_cnt) + ".png") #저장할 이미지의 경로 지정
        print('Save images : ' + "img2/"+ search + "_{0:04}".format(img_cnt) + ".png")
        SAVE_FLAG = True
        img_cnt += 1
        if timer.is_alive():
            timer.join()
    except Exception as e:
        if timer.is_alive():
            timer.join()
        pass

print('driver end. Total images : ', count)
driver.close()