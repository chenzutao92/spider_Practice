from selenium import webdriver
import time
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()
browser.maximize_window()
# browser.get('http://bbs.9game.cn/thread-29849785-1-1.html')
browser.get('http://api.open.uc.cn/cas/login?client_id=191&v=1.1&redirect_uri=http%3A%2F%2Fbbs.9game.cn%2Fplugin.php%3Fid%3Dcas%3AuserPlatformCallback%26act%3D2%26requestid%3Dfedd846e-8528-44e6-a872-da40d1e327a8&display=pc')
# time.sleep(5)
# # cookies = browser.get_cookies()
# # print(cookies)
# # browser.find_element_by_css_selector("#newspecial > img").click()
browser.find_element_by_css_selector("#loginName").send_keys("18924220519")
browser.find_element_by_css_selector("#password").send_keys("chenzutao0908")
# # browser.find_element_by_css_selector("nc_1__bg").
dragger = browser.find_element_by_css_selector("#nc_1_n1z")
actions = ActionChains(browser)
# # action.click_and_hold(dragger).perform()
# for index in range(100):

actions.drag_and_drop_by_offset(dragger, 258, 0).perform()

time.sleep(1)
#
# cookies = browser.get_cookies()
# print(cookies)
# browser.find_element_by_css_selector("#post_reply").click()
