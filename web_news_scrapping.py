import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def search_news(keyword, start_date, end_date):
    # 검색 결과를 저장할 리스트
    results = []
    base_url = "https://search.naver.com/search.naver"
    
    # 날짜 형식 변환 (YYYYMMDD)
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    
    # 페이지 수
    page = 1
    while True:
        # 검색 파라미터 설정
        params = {
            "where": "news",
            "query": keyword,
            "sm": "tab_jum",
            "date_from": start_date_str,
            "date_to": end_date_str,
            "date_option": "8",  # 8: 사용자 지정 기간
            "start": (page - 1) * 10 + 1  # 페이지 네비게이션 (1, 11, 21, ...)
        }
        
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 항목들 찾기
        news_items = soup.select(".news_area")
        
        # 뉴스가 없으면 종료
        if not news_items:
            break
        
        for item in news_items:
            title = item.select_one(".news_tit").text
            link = item.select_one(".news_tit")["href"]
            content = item.select_one(".news_dsc").text.strip()
            
            results.append({
                "제목": title,
                "링크": link,
                "내용": content,
                "검색일자": datetime.now().strftime("%Y-%m-%d")
            })
        
        page += 1  # 다음 페이지로 이동
    
    return pd.DataFrame(results)

# 실행
keyword = "비엘에프"
start_date = datetime(2020, 1, 1)  # 시작 날짜
end_date = datetime.now()  # 현재 날짜
news_df = search_news(keyword, start_date, end_date)

# 결과를 엑셀 파일로 저장
output_file = f"./{keyword}_뉴스검색결과.xlsx"  # 현재 디렉토리에 저장

try:
    news_df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"검색 결과가 '{output_file}'로 저장되었습니다.")
except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")