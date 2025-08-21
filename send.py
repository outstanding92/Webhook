import os
import requests
from datetime import datetime, timedelta, timezone

WEBHOOK_URL = os.getenv("DOORAY_INCOMING_URL")

# 한국 시간대
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

# 요일 한글 매핑
weekday_map = ["월", "화", "수", "목", "금", "토", "일"]

# 기본: 다음 날
target_date = now + timedelta(days=1)
# 금요일(weekday=4)에는 다음 주 월요일(+3일)
if now.weekday() == 4:
    target_date = now + timedelta(days=3)

date_str = target_date.strftime("%m월%d일")
weekday_str = weekday_map[target_date.weekday()]

TEXT = f"""안녕하세요.
{date_str}({weekday_str}요일) 구내식당 이용조사 
(O: 이용, X: 미이용) 표기 부탁드립니다.
"""

payload = {
    "botName": "식수조사봇",
    "botIconImage": "https://static.dooray.com/static_images/dooray-bot.png",
    "text": TEXT
}

resp = requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
print("Status:", resp.status_code)
print("Response:", resp.text)
