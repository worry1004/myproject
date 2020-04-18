# -*- coding: utf-8 -*-

import csv
from datetime import date
import requests
from urllib.parse import urlparse

# 사업장 등록 연월일 구분자 만들기
today = date.today()
theday = int(today.strftime("%Y%m%d"))
targetday = theday - 30000
two_yearday = theday - 20000
one_yearday = theday - 10000

f = open('list_202003.csv', 'r')
lines = csv.reader(f)
for line in lines:
    if line[13] != ' ':
        name = line[1]
        address = line[6]
        reg_num = line[2][3:5]
        code_num = int(line[13])
        code_name = line[14]
        join_date = int(line[15])
        join_cnt = line[18]
        # 검색의 정확도를 높이기 위해 사업장 명칭 다듬기
        rename = name.replace("(주)", "")
        new_name = rename.replace("주식회사", "")
        final_name = new_name.replace("주)", "").strip()

        # 사업자등록번호로 영리법인 본점만 걸러내기
        if reg_num == '81' or reg_num == '86' or reg_num == '87' or reg_num == '88':
            # 정보통신업
            # 정보통신업 / 컴퓨터 시스템 관련
            if join_date > one_yearday and code_num > 720000 and code_num < 722000:
                company = {
                    'name': final_name,
                    'address': address,
                    'code_num': code_num,
                    'code_name': code_name,
                    'join_date': str(join_date),
                    'join_cnt': join_cnt
                }
            # 정보통신업 / 응용 소프트웨어 개발 및 공급업
            elif join_date > one_yearday and code_num == 722000:
                company = {
                    'name': final_name,
                    'address': address,
                    'code_num': code_num,
                    'code_name': code_name,
                    'join_date': str(join_date),
                    'join_cnt': join_cnt
                }
            # 정보통신업 / 기타
            elif join_date > one_yearday and code_num > 722000 and code_num < 730000:
                company = {
                    'name': final_name,
                    'address': address,
                    'code_num': code_num,
                    'code_name': code_name,
                    'join_date': str(join_date),
                    'join_cnt': join_cnt
                }
            # 연구개발업
            elif join_date > one_yearday and code_num >= 730000 and code_num < 731000:
                company = {
                    'name': final_name,
                    'address': address,
                    'code_num': code_num,
                    'code_name': code_name,
                    'join_date': str(join_date),
                    'join_cnt': join_cnt
                }
            else:
                continue
        else:
            continue
    else:
        continue

    # print(company)

    keyword = final_name
    url = "https://openapi.naver.com/v1/search/news?query=" + keyword + "&display=1&sort=sim"
    result = requests.get(urlparse(url).geturl(),
            headers={"X-Naver-Client-Id":"nWcBRQJcPcSEX_l9fFNm", "X-Naver-Client-Secret": "fz6_4k9dYV"})
    search_result = result.json()['items']

    final_result = []
    for x in search_result:
        final_result.append(x['title'])
        final_result.append(x['link'])
        final_result.append(company['address'])
        final_result.append(company['code_name'])
        final_result.append(company['join_date'])
        final_result.append(company['join_cnt'])
        for y in final_result:
            if final_name in y:
                final_result[0] = final_name
            else:
                continue
            print(final_result)

f.close()
