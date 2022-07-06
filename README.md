# gov-ca-job-bank-scraping
This application scrapes the Job Bank website of Government of Canada for job postings. The application use Selenium to navigate through the Job Bank website and scrape the information of matched job postings then create and store those information in a JSON file in docs folder.

Requirements:

1. This application use Selenium to scrape, therefore, you need to download a browser's driver of your choice to your computer directory before being able to use the application. The default settings use Chrome browser (Get the driver at this site: https://chromedriver.chromium.org/downloads). If you use other browser, then change the class inheritance in module Driver.py, line 10. (E.g. webdriver.Edge). Note: remember to change to the path directory that store your driver in module Driver.py, line 16.

2. You will need the followings:
  Selenium: https://selenium-python.readthedocs.io/installation.html#installing-python-bindings-for-selenium
  Schedule: https://schedule.readthedocs.io/en/stable/

Brief Tutorial:

The application main code is in the Driver class. The class has two main method:

  a/ find_all_job_postings_url()
    """
    Find all the postings urls and store them in the url_list attribute of the class
    :param operation: 'update' or 'all'; control whether to scrape just a part of the database; default="update"
    :param date_posted: control how new the postings are in terms of days,
    this param is not used if operation is set to 'all'; default=2
    :param location: valid inputs are Canadian province alpha code or 'Canada';
    determine the location of the posting; default="AB"
    """
    
  b/ scrape_all_job_posting_url():
    """
    Access each job posting url and scrape specific information
    then append them to the job_postings attribute (dictionary)
    """
