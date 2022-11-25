# 要件
# 当日の株価
# 前日からの増減
# 直近1週間のグラフ

import define
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# 4220 リケンテクノス
# 4503 アステラス製薬
# SPK
# 8306 三菱UFL
# 9432 NTT
code_list = ['4220','4503','7466','8306','9432']

# 株価データ取得
symbol_data_list = []
# timestamp：取引日時
# open：始値
# high：高値
# low：底値
# close：終値
# volume：出来高
EOL = '\r\n'
SPECE = ' '
name = None
message = EOL + 'おはようございます。' + EOL + '最新の株価情報を送信します。' + EOL + 'ご確認ください。' + EOL +'-----以下、株価情報--------'
symbol_data_list =define.get_share_info_list(code_list,5,1)
symbol_data_list.sort(key=lambda x: x["timestamp"])
print(symbol_data_list)
list_size = len(symbol_data_list)
for d in range(0,int(list_size)):
	symbol_data = symbol_data_list[d]
	price_list = symbol_data["close"]
	time_list = symbol_data["timestamp"]
	print(len(time_list))
	if (d == 0):
		name = '【4220】リケンテクノス'
	elif(d == 1):
		name = '【4503】アステラス製薬'
	elif(d == 2):
		name = '【7466】SPK'
	elif(d == 3):
		name = '【8306】三菱UFJ'
	else:
		name = '【9432】NTT'
	message = message + EOL + name
	for i in range(len(time_list)-2,len(time_list)): # 直近2世代分の株価を取得
		time = time_list[i]
		price = str(price_list[i])
		time = datetime.utcfromtimestamp(int(time/1000))
		time = time.strftime("%m/%d")
		msg_time = '日時' + str(time)
		msg_price = '株価' + str(price)
		message1 = msg_time + SPECE + msg_price
		message = str(message) + EOL + message1
#print(message)
message = message + EOL + EOL + 'SBI証券ログインページ' + EOL + 'https://www.sbisec.co.jp/ETGate/WPLETmgR001Control?OutSide=on&getFlg=on&burl=search_fx&cat1=fx&cat2=guide&dir=guide&file=fx_guide_02_01.html'
define.send_line_notify(message)
