



def customFuncForCp(**kwargs):

    BeautifulSoup = kwargs.get("BeautifulSoup")
    request = kwargs.get("request")

    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
    html = request(method="GET",url="https://kjh.55128.cn/history_js11x5.aspx",headers=headers,timeout=5).text
    soup = BeautifulSoup(html,'html.parser')

    curterm = soup.find_all('span', class_='kaij-qs')[0].string
    curno = ""
    for item in [ item.string for item in soup.find_all('div',class_="kaij-cartoon")[0].children if item != '\n']:
        curno += "{},".format(item)
    curno = curno[:-1]

    return curterm,curno,None

import re,json
from requests import request
print(customFuncForCp(request,re,json))