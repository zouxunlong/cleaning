import requests
url = 'http://10.2.56.190:5005/translator'
d = {'source': 'zh_SG', 'target': 'en_SG', 'query': "好啊"}
r = requests.post(url, data=d)
print(eval(r.text)["data"]["translations"][0]['translatedText'])