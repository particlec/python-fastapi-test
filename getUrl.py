import requests
from bs4 import BeautifulSoup

url = 'https://support.huaweicloud.com/api-iothub/iot_06_v5_0003.html'

# 请求头文件
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36 '
}
res = requests.get(url=url, headers=headers)
res.encoding = "utf-8"  #
# step_3:获取响应数据:通过调用响应对象的text属性
page_text = res.text

bs1 = BeautifulSoup(page_text, 'html.parser')

html_list =bs1.find_all('td', attrs={'class': 'cellrowborder'})


for i in html_list:
    a = i.find('a', href=True)
    if a:
        url = a.attrs['href']
        print(url)
