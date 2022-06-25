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
import selenium.common.exceptions as SeleniumException

os.environ["PATH"] += r"C:\Document\Python\selenium_driver"
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# driver.get("https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=&locationstring=Alberta&sort=M")
driver.get("https://www.jobbank.gc.ca/jobsearch/jobposting/36466882?source=searchresults")
driver.implicitly_wait(10)
job_title = driver.find_element(By.CSS_SELECTOR, "span[property='title']").text
posted_date = driver.find_element(By.CSS_SELECTOR, "span[property='datePosted']").text.replace("Posted on ", "")
employer_name = driver.find_element(By.CSS_SELECTOR, "span[property='hiringOrganization']").text
job_location = driver.find_element(By.CSS_SELECTOR, "span[class='noc-location']").text
city = driver.find_element(By.CSS_SELECTOR, "span[property='addressLocality']").text
province = driver.find_element(By.CSS_SELECTOR, "span[property='addressRegion']").text
try:
    street = driver.find_element(By.CSS_SELECTOR, "span[property='streetAddress']").text
except SeleniumException.NoSuchElementException:
    street = "N/A"
try:
    postal_code = driver.find_element(By.CSS_SELECTOR, "span[property='postalCode']").text
except SeleniumException.NoSuchElementException:
    postal_code = "N/A"

job_requirement = driver.find_element(By.CSS_SELECTOR, "div.job-posting-detail-requirements ").text
try:
    print(job_requirement[job_requirement.index("Other benefits"):])
    print(job_requirement[:job_requirement.index("Other benefits")])
    benefits = job_requirement[job_requirement.index("Other benefits"):]
    job_requirement = job_requirement[:job_requirement.index("Other benefits")]
except ValueError:
    benefits = "N/A"


# salary_amount = soup.find("span", property="baseSalary", class_="attribute-value").getText()\
#     .removeprefix("$").replace("HOUR", "") + " for" + soup.find("span", property="workHours").getText()
# job_requirement = soup.find("div", property="skills").find_all("dd")
salary_amount = driver.find_element(By.CSS_SELECTOR, "span[property='value']").text\
    .replace("HOUR", "").replace("hourly", "").rstrip("\n")
employment_type = driver.find_element(By.CSS_SELECTOR, "span[property='employmentType']").text
work_hour = driver.find_element(By.CSS_SELECTOR, "span[property='workHours']").text

# We need to scrape the start date but its value is inside a span tag without any class name,or, id, or attributes
# I notice that tha span tag we need is inside an item list inside an unordered list
# There are either 7 or 9 list items
# If there are 7 list items then start date would be in list item 5
# If there are 9 list items then start date would be in list item 4
# The case for scraping vacancy information and job id are similar
list_items = driver.find_elements(By.CSS_SELECTOR, "ul.job-posting-brief.colcount-lg-2 > li")
if len(list_items) == 9:
    start_date = list_items[4].text.replace("Start date", "").lstrip("\n")
    vacancy = list_items[6].text.replace("vacancies", "").lstrip("\n")
    job_id = list_items[-1].text.replace("Source", "").replace("Job Bank #", "").lstrip("\n")
elif len(list_items) == 7:
    start_date = list_items[3].text.replace("Start date", "").lstrip("\n")
    vacancy = list_items[4].text.replace("vacancies", "").lstrip("\n")
    job_id = list_items[-1].text.replace("Source", "").replace("Job Bank #", "").lstrip("\n")
else:
    start_date = "N/A"
    vacancy = "N/A"
    job_id = "N/A"

print(job_title)
print(posted_date)
print(employer_name)
print(job_location)
print(street)
print(city)
print(province)
print(postal_code)
print(salary_amount)
print(employment_type)
print(work_hour)
print(start_date)
print(vacancy)
print(job_id)
print(job_requirement)
print(benefits)

print("test")


