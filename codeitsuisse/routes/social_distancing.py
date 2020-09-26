import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_ans(x, y, z):
    if x < (y-1) * z + y:
        return 0
    dp = []
    for i in range(x+1):
        temp = []
        for j in range(y+1):
            temp.append(0)
        dp.append(temp)
    
    for i in range(x+1):
        dp[i][0] = 1
    for i in range(x+1):
        dp[i][1] = i
    for j in range(2, y+1):
        for i in range(x+1):
            if i == 0:
                dp[i][j] = 0
                continue
            dp[i][j] = dp[i-1][j]
            if i-z-1>=0:
                dp[i][j] += dp[i-z-1][j-1]
    return dp[x][y]

@app.route('/social_distancing', methods=['POST'])
def evaluate_social_distancing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    
    answer_dic = {}
    for key in data["tests"]:
        x = data["tests"][key]["seats"]
        y = data["tests"][key]["people"]
        z = data["tests"][key]["spaces"]
        answer_dic[key] = get_ans(x, y, z)

    # logging.info("My result :{}".format(result))
    return jsonify({"answers": answer_dic});



