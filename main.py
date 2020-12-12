import logging
import sys
from selenium import webdriver
import random

# super bad setup info, but here it is
# pip install chromedriver selenium
# https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/
# put "cromedriver.exe" in your path, i just used c:\windows\system32


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    log_name = "{0}_log.txt".format(name)
    handler = logging.FileHandler(log_name, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


def hit_poll(loop_number, url_path, poll_option):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # OR options.add_argument("--disable-gpu")

        web = webdriver.Chrome('chromedriver', options=options)
        web.get(url_path)

        # pick our radio button to vote on.
        xpath = '//*[@id="choice{0}"]'.format(str(poll_option))
        poll_choice = web.find_element_by_xpath(xpath)
        poll_choice.click()

        # now to hit the submit/vote button!
        xpath = '/html/body/div[2]/div/div[2]/form/input[11]'
        poll_choice = web.find_element_by_xpath(xpath)
        poll_choice.click()

        # poll results  xpath
        # /html/body/div[2]/div/div[1]/h1
        get_conf_div_text = web.find_element_by_xpath("/html/body/div[2]/div/div[1]/h1")
        if get_conf_div_text.text == "Poll Results":
            log.info("Automated voting successfully completed. [LOOP: {0}]".format(loop_number))
        else:
            log.info("Automated voting failed for some reason.... [LOOP: {0}]".format(loop_number))

    except Exception as e:
        log.error("Loop: {0} - Error: {1}".format(loop_number, e))
    finally:
        web.close()


if __name__ == '__main__':
    log = setup_custom_logger("PollTaker")

    i = 0
    while i < 16947:
        # min:max should be passed in, not static.
        vote_choice = random.randint(1, 9)
        hit_poll(i, 'https://benspelledabc.me/polls/8/', vote_choice)
        i += 1

