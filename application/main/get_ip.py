# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def get_ip_info(ip_address):
    """
    通过爬虫获得用户IP地址的信息
    """
    # 模拟访问
    html_page = requests.get('http://ip.cn/index.php?ip=%s' % ip_address)

    # 解析
    soup = BeautifulSoup(html_page.content, "html5lib")
    html_code = soup.find_all('code')
    ip_area_message = html_code[1].get_text().strip()

    # 函数返回值
    return unicode(ip_area_message)
