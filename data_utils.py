import subprocess
import threading
import urllib.request

from pip._internal.operations.prepare import File
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from urllib import request
import requests
import os
import os.path as osp
import shutil
import chromedriver_autoinstaller
from wand.api import library
import wand.color
import wand.image


# def data_crawling():
try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

driver.implicitly_wait(10)

# 오크 https://opensea.io/collection/ether-orcs
# driver.get('https://opensea.io/collection/chibi-fighters-weapons')
driver.get('https://opensea.io/collection/azuki')
print(' open driver ')
SCROLL_PAUSE_TIME = 3

# get scroll
driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

SAVE_FLAG = False
def timeout(limit_time): #timeout
    start = time.time()
    while True:
        if time.time() - start > limit_time or SAVE_FLAG:
            raise Exception

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)
img_folder = 'azuki/'

if not os.path.isdir(img_folder):  # 없으면 새로 생성하는 조건문
    os.mkdir(img_folder)
# #main > div > div > div.Blockreact__Block-sc-1xf18x6-0.elqhCm > div > div > div > div.AssetSearchView--results.collection--results > div.Blockreact__Block-sc-1xf18x6-0.elqhCm.AssetsSearchView--assets > div.fresnel-container.fresnel-greaterThanOrEqual-sm > div > div > div:nth-child(3) > div > article > a > div.Blockreact__Block-sc-1xf18x6-0.AssetCardContentreact__StyledContainer-sc-a8q9zx-0.dNtdmG.egubqN > div > div > div > img
# images = driver.find_element(by=By.CSS_SELECTOR, value=".Image--image")
count = 0
img_cnt = 0
while True:
    SAVE_FLAG = False
    timer = threading.Thread(target=timeout, args=(10,))

    try:
        count += 1
        if count > 3:
            print('scroll...')

            driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            count = 1
        time.sleep(2)
        timer.start()
        print(count)
        # 해골 '//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div/'
        # 오크 '//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div/div[{0}]/div/article/a/div[2]/div/div[1]/div[2]/div'
        #이미지의 XPath 를 붙여넣기 해준다. >> F12 를 눌러서 페이지 소스의 Element에서 찾아보면됨.
        imgName = driver.find_element(by=By.XPATH,
                                      value='//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div'
                                            '/div[{0}]/div/article/a/div[2]/div/div[1]/div[2]/div'.format(count)
                                        ).text.replace(' ','')
        print(imgName)

        # '//*[@id="main"]/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div'
        imgUrl = driver.find_element(by= By.XPATH,
                                     value='/html/body/div[1]/div/main/div/div/div[3]/div/div/div/div[3]/div[3]/div[2]/div/div'
                                           '/div[{0}]/div/article/a/div[1]/div/div/div/img'.format(count)).get_attribute("src")


        if os.path.isfile(img_folder + imgName + ".png"):
            if timer.is_alive():
                timer.join()
            continue # 이미 결과 파일 존재시, 패스
        print(imgUrl)

        ## SVG ...
        # svg = requests.get(imgUrl).text
        # write_text(svg, "img3/"+ imgName[0] + imgName[1] + ".svg")
        # img = request.urlretrieve(imgUrl, "PHI.svg")
        print('weapons/' + imgName + ".png")

        request.urlretrieve(imgUrl, 'C:/_workspace/gan_project/azuki/' + imgName + ".png") #저장할 이미지의 경로 지정
        print('Save images : ' + img_folder + imgName + ".png")
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

def svg_to_png(path : str):
    for file_name in os.listdir(path):
        print(osp.join(path ,file_name))
        with wand.image.Image(filename=osp.join(path ,file_name)) as image:
            image.save(filename=osp.join('png' ,file_name.split('\\')[-1][:-4] + '.png'))

# data_crawling()