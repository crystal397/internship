import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_kallc_data():
    # 웹사이트 URL
    url = 'http://www.kallc.or.kr/kr/city/state.php'
    
    # 헤더 추가 (웹사이트 접근을 위해)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 웹페이지 요청
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 오류 체크
        
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 데이터를 저장할 리스트
        data = []
        
        # 1부터 244까지의 행 순회
        for i in range(1, 245):
            row_data = []
            # 각 행의 5개 열 데이터 추출
            for j in range(1, 6):
                xpath = f'/html/body/div[2]/div/div/section/div/article/div/div/table/tbody/tr[{i}]/td[{j}]'
                # BeautifulSoup에서는 CSS 선택자를 사용
                selector = f'table tbody tr:nth-child({i}) td:nth-child({j})'
                element = soup.select_one(selector)
                row_data.append(element.text.strip() if element else '')
            data.append(row_data)
        
        # DataFrame 생성
        df = pd.DataFrame(data, columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5'])
        
        # CSV 파일로 저장
        df.to_csv('kallc_data.csv', index=False, encoding='utf-8-sig')
        print("데이터 스크래핑 완료! 'kallc_data.csv' 파일이 생성되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    scrape_kallc_data()
