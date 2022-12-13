from konlpy.tag import Kkma
from flask import Flask, render_template, redirect , request , jsonify
import json
import requests
from flask_cors import CORS
from operator import itemgetter

app = Flask(__name__)
# utf8 설정으로 인한 한글깨짐 방지
app.config['JSON_AS_ASCII'] = False
# json 정렬 false 처리  
app.config['JSON_SORT_KEYS'] = False
# Resource specific CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/",methods=['GET','POST'])
def index():
    return ""

@app.route('/test_post_send_one',methods=['GET','POST'])
def testString():
  params = {
         "aTreatyList" : ["무배당 중등도이상치매종신간병생활자금특약T(해지환급금 미지급형)","무배당 중증치매종신간병생활자금특약T(해지환급금 미지급형)"],
         "pTreatyList" : ["무)중등도이상치매종신간병생활자금특약T(해지환급금 미지급형)","무)중증치매종신간병생활자금특약T(해지환급금 미지급형)"] 
  }

  res = requests.post("http://127.0.0.1:3100/api/v1/getCompare",data=json.dumps(params))
  return res.text

# 특약 문자열 비교 라우터 
# post 처리 
@app.route('/api/v1/getCompare',methods=['GET','POST'])
def excute():

  aTreatyList = []
  pTreatyList = []

  params = json.loads(request.get_data(), encoding = "utf-8")

  for teamKey in params.keys():
    if( teamKey == "aTreatyList" ):
      for aTreatyItem in params[teamKey]:

        # 데이터 전처리 부분 
        aTreatyItem = data_preprocessing(aTreatyItem)
        aTreatyList.append(aTreatyItem)
    if( teamKey == "pTreatyList" ):
      for pTreatyItem in params[teamKey]:

        # 데이터 전처리 부분 
        pTreatyItem = data_preprocessing(pTreatyItem)
        pTreatyList.append(pTreatyItem)

  print("============================================================================")
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

  compareResultObj = {}
  compareResultList = []

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

      # kkma로 명사 + 품사 조사를 기반으로 플랫폼 특약과 분석팀 특약의 일치 여부 판단
      for aTreatyString in aTreaty:
        for pTreatyString in pTreaty:
          if (pTreatyString[0] == aTreatyString[0]):
            compareCnt += 1

      aCompareTreatyList.append(compareCnt)

      # 기존 분석팀 특약리스트와 비교한 분석팀 특약리스트가 같아질때
      # compareCnt 값이 제일 큰 특약과 매칭 
      if(len(aCompareTreatyList) == len(aTreatyList)):

        compareIndex = aCompareTreatyList.index(max(aCompareTreatyList))

        pCompareTreatyList.append(aTreatyList[compareIndex])
        pCompareTreatyIndexList.append(compareIndex)

        compareResultObj[aTreatyList[compareIndex]] = compareIndex

  compareResultList.append(compareResultObj)
  
  print("============================================================================")
  print("문자열 비교 전 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pTreatyList))
  print("문자열 비교 후 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pCompareTreatyList))
  print("문자열 비교 후 매칭 인데스 리스트 :: {treatyName}".format(treatyName=pCompareTreatyIndexList))
  print("문자열 비교 후 결과값  :: {treatyName}".format(treatyName=compareResultList))
  print("============================================================================")

  # return 해줄때 value 의 index 기준으로 정렬
  return jsonify(sorted(compareResultList[0].items(), key = lambda item: item[1]))



class matchTreaty:
	def __init__(self, treatyName, index):
		self.big = big
		self.treatyName = treatyName
		self.index = index

# 데이터 전처리 함수 
def data_preprocessing(treatyItem):
    
    # 불필요한 ( , ) 제거  
    treatyItem = treatyItem.replace("(","").replace(")","")

    return treatyItem

def customSort(treaty):
    return treaty['value']

if __name__ == "__main__":
  app.run(host='127.0.0.1',port=3100,debug=True)
