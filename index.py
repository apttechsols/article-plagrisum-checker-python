from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
driver = webdriver.Firefox(executable_path='C:/Users/arpit/Anaconda3/Lib/site-packages/selenium/webdriver/firefox/geckodriver.exe')
driver.implicitly_wait(30)
driver.maximize_window()

# Navigate to the application home page
driver.get("http://www.google.com")

# get the search textbox
search_field = driver.find_element_by_name('q')
print(search_field)
search_field.clear()
search_field.send_keys('Hello')

# close the browser window
driver.quit()