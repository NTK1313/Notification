# 要件
# 当日の株価
# 前日からの増減
# 直近1週間のグラフ

import define
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import io
import datetime
from decimal import Decimal, ROUND_HALF_UP
from colorama import Fore, Back, Style

# 4220 リケンテクノス
# 4503 アステラス製薬
# 7466 SPK
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
SPACE = ' '
name = None
message = EOL + 'おはようございます。' + EOL + str(datetime.date.today()) + SPACE +'最新の株価情報を送信します。' + EOL + 'ご確認ください。' + EOL +'-----以下、株価情報--------'
symbol_data_list =define.get_share_info_list(code_list,5,1)
# codeでソート
symbol_data_list.sort(key=lambda x: x["code"])
#print(symbol_data_list)
list_size = len(symbol_data_list)
share_list = []
for d in range(0,int(list_size)):
	symbol_data = symbol_data_list[d]
	price_list = symbol_data["close"]
	time_list = symbol_data["timestamp"]
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

	# 株価前日比計算用の変数を設定
	cnt = 0
	before_price = ''

	# 直近2世代分の株価を取得
	for i in range(len(time_list)-2,len(time_list)):
		price = str(price_list[i])
		# 小数点第一位で四捨五入
		price_str = Decimal(str(price)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

		if cnt == 0:
			before_price = price_str
		else:
			msg_price = '株価 ' + '\\' +str(price_str)
			before_diff = Decimal(price_str) - Decimal(before_price)
			msg_diff = '前日'+ '\\' + str(before_price) + '(' + '\\' + str(before_diff) + ')'
			message1 = msg_price + SPACE + msg_diff
			message = str(message) + EOL + message1
			share_list.append([name,msg_price,msg_diff])
		cnt += 1

message = message + EOL + EOL + 'SBI証券ログインページ' + EOL + 'https://www.sbisec.co.jp/ETGate/WPLETmgR001Control?OutSide=on&getFlg=on&burl=search_fx&cat1=fx&cat2=guide&dir=guide&file=fx_guide_02_01.html'

#株価表の作成
# 表のサイズ指定
fig = plt.figure(figsize=(6,4),dpi=150)
plt.rcParams['font.family'] = 'Meiryo'
ax1 = fig.add_subplot(111)
ax1.axis("off")
columns =['【銘柄コード】企業名','株価','前日']
ax1.table(cellText=share_list, colLabels=columns,
        loc='center', bbox=[0, 0, 1, 1])
#メモリに画像を保存
buf = io.BytesIO()
plt.savefig(buf, format='png')
plt.close()

#LINE通知
define.send_line_notify(message,buf.getvalue())
