from select import select
import sys
import time
import threading
import configparser
import datetime
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pickle

config = configparser.ConfigParser()
config.read('KKTIXBooker_Setting.ini', encoding="utf-8")

# 網址
url = config['web']['url']

# 參數
user_agent = config['web']['user_agent']

def KKTIXBooker():
    ticket_count = config['ticket_info']['ticket_count']
    ticket_seat = config['ticket_info']['ticket_seat']
    user_name = config['user']['user_name']
    user_password = config['user']['user_password']
    
    chrome_options = Options()
    
    chrome_options.add_argument('user-agent='+user_agent)
    chrome_options.add_experimental_option('detach',True)

    driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)

    driver.implicitly_wait(5)

    driver.get(url)
    
    #先到登入畫面
    driver.find_element('xpath','//*[@id="guestModal"]/div[2]/div/div[3]/a[2]').click()
    
    #輸入帳號
    driver.find_element('xpath','//*[@id="user_login"]').clear()
    driver.find_element('xpath','//*[@id="user_login"]').send_keys(user_name)
    
    #輸入密碼
    driver.find_element('xpath','//*[@id="user_password"]').clear()
    driver.find_element('xpath','//*[@id="user_password"]').send_keys(user_password)
    
    #登入
    driver.find_element('xpath','//*[@id="new_user"]/input[3]').click()
    
    #票數
    driver.find_element('xpath',f'//*[@id="{ticket_seat}"]/div/span[4]/input').clear()
    driver.find_element('xpath',f'//*[@id="{ticket_seat}"]/div/span[4]/input').send_keys(ticket_count)
    
    #已閱讀與同意
    driver.find_element('xpath','//*[@id="person_agree_terms"]').click()
    
    #下一步
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registrationsNewApp"]/div/div[5]/div[5]/button'))
    )
    element.click()
    
    #系統選位通知 點選知道了
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="infoModal"]/div[2]/div/div[1]/button'))
    )
    element.click()
    # driver.find_element('xpath','/*[@id="infoModal"]/div[2]/div/div[3]/button').click()
    
    #確認座位
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/button'))
    )
    element.click()
    
    #完成選位
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registrationsShowApp"]/div[2]/div/div/div/ng-include[2]/div/div/div/div[3]/div/div/div/div[1]/a'))
    )
    element.click()
    
    #確認訂票資料
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registrations_controller"]/div[4]/div[2]/div/div[5]/a'))
    )
    element.click()
    
    
if __name__ == '__main__':
    KKTIXBooker()
