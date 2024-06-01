# # -*- coding: utf-8 -*-


# import requests
# import json

# token="pat_v3ngMK6mMczFCbojnoxYR1iqtZjAr9cmErrdtxpJxw3bFo8EDyTvxgTwC9zOxqIl"  

# coze_url="https://api.coze.com/open_api/v2/chat"
# coze_headers={
#     'Authorization': f'Bearer {token}',
#     'Content-Type':'application/json',
#     'Connection': 'keep-alive',
#     'Accept':'*/*',
# }

# data=json.dumps({
#     "bot_id":"7369197409735327751",
#     "user":"demo",
#     "query":"bật đèn,turn off servo , turn off còi",
#     "stream": False
# })

# resp=requests.post(coze_url,data=data,headers=coze_headers)
# #print(resp)

#a=resp.json()
import json
a={'messages': [{'role': 'assistant',
   'type': 'function_call',
   'content': '{"name":"keyword_memory-setKeywordMemory","arguments":{"data":[{"keyword":"servo","value":"off"},{"keyword":"led","value":"on"},{"keyword":"horn","value":"on"}]},"plugin_id":7263427170075148306,"api_id":7288908904883322882,"plugin_type":1}',
   'content_type': 'text'},
  {'role': 'assistant',
   'type': 'tool_response',
   'content': '{"status":"success","reason":""}',
   'content_type': 'text'},
  {'role': 'assistant',
   'type': 'answer',
   'content': 'Đã thực hiện theo yêu cầu của bạn:\n\n-   🪄 Servo: off\n-   🪄 Đèn(Led): on\n-   🪄 Còi(Horn): on\n\nNếu bạn cần thay đổi trạng thái của các thiết bị, hãy yêu cầu!',
   'content_type': 'text'},
  {'role': 'assistant',
   'type': 'verbose',
   'content': '{"msg_type":"generate_answer_finish","data":""}',
   'content_type': 'text'}],
 'conversation_id': '8201b3b6838844fba6b011fd73248d60',
 'code': 0,
 'msg': 'success'}
json_string = json.dumps(a)


#chuyển sang dạng data
jsondt=json.loads(json_string)
messages=jsondt["messages"]  # lấy value của key "message"
#print(messages)


led_status=messages[0]["content"]

led_dt=json.loads(led_status)
argument=led_dt["arguments"]
#print(argument)
for keyword in argument["data"]:
  if(keyword["keyword"]=="servo"):
    servo_sta=keyword["keyword"]+'_'+keyword["value"]
  elif(keyword["keyword"]=="led"):
    led_sta=keyword["keyword"]+'_'+keyword["value"]
  else:
    horn_sta=keyword["keyword"]+'_'+keyword["value"]
print(horn_sta)
print(led_sta)
print(servo_sta)
