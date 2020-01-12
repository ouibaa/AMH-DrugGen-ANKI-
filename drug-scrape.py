from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path="./chromedriver.exe") #??

driver.get("https://amhonline-amh-net-au.ezproxy1.library.usyd.edu.au/drugs/monographs")
time.sleep(10);

time.sleep(15);

content = driver.find_elements_by_class_name('browse-by')
for i in range(0, 25):
  print(content[i])




