import requests
import json

url = 'http://10.2.56.190:5005/translator'
d = {'source': 'zh_SG', 'target': 'en_SG', 'query': "举报者是2014年在韩国上映的一部电影，导演是任順禮"}
r = requests.post(url, data=d)
print(json.loads(r.text)["data"]["translations"][0]['translatedText'])