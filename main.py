from bs4 import BeautifulSoup
import requests
# import lxml
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

os.environ["PATH"] += r"C:\Document\Python\selenium_driver"
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# driver.get("https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=&locationstring=Alberta&sort=M")
driver.get("https://www.jobbank.gc.ca/jobsearch/jobposting/36425756?source=searchresults")
driver.implicitly_wait(10)
job_title = driver.find_element(By.CSS_SELECTOR, "span[property='title']").text
print(job_title)
posted_date = driver.find_element(By.CSS_SELECTOR, "span[property='datePosted']").text.replace("Posted on ", "")
print(posted_date)
employer_name = driver.find_element(By.CSS_SELECTOR, "span[property='hiringOrganization']").text
print(employer_name)

# employer_name = soup.find("span", property="hiringOrganization").find(property="name").getText()
# job_location = soup.find("span", property="address", class_="city").getText()



# WebDriverWait(driver, 30).until(
#     EC.visibility_of_element_located((By.XPATH, "//div[@class='btn btn-default btn-sm btn-block'"
#                                                 " and contains(.,'Show more results')]"))
# )
# while True:
#     try:
#         WebDriverWait(driver, 30).until(
#             EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-default btn-sm btn-block'"
#                                                         " and contains(.,'Show more results')]"))
#         )
#         print("MORE button clicked")
#     except TimeoutException:
#         print("Time Out")
#         break









# def extract_jobs(job_position="", job_location="", parser="html.parser"):
#     url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={job_position}&locationstring={job_location}"
#     response = requests.get(url=url).text
#     soup = BeautifulSoup(response, parser)
#     return soup
#
#
# soup = extract_jobs(parser="lxml")
# print(soup)

# response = requests.get(url="https://www.jobbank.gc.ca/jobsearch/jobposting/36411535?source=searchresults")
# job_bank_gc_ca = response.text
#
# soup = BeautifulSoup(job_bank_gc_ca, "html.parser")
# job_title = soup.find("span", property="title").getText()
# posted_date = soup.find("span", property="datePosted", class_="date").getText()
# employer_name = soup.find("span", property="hiringOrganization").find(property="name").getText()
# job_location = soup.find("span", property="address", class_="city").getText()
# salary_amount = soup.find("span", property="baseSalary", class_="attribute-value").getText()\
#     .removeprefix("$").replace("HOUR", "") + " for" + soup.find("span", property="workHours").getText()
# job_requirement = soup.find("div", property="skills").find_all("dd")
# for dd in job_requirement:
#     print(dd.getText())
#
# print(job_title)
# print(posted_date)
# print(employer_name)
# print(job_location)
# print(salary_amount)
# print(job_requirement)
