



def customFuncForCp(**kwargs):

    request = kwargs.get("request")
    re = kwargs.get("re")
    json = kwargs.get("json")
    ut = kwargs.get("ut")()
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
    html = request(method="GET",url="https://www.52cp.cn/xjssc/home.html",headers=headers,timeout=5).text
    pattern = re.compile(r"DataInfo?.*?;")
    res = json.loads(pattern.findall(html)[0].split('=')[1].replace("'","").replace(";",""))
    curterm = res['now']['expect']
    curno = res['now']['opencode']
    nextterm = res['next']['expect']
    nexttime = ut.string_to_timestamp(res['next']['opentime'].strip())
    return curterm,curno,nextterm,nexttime

if __name__ == '__main__':
    from lib.utils.mytime import UtilTime
    import json, re, random, time
    from requests import request
    from bs4 import BeautifulSoup
    print(customFuncForCp(request = request, re = re, json = json, BeautifulSoup = BeautifulSoup, ut = UtilTime))