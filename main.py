from crawl import *
from settings import *

webdriver_options = webdriver.ChromeOptions()
webdriver_options.add_argument('headless')
driver = webdriver.Chrome('chromedriver', options=webdriver_options)
index = 0
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    blog_posting_urls = get_blog_posting_urls(
        dining_name, start_date, end_date, driver)
    # blog_postings의 date, text, title 가져오기
    dates = []
    titles = []
    texts = []
    images = []
    cnt = 0
    post_len = len(blog_posting_urls)
    window_url = blog_posting_urls
    for posting_addr in blog_posting_urls:
        cnt += 1
        date = get_element(DATE, posting_addr, driver)
        dates.append(date)

        text = get_element(TEXT, posting_addr, driver)
        texts.append(text)

        title = get_element(TITLE, posting_addr, driver)
        titles.append(title)

        #image = get_element(IMAGE, posting_addr, driver)
        # images.append(image)
        # csv 중간 저장
        if cnt % 50 == 0:
            save_csv(titles, dates, texts, window_url)
            dates = []
            titles = []
            texts = []
            images = []
            window_url = window_url[50:]
        if cnt % 10 == 0:
            print(cnt, post_len)
    save_csv(titles, dates, texts, window_url)
