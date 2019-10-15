#-*- coding:utf-8 -*-
import requests
import xmltodict
import json
import sys
import io

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
    # url 요청
    req = requests.get(url, params = parameters)
    # xml 형식 데이터 -> dict로 변환
    xml_data = xmltodict.parse(req.text)

    informations = xml_data['response']['body']['items']['item']
    # 사업자 등록 번호로 구분?
    # registration_no = informations[0]['bzowrRgstNo']
    # 회사 이름
    company_name = informations[0]['wkplNm'].strip()
    for item in informations:
        if(item['wkplNm'].strip() != company_name):
            return "Error"
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
    # url 요청
    req = requests.get(url, params = parameters)
    # xml 형식 데이터 -> dict로 변환
    xml_data = xmltodict.parse(req.text)

    detail = xml_data['response']['body']['item']

    info['employee_count'] = detail['jnngpCnt']
    info['paid_pension'] = detail['crrmmNtcAmt']
    info['pension_per_employee'] = int(int(detail['crrmmNtcAmt']) / int(detail['jnngpCnt']) / 2)

    return info

# api key 세팅
set_api_key_decode()
# 사업자 정보 조회
bass_info = get_bass_info_search("당근마켓", "375870", 1, 100)
info = get_detail_info_search(bass_info)
print(info)
