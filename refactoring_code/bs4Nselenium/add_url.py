from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_kallc_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        url = 'http://www.kallc.or.kr/kr/city/state.php'
        driver.get(url)
        time.sleep(3)
        
        data = []
        
        for i in range(1, 245):
            row_data = []
            # 각 열 데이터 추출
            for j in range(1, 6):
                # 3번째 열일 경우 href 속성을 가져옴
                if j == 3:
                    xpath = f'/html/body/div[2]/div/div/section/div/article/div/div/table/tbody/tr[{i}]/td[{j}]/a'
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        # href 속성 가져오기
                        href = element.get_attribute('href')
                        row_data.append(href if href else '')
                    except:
                        # a 태그가 없는 경우 일반 텍스트로 처리
                        xpath = f'/html/body/div[2]/div/div/section/div/article/div/div/table/tbody/tr[{i}]/td[{j}]'
                        try:
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, xpath))
                            )
                            row_data.append(element.text.strip())
                        except:
                            row_data.append('')
                else:
                    xpath = f'/html/body/div[2]/div/div/section/div/article/div/div/table/tbody/tr[{i}]/td[{j}]'
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        row_data.append(element.text.strip())
                    except:
                        row_data.append('')
            
            data.append(row_data)
            if i % 10 == 0:
                print(f"{i}행 처리 완료...")
        
        df = pd.DataFrame(data, columns=['Column1', 'Column2', 'URL', 'Column4', 'Column5'])
        df.to_csv('kallc_data.csv', index=False, encoding='utf-8-sig')
        print("데이터 스크래핑 완료! 'kallc_data.csv' 파일이 생성되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_kallc_data()