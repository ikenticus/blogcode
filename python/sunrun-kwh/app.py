import boto3
import json
import os
import sys

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from chalice import Chalice
app = Chalice(app_name=os.path.basename(os.getcwd()))
from pprint import pprint

class Struct:
    # simple non-recursive dict2obj class
    def __init__(self, **entries):
        self.__dict__.update(entries)

s3 = boto3.client('s3')
settings = json.load(open('chalicelib/settings.json'))
cfg = Struct(**settings)

class Struct:
    # simple non-recursive dict2obj class
    def __init__(self, **entries):
        self.__dict__.update(entries)

def email_alert(kwh, user):
    subject = 'Daily Production below %s kWh: %s' % (cfg.threshold, kwh)
    client = boto3.client('ses')
    response = client.send_email(
        Destination={
            'ToAddresses': [user]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=cfg.sender,
    )
    print(response)

def login(driver):
    driver.get(cfg.website + cfg.page['login'])
    #driver.find_element_by_css_selector('button[data-testid="email-signin"]').click()
    driver.implicitly_wait(10)
    #driver.find_element_by_id('email').send_keys(cfg.username)
    #driver.find_element_by_id('password').send_keys(cfg.password)
    #driver.find_element_by_css_selector('input.btn').click()
    driver.find_element_by_css_selector('input[name="email"]').send_keys(cfg.username)
    driver.find_element_by_css_selector('label[for="tos"] > span').click()
    driver.find_element_by_css_selector('button[type="submit"]').click()
    driver.implicitly_wait(10)

def scrape_output():
    # Open browser
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('--window-size=1920,1080')

    if sys.platform == 'darwin':
        driver = webdriver.Chrome(executable_path='macosx/chromedriver', options=chrome_options)
    else:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--start-maximized')
        chrome_options.binary_location = 'drivers/headless-chromium'
        driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

    login(driver)
    driver.implicitly_wait(1000)

    # click Generate then Download Report
    if sys.platform == 'darwin':
        driver.implicitly_wait(5000)
        driver.get(cfg.page['history'])
        driver.find_element_by_link_text('Export').click()
        #driver.find_element_by_css_selector('input.btn.submit').click()
        #driver.find_element_by_css_selector('a.btn').click()
        #driver.get(csv)

    '''
    csv = driver.find_element_by_css_selector('a.btn').get_attribute('href')
    kwh = driver.find_element_by_css_selector('div.system-production .total .ng-binding').get_attribute('innerHTML')
    print(kwh)
    if int(kwh) < int(cfg.threshold):
        email_alert(kwh, cfg.username)
    if int(kwh) == 0:
        email_alert(kwh, cfg.smsphone)
    '''

    if driver:
        driver.quit()

    '''
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe').get_attribute('id'))
    driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe').get_attribute('id'))
    driver.implicitly_wait(10)
    driver.find_element_by_link_text('Week').click()
    driver.implicitly_wait(1000)

    driver.find_element_by_css_selector('li.week').click()
    driver.implicitly_wait(1000)
    driver.find_element_by_link_text('Month').click()
    driver.implicitly_wait(1000)
    driver.find_element_by_link_text('Year').click()
    driver.implicitly_wait(10)
    driver.find_element_by_css_selector('allstates')
    '''

'''
@app.route('/')
def index():
    return {'Lambda': 'Chalice'}
'''

# cron(M H D M DoW Y)
@app.schedule('cron(0 12,18 * * ? *)')
def crontab(event):
    scrape_output()

if __name__ == '__main__':
    scrape_output()
