from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_kallc_data():
    # Chrome 웹드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창을 띄우지 않고 실행
    driver = webdriver.Chrome(options=options)
    
    try:
        # 웹페이지 접속
        url = 'http://www.kallc.or.kr/kr/city/state.php'
        driver.get(url)
        
        # 페이지 로딩 대기
        time.sleep(3)
        
        # 데이터를 저장할 리스트
        data = []
        
        # 1부터 244까지의 행 순회
        for i in range(1, 245):
            row_data = []
            # 각 행의 5개 열 데이터 추출
            for j in range(1, 6):
                xpath = f'/html/body/div[2]/div/div/section/div/article/div/div/table/tbody/tr[{i}]/td[{j}]'
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    row_data.append(element.text.strip())
                except:
                    row_data.append('')
            data.append(row_data)
            if i % 10 == 0:  # 진행상황 표시
                print(f"{i}행 처리 완료...")
        
        # DataFrame 생성
        df = pd.DataFrame(data, columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5'])
        
        # CSV 파일로 저장
        df.to_csv('kallc_data.csv', index=False, encoding='utf-8-sig')
        print("데이터 스크래핑 완료! 'kallc_data.csv' 파일이 생성되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_kallc_data()