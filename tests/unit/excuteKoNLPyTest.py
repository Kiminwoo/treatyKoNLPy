from konlpy.tag import Kkma
from flask import Flask, render_template, redirect , request , jsonify
import json
import requests
import pytest



class TestClass : 

    @pytest.fixture
    def getCompare_post_send_one():

        """Test function getCompare ."""

        params = {
            "aTreatyList" : ["주계약","(무)크라운치료특약Ⅱ갱신형","(무)소액치과치료특약 Ⅱ(갱신형)"],
            "pTreatyList" : ["주계약","무)소액치과치료특약Ⅱ(갱신형)","무)크라운치료특약Ⅱ갱신형"]
          }
        res = requests.post("http://127.0.0.1:3100/getCompare",data=json.dumps(params))
        return res.text
