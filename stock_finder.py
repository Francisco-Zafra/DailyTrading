from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options

def getStocks(num_stocks = 5):

    stocks = num_stocks

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://es.finance.yahoo.com/gainers')
    print('Headless Mozilla Initialiced')

    user = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[2]/form/button')
    user.click()
    print('First click done')

    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 500)")

    user = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[1]/table/thead/tr/th[4]/span')
    user.click()
    time.sleep(1)
    user.click()
    print('Data sorted')

    stocks_names = []

    for i in range(stocks):
        pos = i+1
        xpath = '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[1]/table/tbody/tr[' + str(pos) +']/td[1]/a'
        user = driver.find_element_by_xpath(xpath).text
        stocks_names.append(user)
    return (stocks_names)