from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selenium_exception
import os
import json


class Driver(webdriver.Chrome):
    """
    Represents an automatic web src that navigates through the Job Bank site
    and scrape desired information
    """

    def __init__(self, driver_path=r"C:\Document\Python\selenium_driver", teardown=False):
        """
        Initialize a web driver with all its parent Class attributes and methods,
        and with the browser's driver, location of job postings, and job posting date
        :param driver_path: directory in your computer that contains your browser's driver
        :param teardown: boolean; whether to shut down the browser automatically after finishing
        """
        self.teardown = teardown
        self.driver_path = driver_path
        self.url_list = []
        self.job_postings = {}
        self.job_posting_index = 1
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)  # Keep the browser opened after the script is finished
        super().__init__(options=options)
        self.implicitly_wait(30)  # Wait at most 30s before execute a task
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Method to exit the test after completing all task. It is disabled by default"""
        if self.teardown:
            self.quit()

    def clear_all_url(self):
        self.url_list = []
        self.job_postings = {}
        self.job_posting_index = 1

    def find_all_job_postings_url(self, operation="update", date_posted="2", location="AB"):
        """
        Find all the postings urls and store them in the url_list attribute of the class
        :param operation: 'update' or 'all'; control whether to scrape just a part of the database; default="update"
        :param date_posted: control how new the postings are in terms of days,
        this param is not used if operation is set to 'all'; default=2
        :param location: valid inputs are Canadian province alpha code or 'Canada';
        determine the location of the posting; default="AB"
        """
        if operation == "update" and isinstance(location, str):
            self.get(f"https://www.jobbank.gc.ca/jobsearch/jobsearch?"
                     f"fage={str(date_posted)}&sort=M&fprov={location}&fsrc=16")
            # fsrc=16 means only verified job postings will be shown
        elif operation == "all" and isinstance(location, str):
            self.get(f"https://www.jobbank.gc.ca/jobsearch/jobsearch?"
                     f"sort=M&fprov={location}&fsrc=16")  # fsrc=16 means only verified job postings will be shown
        else:
            print("Invalid input! Please check your arguments!")
            self.teardown = True
        there_more = True
        while there_more:
            try:
                WebDriverWait(self, 10, ignored_exceptions=selenium_exception.StaleElementReferenceException) \
                    .until(
                    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[id='moreresultbutton']"))
                ).click()  # Wait 10s for button to show up before raising an exception
            except selenium_exception.TimeoutException:
                print("Extracted All Postings")
                there_more = False
        articles = self.find_elements(By.CSS_SELECTOR, "div[id='ajaxupdateform:result_block'] > article > a")
        for article in articles:
            self.url_list.append(article.get_attribute("href"))
        print(f"The total number of job postings is: {len(self.url_list)}")

    def scrape_all_job_posting_url(self):
        print(f"The total number of job postings is: {len(self.url_list)}")
        for url in self.url_list:
            print(f"Begin scraping url: {self.job_posting_index}")
            try:
                self.get(url)
                self.implicitly_wait(10)
                job_title = self.find_element(By.CSS_SELECTOR, "span[property='title']").text
                posted_date = self.find_element(By.CSS_SELECTOR, "span[property='datePosted']")\
                    .text.replace("Posted on ", "")
                employer_name = self.find_element(By.CSS_SELECTOR, "span[property='hiringOrganization']").text
                job_location = self.find_element(By.CSS_SELECTOR, "span[class='noc-location']").text
                city = self.find_element(By.CSS_SELECTOR, "span[property='addressLocality']").text
                province = self.find_element(By.CSS_SELECTOR, "span[property='addressRegion']").text
                job_requirement = self.find_element(By.CSS_SELECTOR, "div.job-posting-detail-requirements ").text
                try:
                    street = self.find_element(By.CSS_SELECTOR, "span[property='streetAddress']").text
                except selenium_exception.NoSuchElementException:
                    street = "N/A"
                try:
                    postal_code = self.find_element(By.CSS_SELECTOR, "span[property='postalCode']").text
                except selenium_exception.NoSuchElementException:
                    postal_code = "N/A"
                try:
                    # print(job_requirement[job_requirement.index("Other benefits"):])
                    # print(job_requirement[:job_requirement.index("Other benefits")])
                    benefits = job_requirement[job_requirement.index("Other benefits"):]
                    job_requirement = job_requirement[:job_requirement.index("Other benefits")]
                except ValueError:
                    benefits = "N/A"
                try:
                    salary_amount = self.find_element(By.CSS_SELECTOR, "span[property='value']").text \
                        .replace("HOUR", "").replace("hourly", "").rstrip("\n")
                except selenium_exception.NoSuchElementException:
                    salary_amount = self.find_element(By.CSS_SELECTOR, "span[property='baseSalary']").text
                try:
                    employment_type = self.find_element(By.CSS_SELECTOR, "span[property='employmentType']").text
                except selenium_exception.NoSuchElementException:
                    employment_type = "N/A"
                try:
                    work_hour = self.find_element(By.CSS_SELECTOR, "span[property='workHours']").text
                except selenium_exception.NoSuchElementException:
                    work_hour = "N/A"
                """
                We need to scrape the start date but its value is inside a span tag without any class name,
                or, id, or attributes
                I notice that tha span tag we need is inside an item list inside an unordered list
                There are either 7 or 9 list items
                If there are 7 list items then start date would be in list item 5
                If there are 9 list items then start date would be in list item 4
                The case for scraping vacancy information and job id are similar
                """
                list_items = self.find_elements(By.CSS_SELECTOR, "ul.job-posting-brief.colcount-lg-2 > li")
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
                self.job_postings[self.job_posting_index] = {
                    "source_url": url,
                    "job_title": job_title,
                    "posted_date": posted_date,
                    "employer_name": employer_name,
                    "job_location": job_location,
                    "street": street,
                    "city": city,
                    "province": province,
                    "postal_code": postal_code,
                    "salary_amount": salary_amount,
                    "employment_type": employment_type,
                    "work_hour": work_hour,
                    "start_date": start_date,
                    "vacancy": vacancy,
                    "job_id": job_id,
                    "job_requirement": job_requirement,
                    "benefits": benefits,
                }
                print(f"Finished scraping url: {self.job_posting_index}")
                self.job_posting_index += 1
            except Exception:
                with open("./docs/job_postings_incomplete.json", "w") as file:
                    json.dump(self.job_postings, file)
                print(f"Encounter some error.... Skipping url {self.job_posting_index}...")
                continue
        with open("./docs/job_postings_complete.json", "w") as file:
            json.dump(self.job_postings, file)
        print("DONE SCRAPING!")
