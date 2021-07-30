import requests
from bs4 import BeautifulSoup
import re
url = "https://m.blog.naver.com/engagedllls2/221495965553"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()  # 문제시 프로그램 종료
bs = BeautifulSoup(res.text, "html.parser")

img_div = bs.select('.se-image ')
image = []
for i in img_div:
    x = re.findall(r'(?=src)src=\"(?P<src>[^\"]+)', str(i))
    image += x
print(image)
