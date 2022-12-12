from konlpy.tag import Kkma
from flask import Flask, render_template, redirect , request , jsonify
import json
import requests

app = Flask(__name__)
# utf8 설정으로 인한 한글깨짐 방지
app.config['JSON_AS_ASCII'] = False

@app.route("/",methods=['GET','POST'])
def index():
    return ""

@app.route('/test_post_send_one',methods=['GET','POST'])
def test():
  params = {
         "planId" : "38150",
         "aTreatyList" : ["주계약","(무)크라운치료특약Ⅱ갱신형","(무)소액치과치료특약 Ⅱ(갱신형)"],
         "pTreatyList" : ["주계약","무)소액치과치료특약Ⅱ(갱신형)","무)크라운치료특약Ⅱ갱신형"] 
  }

  res = requests.post("http://127.0.0.1:3100/getCompareOnlyOnePlanId",data=json.dumps(params))
  return res.text


# 특약 문자열 비교 라우터 
# post 처리 
@app.route('/getCompareOnlyOnePlanId',methods=['GET','POST'])
def excute():
  # aTreatyList = request.args.get('analysisTreatyList')
  # pTreatyList = request.args.get('platformTreatyList')

  aTreatyList = []
  pTreatyList = []

  params = json.loads(request.get_data(), encoding = "utf-8")

  for teamKey in params.keys():
    if( teamKey == "aTreatyList" ):
      for aTreatyItem in params[teamKey]:
        aTreatyList.append(aTreatyItem)
    if( teamKey == "pTreatyList" ):
      for pTreatyItem in params[teamKey]:
        pTreatyList.append(pTreatyItem)

  print("============================================================================")
  print("플랜ID  : {planId}".format(planId=params["planId"]))
  print("분석팀 post 특약 list  : {aTreatyList}".format(aTreatyList=aTreatyList))
  print("플랫폼팀 post 특약 list  : {pTreatyList}".format(pTreatyList=pTreatyList))
  print("============================================================================")

  compareResult = excute_compare(aTreatyList,pTreatyList)

  return compareResult


# 플랫폼팀 특약과 분석팀 특약의 문장 유사도 계산
def excute_compare(aTreatyList,pTreatyList):
  pCompareTreatyList = []
  pCompareTreatyIndexList = []
  aCompareTreatyList = []
  compareResultList = {}

  # 꼬꼬마 선언 
  kkma = Kkma()


  # 플랫폼 특약 리스트
  for pIndex, aTreatyItem in enumerate(aTreatyList):

    # 분석팀 특약 비교 리스트 초기화
    aCompareTreatyList = []

    # 분석팀 특약 리스트
    for aIndex, pTreatyItem in enumerate(pTreatyList):

      # 동일 카운트 0 초기화
      compareCnt = 0

      aTreaty = kkma.pos(aTreatyItem)
      pTreaty = kkma.pos(pTreatyItem)

      # print("=====================================================")
      # print("분석팀 특약 :: {treatyName}" .format(treatyName=aTreaty))
      # print("플랫폼 특약 :: {treatyName}" .format(treatyName=pTreaty))
      # print("=====================================================")

      # kkma로 명사 + 품사 조사를 기반으로 플랫폼 특약과 분석팀 특약의 일치 여부 판단
      for aTreatyString in aTreaty:
        for pTreatyString in pTreaty:
          if (pTreatyString == aTreatyString):
            compareCnt += 1

      aCompareTreatyList.append(compareCnt)

      # 기존 분석팀 특약리스트와 비교한 분석팀 특약리스트가 같아질때
      if(len(aCompareTreatyList) == len(aTreatyList)):
        compareIndex = aCompareTreatyList.index(max(aCompareTreatyList))
        pCompareTreatyList.append(aTreatyList[compareIndex])
        pCompareTreatyIndexList.append(compareIndex)
        compareResultList[aTreatyList[compareIndex]] = compareIndex

  print("============================================================================")
  print("문자열 비교 전 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pTreatyList))
  print("문자열 비교 후 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pCompareTreatyList))
  print("문자열 비교 후 매칭 인데스 리스트 :: {treatyName}".format(treatyName=pCompareTreatyIndexList))
  print("문자열 비교 후 결과값  :: {treatyName}".format(treatyName=compareResultList))
  print("============================================================================")


  return jsonify(compareResultList)


if __name__ == "__main__":
  app.run(host='127.0.0.1',port=3100,debug=True)
