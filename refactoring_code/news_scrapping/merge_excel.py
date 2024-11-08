import pandas as pd
import glob
import os

# 엑셀 파일들이 있는 디렉토리 경로
directory = "./"  # 현재 디렉토리
keyword = "비엘에프"  # 검색했던 키워드

# 해당 키워드가 포함된 모든 엑셀 파일 찾기
excel_files = glob.glob(f"{directory}/{keyword}_뉴스검색결과_*.xlsx")

# 데이터프레임을 저장할 리스트
dfs = []

# 각 엑셀 파일 읽어서 리스트에 추가
for file in excel_files:
    df = pd.read_excel(file, engine='openpyxl')
    dfs.append(df)
    print(f"'{file}' 파일 로드 완료 - {len(df)}개 데이터")

# 모든 데이터프레임 합치기
if dfs:  # 데이터프레임이 있을 경우
    merged_df = pd.concat(dfs, ignore_index=True)

    # '제목'과 '날짜' 열이 있는지 확인
    print("현재 데이터프레임 열:", merged_df.columns)

    # 중복 제거 (제목과 날짜와 링크가 같은 경우 중복으로 간주)
    merged_df = merged_df.drop_duplicates(subset=['제목', '날짜', '링크'])

    # 날짜 기준으로 정렬
    merged_df = merged_df.sort_values('날짜', ascending=False)

    # 합친 파일 저장
    output_file = f"{keyword}_뉴스검색결과_통합.xlsx"
    merged_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"\n처리 완료:")
    print(f"총 {len(excel_files)}개 파일을 통합했습니다.")
    print(f"전체 데이터 수: {len(merged_df)}개")
    print(f"저장된 파일명: {output_file}")
else:
    print("파일을 읽을 수 없거나, 파일이 비어 있습니다.")
