#-*- coding:utf-8 -*-
import requests
import xmltodict
import sys
import json
import csv

api_key_decode = ""

# api key 세팅
def set_api_key_decode():
    global api_key_decode
    api_key_decode = requests.utils.unquote("XaMtCJTJtlmQEGswOTfoO7XVM9uD7umqE05HBQhkAKPW1uAMeLeNU3UPnBrw6LRuLwsvXPLmxBO%2FT7T8rXoj%2Fw%3D%3D")

# 사업장 정보조회 서비스 api 요청
def get_bass_info_search(company_name, company_no, page_no, num_of_rows):
    # url 가져온후
    url = "http://apis.data.go.kr/B552015/NpsBplcInfoInqireService/getBassInfoSearch"
    # url 파라미터 세팅
    parameters = {
        "serviceKey":api_key_decode,
        "wkpl_nm" : company_name,
        "bzowr_rgst_no":company_no ,
        "pageNo": page_no,
        "numOfRows" : num_of_rows
    }
    try:
        # url 요청
        req = requests.get(url, params = parameters)
    except requests.exceptions.RequestException as e:
        return {"exception_msg" : e}

    # xml 형식 데이터 -> dict로 변환
    xml_data = xmltodict.parse(req.text)

    if(xml_data['response']['body']['items'] == None):
        return {"exception_msg": "조회하려는 정보가 없습니다."}
    informations = xml_data['response']['body']['items']['item']
    # 사업자 등록 번호로 구분?
    # registration_no = informations[0]['bzowrRgstNo']
    # 회사 이름
    company_name = informations[0]['wkplNm'].strip()
    for item in informations:
        if(item['wkplNm'].strip() != company_name):
            return {"exception_msg" : "중복되는 회사가 여러개입니다."}
        # print("회사명: "+item['wkplNm'])
        # print("월 : "+item['dataCrtYm'])
        # print("seq : "+item['seq'])
    # 가장 최근 정보
    lately_bass_info = informations[len(informations)-1]

    bass_info = {}
    bass_info['company'] = lately_bass_info['wkplNm']
    bass_info['date'] = lately_bass_info['dataCrtYm']
    bass_info['seq'] = lately_bass_info['seq']

    return bass_info

# 상세 정보 조회 서비스 api 요청
def get_detail_info_search(info):
    # url 가져온후
    url = "http://apis.data.go.kr/B552015/NpsBplcInfoInqireService/getDetailInfoSearch"
    parameters = {
        "serviceKey": api_key_decode,
        "seq" : info['seq']
    }
    try:
        # url 요청
        req = requests.get(url, params = parameters)
    except requests.exceptions.RequestException as e:
        return {"exception_msg" : e}

    # xml 형식 데이터 -> dict로 변환
    xml_data = xmltodict.parse(req.text)

    detail = xml_data['response']['body']['item']

    info['employee_count'] = int(detail['jnngpCnt'])
    info['paid_pension'] = int(detail['crrmmNtcAmt'])
    info['pension_per_employee'] = int(info['paid_pension'] / info['employee_count'] / 2)

    return info

def get_salary_pension_csv(price):
    with open('./resources/pension_per_employee.csv', 'r', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        pre = 0
        result = 0
        for row in reader:
            pension = int(row['국민연금'])
            if pre == 0 and price <= pension:
                result = row['연봉']
                break
            elif pre <= price and price <= pension:
                # 더 가까운 곳의 연봉을 넣어줌
                if (price - pre) < (pension - price):
                    result = pre_salary
                else :
                    result = row['연봉']
                break
            elif price >= pension:
                pre = pension
                pre_salary = row['연봉']
    return result


def lambda_handler(event, context):

    # 매핑 펨플릿 형식에서  파라미터 가져오기 위한 작업
    # params_arry = event['params']
    # path_arry = params_arry['path']
    # post로 받으려면
    body = event['body-json']

    # 에러처리
    isNameParam = True
    isBsNoParam = True
    if('name' not in body): isNameParam = False
    if('bsNo' not in body): isBsNoParam = False
    if(not isNameParam and not isBsNoParam): return "name과 bsNo 요청 변수가 없습니다."
    elif(not isNameParam): return "name 요청 변수가 없습니다."
    elif(not isBsNoParam): return "bsNo 요청 변수가 없습니다."

    company_name = body['name']
    company_no = body['bsNo']

    # # api key 세팅
    set_api_key_decode()
    # 사업자 정보 조회
    bass_info = get_bass_info_search(company_name, company_no, 1, 100)
    if('exception_msg' in bass_info):
        return {
            'statusCode' : 204,
            'message' : "정보를 조회할 수 없습니다.",
            "exception_msg" : bass_info['exception_msg']
        }
    info = get_detail_info_search(bass_info)
    if('exception_msg' in info):
        return {
            'statusCode' : 204,
            'message' : "정보를 조회할 수 없습니다.",
            "exception_msg" : bass_info['exception_msg']
        }
    salary = get_salary_pension_csv(info['pension_per_employee'])
    info['salary'] = salary
    # TODO implement
    return {
        'statusCode': 200,
        'body' : info
        # 'body': json.dumps(info, indent=4)
    }
