# coding=utf-8
from tools import get_soup


if __name__=="__main__":
    url = "http://hotel.meituan.com/108312797/?ci=2018-03-25&co=2018-03-29"
    soup = get_soup(url)
    p = soup.find_all("em", {"class": "price-number"})
    for i in p:
        print i.text
