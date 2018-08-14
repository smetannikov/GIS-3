url2 = 'https://sisfor.osinfor.gob.pe/visor/geoObsROJO/20130002429|1'

import requests

from selenium.webdriver.common.action_chains import ActionChains

r = requests.get(url2).text


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\server\chromedriver.exe')
driver.get(url2)

element = driver.find_element_by_id("btnterminoUso").click()
element.send_keys("", Keys.ARROW_DOWN)

element1 = driver.find_element_by_id("mapDiv_graphics_layer").click()
element.send_keys("", Keys.ARROW_DOWN)

action = ActionChains(driver)
action.move_to_element(element1)            
action.click().perform()