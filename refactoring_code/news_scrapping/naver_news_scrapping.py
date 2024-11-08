import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def search_news(keyword, start_date, end_date):
    results = []
    base_url = "https://search.naver.com/search.naver"
    
    # User-Agent 헤더 추가
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    
    page = 1
    while True:
        try:
            params = {
                "where": "news",
                "query": keyword,
                "sm": "tab_pge",
                "sort": "0",  # 0: 최신순, 1: 관련도순
                "photo": "0",
                "field": "0",
                "pd": "3",    # 3: 직접입력
                "ds": start_date_str,
                "de": end_date_str,
                "cluster_rank": "0",
                "mynews": "0",
                "office_type": "0",
                "office_section_code": "0",
                "news_office_checked": "",
                "nso": f"so:r,p:from{start_date.strftime('%Y%m%d')}to{end_date.strftime('%Y%m%d')},a:all",
                "start": (page - 1) * 10 + 1
            }
            
            response = requests.get(base_url, params=params, headers=headers)
            time.sleep(1)
            response.raise_for_status()  # 오류 발생시 예외 발생
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = soup.select("div.news_wrap.api_ani_send")  # 선택자 수정
            
            if not news_items:
                break
                
            for item in news_items:
                try:
                    title = item.select_one(".news_tit").text.strip()
                    link = item.select_one(".news_tit")["href"]
                    content = item.select_one(".api_txt_lines.dsc_txt_wrap").text.strip()
                    press = item.select_one(".info_group > a:first-child").text.strip()
                    date = item.select_one(".info_group > span.info").text.strip()
                    
                    results.append({
                        "제목": title,
                        "언론사": press,
                        "날짜": date,
                        "링크": link,
                        "내용": content,
                        "검색일자": datetime.now().strftime("%Y-%m-%d")
                    })
                except AttributeError as e:
                    print(f"데이터 추출 중 오류 발생: {e}")
                    continue
            
            print(f"{page}페이지 완료 (검색결과: {len(results)}건)")
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f"페이지 요청 중 오류 발생: {e}")
            break
            
    return pd.DataFrame(results)

# 실행 예시
from datetime import datetime, timedelta

keyword = "비엘에프"
start_date = datetime(2020, 1, 1)
end_date = datetime.now()

# 1년 단위로 검색
current_start = start_date
while current_start < end_date:
    current_end = min(current_start + timedelta(days=365), end_date)
    print(f"검색 기간: {current_start.strftime('%Y-%m-%d')} ~ {current_end.strftime('%Y-%m-%d')}")
    
    news_df = search_news(keyword, current_start, current_end)
    output_file = f"./{keyword}_뉴스검색결과_{current_start.strftime('%Y%m%d')}_{current_end.strftime('%Y%m%d')}.xlsx"
    news_df.to_excel(output_file, index=False, engine='openpyxl')
    
    current_start = current_end + timedelta(days=1)