from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeDriverManager().install())

driver.get("https://google.com/")
print(driver.title)
driver.quit()
