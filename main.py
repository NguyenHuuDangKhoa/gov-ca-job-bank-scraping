from src.Driver import Driver
import schedule
import time


def job():
    with Driver() as bot:
        bot.find_all_job_postings_url(operation='update')
        bot.scrape_all_job_posting_url()
        print("Exiting...")


if __name__ == "__main__":
    schedule.every().day.at("13:32").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


# from bs4 import BeautifulSoup
# import requests
# import lxml
# import json
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import selenium.common.exceptions as SeleniumException
# BASE_URL = "https://www.jobbank.gc.ca/jobsearch/jobsearch?fage=2&sort=M&fprov=AB&fsrc=16"
#
# os.environ["PATH"] += r"C:\Document\Python\selenium_driver"
# options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument("--start-maximized")
# driver = webdriver.Chrome(options=options)
#
# driver.get(BASE_URL)
# driver.implicitly_wait(10)
#
# there_more = True
# show_more_button = driver.find_element(By.CSS_SELECTOR, "button[id='moreresultbutton']")
# show_more_button.click()
#
# while there_more:
#     try:
#         WebDriverWait(driver, 10, ignored_exceptions=SeleniumException.StaleElementReferenceException)\
#             .until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR,  "button[id='moreresultbutton']"))
#         ).click()
#     except SeleniumException.TimeoutException:
#         print("There's no more result")
#         there_more = False


# articles = driver.find_elements(By.CSS_SELECTOR, "div[id='ajaxupdateform:result_block'] > article > a")
# url_list = []
# for article in articles:
#     url_list.append(article.get_attribute("href"))
# print(len(url_list))
# job_postings = {}
# job_posting_index = 1
# try:
#     for url in url_list:
#         print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#         print(f"{job_posting_index} begin!")
#         driver.get(url)
#         driver.implicitly_wait(10)
#         job_title = driver.find_element(By.CSS_SELECTOR, "span[property='title']").text
#         posted_date = driver.find_element(By.CSS_SELECTOR,
#                                           "span[property='datePosted']").text.replace("Posted on ", "")
#         employer_name = driver.find_element(By.CSS_SELECTOR, "span[property='hiringOrganization']").text
#         job_location = driver.find_element(By.CSS_SELECTOR, "span[class='noc-location']").text
#         city = driver.find_element(By.CSS_SELECTOR, "span[property='addressLocality']").text
#         province = driver.find_element(By.CSS_SELECTOR, "span[property='addressRegion']").text
#         try:
#             street = driver.find_element(By.CSS_SELECTOR, "span[property='streetAddress']").text
#         except SeleniumException.NoSuchElementException:
#             street = "N/A"
#         try:
#             postal_code = driver.find_element(By.CSS_SELECTOR, "span[property='postalCode']").text
#         except SeleniumException.NoSuchElementException:
#             postal_code = "N/A"
#
#         job_requirement = driver.find_element(By.CSS_SELECTOR, "div.job-posting-detail-requirements ").text
#         try:
#             print(job_requirement[job_requirement.index("Other benefits"):])
#             print(job_requirement[:job_requirement.index("Other benefits")])
#             benefits = job_requirement[job_requirement.index("Other benefits"):]
#             job_requirement = job_requirement[:job_requirement.index("Other benefits")]
#         except ValueError:
#             benefits = "N/A"
#
#         # salary_amount = soup.find("span", property="baseSalary", class_="attribute-value").getText()\
#         #     .removeprefix("$").replace("HOUR", "") + " for" + soup.find("span", property="workHours").getText()
#         # job_requirement = soup.find("div", property="skills").find_all("dd")
#         try:
#             salary_amount = driver.find_element(By.CSS_SELECTOR, "span[property='value']").text \
#                 .replace("HOUR", "").replace("hourly", "").rstrip("\n")
#         except SeleniumException.NoSuchElementException:
#             salary_amount = driver.find_element(By.CSS_SELECTOR, "span[property='baseSalary']").text
#         employment_type = driver.find_element(By.CSS_SELECTOR, "span[property='employmentType']").text
#         work_hour = driver.find_element(By.CSS_SELECTOR, "span[property='workHours']").text
#
#         # We need to scrape the start date but its value is inside a span tag without any class name,
#         # or, id, or attributes
#         # I notice that tha span tag we need is inside an item list inside an unordered list
#         # There are either 7 or 9 list items
#         # If there are 7 list items then start date would be in list item 5
#         # If there are 9 list items then start date would be in list item 4
#         # The case for scraping vacancy information and job id are similar
#         list_items = driver.find_elements(By.CSS_SELECTOR, "ul.job-posting-brief.colcount-lg-2 > li")
#         if len(list_items) == 9:
#             start_date = list_items[4].text.replace("Start date", "").lstrip("\n")
#             vacancy = list_items[6].text.replace("vacancies", "").lstrip("\n")
#             job_id = list_items[-1].text.replace("Source", "").replace("Job Bank #", "").lstrip("\n")
#         elif len(list_items) == 7:
#             start_date = list_items[3].text.replace("Start date", "").lstrip("\n")
#             vacancy = list_items[4].text.replace("vacancies", "").lstrip("\n")
#             job_id = list_items[-1].text.replace("Source", "").replace("Job Bank #", "").lstrip("\n")
#         else:
#             start_date = "N/A"
#             vacancy = "N/A"
#             job_id = "N/A"
#
#         # print(job_title)
#         # print(posted_date)
#         # print(employer_name)
#         # print(job_location)
#         # print(street)
#         # print(city)
#         # print(province)
#         # print(postal_code)
#         # print(salary_amount)
#         # print(employment_type)
#         # print(work_hour)
#         # print(start_date)
#         # print(vacancy)
#         # print(job_id)
#         # print(job_requirement)
#         # print(benefits)
#         print(f"{job_posting_index} finished!")
#
#         job_postings[job_posting_index] = {
#             "source_url": url,
#             "job_title": job_title,
#             "posted_date": posted_date,
#             "employer_name": employer_name,
#             "job_location": job_location,
#             "street": street,
#             "city": city,
#             "province": province,
#             "postal_code": postal_code,
#             "salary_amount": salary_amount,
#             "employment_type": employment_type,
#             "work_hour": work_hour,
#             "start_date": start_date,
#             "vacancy": vacancy,
#             "job_id": job_id,
#             "job_requirement": job_requirement,
#             "benefits": benefits,
#         }
#         job_posting_index += 1
#         # time.sleep(0.5)
# except:
#     with open("job_postings_incomplete.json", "w") as file:
#         json.dump(job_postings, file)
# finally:
#     with open("job_postings_complete.json", "w") as file:
#         json.dump(job_postings, file)
# print("Done!")





