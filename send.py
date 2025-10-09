import os
import requests
from datetime import datetime, timedelta, timezone
import holidays
import sys

WEBHOOK_URL = os.getenv("DOORAY_INCOMING_URL")

# 한국 시간대
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

# 요일 한글 매핑
weekday_map = ["월", "화", "수", "목", "금", "토", "일"]

# 한국 공휴일 객체
kr_holidays = holidays.KR()

# ✅ 오늘이 주말 또는 공휴일이면 종료 (메시지 전송 X)
if now.weekday() >= 5 or now.date() in kr_holidays:
    sys.exit(0)

# ✅ 금요일이면 다음 주 월요일(비공휴일)로 설정
if now.weekday() == 4:
    target_date = now + timedelta(days=3)
else:
    target_date = now + timedelta(days=1)

# ✅ target_date가 공휴일 또는 주말이면 다음 비공휴일 평일로 미룸
while target_date.weekday() >= 5 or target_date.date() in kr_holidays:
    target_date += timedelta(days=1)

# 메시지 구성
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

# 메시지 전송 (콘솔 출력 없음)
requests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
