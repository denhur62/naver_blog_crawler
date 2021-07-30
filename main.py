from crawl import *
from settings import *

webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')
driver = webdriver.Chrome(WEB_DRIVER_PATH)
index = 0
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    blog_posting_urls = get_blog_posting_urls(
        dining_name, start_date, end_date, driver)
    # blog_postings의 date, text, title 가져오기
    dates = []
    titles = []
    texts = []
    cnt = 0
    for posting_addr in blog_posting_urls:
        date = get_element(DATE, posting_addr, driver)
        dates.append(date)

        text = get_element(TEXT, posting_addr, driver)
        texts.append(text)

        title = get_element(TITLE, posting_addr, driver)
        titles.append(title)
    # csv에 저장하기
    save_csv(dates, titles, texts)
