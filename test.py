def customFuncForCp(**kwargs):

    request = kwargs.get("request")
    re = kwargs.get("re")
    json = kwargs.get("json")
    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
    html = request(method="GET",url="https://www.52cp.cn/cqssc/history",headers=headers,timeout=5).text
    pattern = re.compile(r"myinfo?.*?';")
    res = json.loads(pattern.findall(html)[0].split('=')[1].replace("'","").replace(";",""))
    curterm = res['now']['expect']
    curno = res['now']['opencode']
    # for item in res['now']['opencode'].split(','):
    #     curno += str(int(item))
    nextterm = res['next']['expect']
    return curterm,curno,nextterm