"""Utilities for fetching articles.
Currently only affects Helsingin Sanomat. Scraping of the other sources can be done just using requests,
but HS needs a user to be logged in, as well as renders their articles using dynamic javascript,
thus requiring a Selenium session to enable fetching the articles.
"""
from typing import Union

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def prepare_session_hs(
        driver: Union[webdriver.Remote, webdriver.Firefox, webdriver.Chrome],
        username: str, password: str, max_web_driver_wait: int = 30):
    """Prepare a Selenium session for scraping articles from Helsingin Sanomat
    by logging in using the provided user id and password.

    Raises:
        TimeoutException: if the web driver is unable to find the elements it is looking for in 30 seconds.
                          May indicate changes to the loging page structure.

    Args:
        driver (Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome]): the Selenium session to use
        username (str): the username to log in as
        password (str): the password to use for logging in
        max_web_driver_wait (int): the maximum number of seconds to wait for the webdriver to
                                   render a page before failing (default: 30)

    """
    driver.get("https://www.hs.fi")
    cookies_frame = WebDriverWait(driver, max_web_driver_wait).until(
        lambda d: d.find_element(By.XPATH, "//iframe[@title='SP Consent Message']"))
    driver.switch_to.frame(cookies_frame)
    ok_button = WebDriverWait(driver, max_web_driver_wait).until(
        lambda d: d.find_element(By.XPATH, "//button[@title='OK']"))
    ok_button.click()
    driver.switch_to.default_content()
    login = WebDriverWait(driver, max_web_driver_wait).until(
        lambda d: d.find_element(By.XPATH, "//*[contains(text(), 'Kirjaudu')]"))
    driver.execute_script("arguments[0].click();", login)
    user = WebDriverWait(driver, max_web_driver_wait).until(
        lambda d: d.find_element(By.ID, "username"))
    user.send_keys(username)
    pas = driver.find_element(By.ID, "password")
    pas.send_keys(password)
    current_url = driver.current_url
    pas.submit()
    WebDriverWait(driver, max_web_driver_wait).until(EC.url_changes(current_url))


def fetch_article_hs(
        driver: Union[webdriver.Remote, webdriver.Firefox, webdriver.Chrome],
        url: str, max_web_driver_wait: int = 30) -> str:
    """Fetch the HTML of a single article using a Selenium session where
    prepare_session_hs has been called before.

    Args:
        driver (Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome]): the Selenium session to use.
        url (str): the HS article URL to fetch article content from
        max_web_driver_wait (int): the maximum number of seconds to wait for the webdriver to
                                   render a page before failing (default: 30)


    Raises:
        ValueError: If parsing the article fails, probably due to encountering a prevously unknown layout

    Returns:
        str: the HTML of the article
    """
    driver.get(url)
    try:
        dynamic_content = WebDriverWait(driver, max_web_driver_wait).until(
            lambda d: d.find_element(By.XPATH, "//div[@id='page-main-content']/following-sibling::*"))
        if dynamic_content.tag_name == 'iframe':
            driver.switch_to.frame(dynamic_content)
            if len(driver.find_elements(By.XPATH, "//div[@class='paywall-container']")) != 0:
                WebDriverWait(driver, max_web_driver_wait).until(lambda d: d.find_element(
                    By.XPATH, "//div[@class='paywall-content']|//div[@id='paid-content']"))
    except TimeoutException as timeout_exception:
        raise ValueError(
            f"Couldn't find the dynamic content I was looking for in {url}. There may be a class of HS articles we're not yet handling."
        ) from timeout_exception
    article = driver.find_element(By.XPATH, '/*').get_attribute('innerHTML')
    return article
