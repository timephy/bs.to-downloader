from bs4 import BeautifulSoup
import requests


def get(url):
    return requests.get(url).text


def soup(html):
    return BeautifulSoup(html, "html.parser")


illegal_chars_none = "-|!?*<>\"\'\\/:"
illegal_chars_dot = [" - ", " | "]


def safe_filename(filename):
    for c in illegal_chars_dot:
        filename = filename.replace(c, ".")
    for c in illegal_chars_none:
        filename = filename.replace(c, "")
    return filename
