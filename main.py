from src.Driver import Driver
import schedule
import time


def job():
    with Driver() as bot:
        bot.find_all_job_postings_url(operation='update')
        bot.scrape_all_job_posting_url()
        bot.reset_scraper()
        print("Exiting...")


if __name__ == "__main__":
    start_time = input("Please enter the time [HH:MM 24h format] you want to start the script everyday: ")
    schedule.every().day.at(start_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)





