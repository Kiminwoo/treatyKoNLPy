from konlpy.tag import Kkma
from flask import Flask, render_template, redirect , request

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/getCompare',methods=['GET','POST'])
def excute():
    try:

      pTreatyList = request.args.get('platformTreatyList')
      aTreatyList = request.args.get('analysisTreatyList')

      excute_compare(pTreatyList, aTreatyList)

    except Exception as e:
      print(e)
    return redirect("/")

# 플랫폼팀 특약과 분석팀 특약의 문장 유사도 계산
def excute_compare(pTreatyList, aTreatyList):
    try:
      pCompareTreatyList = []
      aCompareTreatyList = []

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

          print("분석팀 특약 :: {treatyName}" .format(treatyName=aTreaty))
          print("플랫폼 특약 :: {treatyName}" .format(treatyName=pTreaty))

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

        print("문자열 비교 전 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pTreatyList))
        print("문자열 비교 후 플랫폼팀 특약 리스트 :: {treatyName}".format(treatyName=pCompareTreatyList))

      return redirect("/")

    except Exception as e:
      print(e)
    return redirect("/")

if __name__ == "__main__":
  app.run(host='127.0.0.1',port=3000,debug=True)