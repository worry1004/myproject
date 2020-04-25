# -*- coding: utf-8 -*-

import csv
from datetime import date
import requests
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/corp_1/')

def corp_finder_1():
    db.corporates.drop()

    today = date.today()
    theday = int(today.strftime("%Y%m%d"))
    one_yearday = theday - 10000

    f = open('list_202003.csv', 'r', encoding='CP949')
    lines = csv.reader(f)
    for line in lines:
        if line[13] != ' ':  # 업종이 공란인 부분 제외
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
                # 1년차 연구개발업 및 정보통신업
                if join_date > one_yearday and code_num > 720000 and code_num < 731000:
                    company = {
                        'name': final_name,
                        'address': address,
                        'code_num': str(code_num),
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
        # 네이버 뉴스 API로 사업장명(회사명)으로 검색하여 검색되는 기업의 정보 출력하기
        keyword = final_name
        url = "https://openapi.naver.com/v1/search/news?query=" + keyword + "&display=1&sort=sim"
        result = requests.get(urlparse(url).geturl(),
                               headers={"X-Naver-Client-Id": "nWcBRQJcPcSEX_l9fFNm",
                                       "X-Naver-Client-Secret": "fz6_4k9dYV"})
        json_result = result.json()
        if 'items' in json_result:
            search_result = json_result['items']
        else:
            continue

        final_result = []
        for x in search_result:
            final_result.append(x['title'])
            final_result.append(x['link'])
            final_result.append(company['address'])
            final_result.append(company['code_num'])
            final_result.append(company['code_name'])
            final_result.append(company['join_date'])
            final_result.append(company['join_cnt'])
            for y in final_result:
                if final_name in y:
                    final_result[0] = final_name
                else:
                    continue
                # 최종 결과를 딕셔너리 형태로 저장
                corporates = {}
                corporates['corporate_name'] = final_result[0]
                corporates['article_link'] = final_result[1]
                corporates['address'] = final_result[2]
                corporates['code_num'] = final_result[3]
                corporates['code_name'] = final_result[4]
                corporates['registration_date'] = final_result[5]
                corporates['employee_num'] = final_result[6]

                db.corporates.insert_one(corporates)
    f.close()
    return render_template('index.html')

@app.route('/corp_2/')

def corp_finder_2():
    db.corporates.drop()

    today = date.today()
    theday = int(today.strftime("%Y%m%d"))
    two_yearday = theday - 20000
    one_yearday = theday - 10000

    f = open('list_202003.csv', 'r', encoding='CP949')
    lines = csv.reader(f)
    for line in lines:
        if line[13] != ' ':  # 업종이 공란인 부분 제외
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
                # 2년차 연구배발업 및 정보통신업
                if join_date <= one_yearday and join_date > two_yearday and code_num > 720000 and code_num < 731000:
                    company = {
                        'name': final_name,
                        'address': address,
                        'code_num': str(code_num),
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
        # 네이버 뉴스 API로 사업장명(회사명)으로 검색하여 검색되는 기업의 정보 출력하기
        keyword = final_name
        url = "https://openapi.naver.com/v1/search/news?query=" + keyword + "&display=1&sort=sim"
        result = requests.get(urlparse(url).geturl(),
                               headers={"X-Naver-Client-Id": "nWcBRQJcPcSEX_l9fFNm",
                                       "X-Naver-Client-Secret": "fz6_4k9dYV"})
        # search_result = result.json()['items']
        json_result = result.json()
        if 'items' in json_result:
            search_result = json_result['items']
        else:
            continue

        final_result = []
        for x in search_result:
            final_result.append(x['title'])
            final_result.append(x['link'])
            final_result.append(company['address'])
            final_result.append(company['code_num'])
            final_result.append(company['code_name'])
            final_result.append(company['join_date'])
            final_result.append(company['join_cnt'])
            for y in final_result:
                if final_name in y:
                    final_result[0] = final_name
                else:
                    continue
                # 최종 결과를 딕셔너리 형태로 저장
                corporates = {}
                corporates['corporate_name'] = final_result[0]
                corporates['article_link'] = final_result[1]
                corporates['address'] = final_result[2]
                corporates['code_num'] = final_result[3]
                corporates['code_name'] = final_result[4]
                corporates['registration_date'] = final_result[5]
                corporates['employee_num'] = final_result[6]

                db.corporates.insert_one(corporates)
    f.close()
    return render_template('index.html')

@app.route('/corp_3/')

def corp_finder_3():
    db.corporates.drop()

    today = date.today()
    theday = int(today.strftime("%Y%m%d"))
    three_yearday = theday - 30000
    two_yearday = theday - 20000

    f = open('list_202003.csv', 'r', encoding='CP949')
    lines = csv.reader(f)
    for line in lines:
        if line[13] != ' ':  # 업종이 공란인 부분 제외
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
                # 3년차 연구개발업 및 정보통신업
                if join_date <= two_yearday and join_date > three_yearday and code_num > 720000 and code_num < 731000:
                    company = {
                        'name': final_name,
                        'address': address,
                        'code_num': str(code_num),
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
        # 네이버 뉴스 API로 사업장명(회사명)으로 검색하여 검색되는 기업의 정보 출력하기
        keyword = final_name
        url = "https://openapi.naver.com/v1/search/news?query=" + keyword + "&display=1&sort=sim"
        result = requests.get(urlparse(url).geturl(),
                               headers={"X-Naver-Client-Id": "nWcBRQJcPcSEX_l9fFNm",
                                       "X-Naver-Client-Secret": "fz6_4k9dYV"})
        json_result = result.json()
        if 'items' in json_result:
            search_result = json_result['items']
        else:
            continue

        final_result = []
        for x in search_result:
            final_result.append(x['title'])
            final_result.append(x['link'])
            final_result.append(company['address'])
            final_result.append(company['code_num'])
            final_result.append(company['code_name'])
            final_result.append(company['join_date'])
            final_result.append(company['join_cnt'])
            for y in final_result:
                if final_name in y:
                    final_result[0] = final_name
                else:
                    continue
                # 최종 결과를 딕셔너리 형태로 저장
                corporates = {}
                corporates['corporate_name'] = final_result[0]
                corporates['article_link'] = final_result[1]
                corporates['address'] = final_result[2]
                corporates['code_num'] = final_result[3]
                corporates['code_name'] = final_result[4]
                corporates['registration_date'] = final_result[5]
                corporates['employee_num'] = final_result[6]

                db.corporates.insert_one(corporates)
    f.close()
    return render_template('index.html')

@app.route('/reader_1', methods=['GET'])
def corp_reader_1():
    corporates = list(db.corporates.find({},{'_id':0}))
    resultlist = []
    for c in corporates:
        if int(c['code_num']) < 722000:
            resultlist.append(c)
    finallist = random.sample(resultlist, 12)
    return jsonify({'result': 'success', 'finallist': finallist})

@app.route('/reader_2', methods=['GET'])
def corp_reader_2():
    corporates = list(db.corporates.find({},{'_id':0}))
    resultlist = []
    for c in corporates:
        if int(c['code_num']) == 722000:
            resultlist.append(c)
    finallist = random.sample(resultlist, 12)
    return jsonify({'result': 'success', 'finallist': finallist})

@app.route('/reader_3', methods=['GET'])
def corp_reader_3():
    corporates = list(db.corporates.find({},{'_id':0}))
    resultlist = []
    for c in corporates:
        if int(c['code_num']) > 722000 and int(c['code_num']) < 730000:
            resultlist.append(c)
    finallist = random.sample(resultlist, 12)
    return jsonify({'result': 'success', 'finallist': finallist})

@app.route('/reader_4', methods=['GET'])
def corp_reader_4():
    corporates = list(db.corporates.find({},{'_id':0}))
    resultlist = []
    for c in corporates:
        if int(c['code_num']) >= 730000 and int(c['code_num']) < 731000:
            resultlist.append(c)
    finallist = random.sample(resultlist, 12)
    return jsonify({'result': 'success', 'finallist': finallist})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)