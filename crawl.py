from bs4 import BeautifulSoup
from urllib import request, parse
from selenium import webdriver
from html import unescape
import time
import re
from settings import WEB_DRIVER_PATH
import csv
DATE = 0
TITLE = 1
TEXT = 2
IMAGE = 3


def make_basic_url(keyword, start, end):
    base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_blog&start='
    final_url = base_url + period + query + end
    return final_url


def get_blog_posting_urls(keyword, start, end, driver):
    basic_url = make_basic_url(keyword, start, end)
    blog_postings = []
    index = 1
    flag = True
    regex_href = r'.*https:\/\/m\.blog\.naver\.com\/(\w*\/\d*)'
    while(flag):
        # index에 해당하는 url
        url = basic_url + str(index)

        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(unescape(html), 'html.parser')
        links = bs.select('.api_txt_lines')
        for single_link in links:
            # single_link가 https://m.blg.naver.com을 포함하면 그걸 가져오자
            href = re.findall(regex_href, str(single_link))
            if href != None and href != []:
                if href in blog_postings:
                    flag = False
                    break
                else:
                    blog_postings.append(href)
        index += 15
    return blog_postings


def get_element(type, posting_addr, driver):
    url = 'https://m.blog.naver.com/' + posting_addr[0]
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

    switcher = {
        0: get_date,
        1: get_title,
        2: get_text,
        3: get_image
    }
    return switcher.get(type)(bs)


def get_date(bs):
    date_divs = bs.select('.se_date')
    date_divs2 = bs.select('.blog_date')
    date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))
    date2 = re.findall(r'(20[\d\s\.\:]*)', str(date_divs2))
    try:
        return date[0]
    except IndexError:
        try:
            date = date2[0].replace('\n', '')
            return date.rstrip()
        except:
            return None


def get_text(bs):
    # 네이버는 에디터에 따라 css selctor가 달라진다
    text_divs1 = bs.select('.se_textView > .se_textarea > span,p')
    text_divs2 = bs.select('.post_ct')
    if len(text_divs1) > len(text_divs2):
        final_text_div = text_divs1
    else:
        final_text_div = text_divs2

    text_for_blog = ''
    for text in final_text_div:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        if text not in text_for_blog:
            text_for_blog += text

    text_for_blog = text_for_blog.replace('\n', "")
    if text_for_blog[:3] == "로그인":
        text_for_blog = text_for_blog[40:]
    return text_for_blog.rstrip()


def get_title(bs):
    title_divs = bs.select('.se_title > .se_textView > .se_textarea')
    if title_divs == []:
        title_divs = bs.select('.tit_h3')
        if title_divs == []:
            title_divs = bs.select('.se-fs-')
    for title in title_divs:
        final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
        return final_title


def get_image(bs):
    img_div = bs.select('.se-component')
    image = []
    for i in img_div:
        x = re.findall(r'(?=src)src=\"(?P<src>[^\"]+)', str(i))
        image += x
    return image


def save_csv(list1, list2, list3, list4):
    f = open("diary.csv", "a", encoding="UTF-8", newline='')
    csvWriter = csv.writer(f)
    for val1, val2, val3, val4 in zip(list1, list2, list3, list4):
        if val1 and val2 and val3 and val4:
            csvWriter.writerow([val1, val2, val3, *val4])

    f.close()
