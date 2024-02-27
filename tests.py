from main import LinkedinScraper
import threading

scraper = LinkedinScraper()

# just to keep the browser open and session valid as long as possible
threading.Thread(target=scraper.stay_alive).start()


def test_login():
    scraper.login()


if __name__ == '__main__':
    test_login()
