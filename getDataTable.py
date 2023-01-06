import requests
from bs4 import BeautifulSoup
import json
import jsonpickle

arr = [
    "https://www.apifox.cn/apidoc/project-759159/api-14621407"

]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36 '
}

functionList = []


def __getFunction():
    for url in arr:
        applicationServerFunction = {"urlInfoList": [{
            "urlType": "dev",
            "requestMethod": "post",
            "url": ''

        }, {
            "urlType": "uat",
            "requestMethod": "post",
            "url": ''

        }, {
            "urlType": "pro",
            "requestMethod": "post",
            "url": ''

        }]}

        paramTypeList = []

        lastData = {
            "paramTypeList": "[{\"whetherRequired\":false,\"name\":\"access_token\",\"remark\":\"调用接口凭证\",\"dataType\":{\"type\":\"string\"}}]",
            "returnDataType": "",
            "enName": "",
            "cnName": "删除分组",
            "functionType": "server",
            "serviceId": "6888411520197280316",
            "inputTypeFormat": 0,
            "outputTypeFormat": 0,
            "applicationServerFunction": "{\"source\":\"utyun\",\"extendParam\":null,\"urlInfoList\":[{\"urlType\":\"dev\",\"requestMethod\":\"get\",\"url\":\"/cgi-bin/kf/knowledge/del_group\"},{\"urlType\":\"uat\",\"requestMethod\":\"get\",\"url\":\"/cgi-bin/kf/knowledge/del_group\"},{\"urlType\":\"pro\",\"requestMethod\":\"get\",\"url\":\"/cgi-bin/kf/knowledge/del_group\"}]}",
            "whetherIdempotence": "true",
        }

        cnName = ''
        # 请求头文件
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"  #
        # step_3:获取响应数据:通过调用响应对象的text属性
        page_text = res.text

        bs1 = BeautifulSoup(page_text, 'html.parser')

        serialized = json.dumps(applicationServerFunction, sort_keys=True, indent=3)
        jsonType = json.loads(serialized)

        paramList = bs1.find_all('div', attrs={'class': 'tablenoborder'})[1].find_all('tr')[1:]
        for tr in paramList:
            paramTypeLists = {}
            for index, td in enumerate(tr):
                if index == 1:
                    paramTypeLists["name"] = td.text
                if index == 3:
                    paramTypeLists["whetherRequired"] = (td.text.strip() == '必选')
                if index == 5:
                    paramTypeLists["dataType"] = {"specs": {
                        "length": ""
                    },
                        "type": td.text}
                if index == 9:
                    paramTypeLists["remark"] = td.text
            paramTypeList.append(paramTypeLists)

            lastData['paramTypeList'] = json.dumps(paramTypeList).encode('utf-8').decode(
                'unicode_escape')
            # lastData['paramTypeList'] = ""
        # 获取url 和 get
        for i in bs1.find_all('p'):
            url_list = i.text
            is_post = "post" in url_list
            is_get = "get" in url_list
            is_put = "put" in url_list
            is_delete = "delete" in url_list
            is_url = "/v5" in url_list
            if is_post:
                for obj in jsonType.get('urlInfoList'):
                    obj.requestMethod = 'post'
            if is_get:
                for obj in jsonType.get('urlInfoList'):
                    obj.requestMethod = 'get'
            if is_put:
                for obj in jsonType.get('urlInfoList'):
                    obj.requestMethod = 'put'
            if is_delete:
                for obj in jsonType.get('urlInfoList'):
                    obj.requestMethod = 'delete'
            if is_url:
                for obj in jsonType.get('urlInfoList'):
                    obj['url'] = url_list
            lastData['applicationServerFunction'] = json.dumps(jsonType)
            # lastData['applicationServerFunction'] = ''

        for i in bs1.find_all('h1', attrs={'class': 'topictitle1'}):
            url_list = i.text
            lastData['cnName'] = url_list

        functionList.append(lastData)
    print(functionList)
    # print(str(functionList).replace("'", "\"").replace(r"\n", ""))


__getFunction()
