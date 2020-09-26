import logging
import json
import numpy as np
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def my_round(num, k):
    up = math.ceil(num * (10 ** k)) / (10 ** k)
    down = math.floor(num * (10 ** k)) / (10 ** k)
    dup = abs(num - up)
    ddown = abs(num - down + 0.0000001)
    if dup > ddown:
        return down
    return up


def get_ans(port_val, sigma_s, futures):
    hedge_ratios = []
    sigma_fs = []
    for i in range(len(futures)):
        future = futures[i]
        hedge_ratios.append(my_round(future["CoRelationCoefficient"] * sigma_s / future["FuturePrcVol"], 3))
        sigma_fs.append(future["FuturePrcVol"])
        
    convex_ind = []
    for i in range(len(futures)):
        dominated = False
        for j in range(len(futures)):
            if j != i and hedge_ratios[j] < hedge_ratios[i] and sigma_fs[j] < sigma_fs[i]:
                dominated = True
                break
        if not dominated:
            convex_ind.append(i)
    
    if len(convex_ind) > 1:
        convex_ind = [i for i in range(len(futures))]
    
    best_contracts = 1000000000
    best_ind = -1
    for ind in convex_ind:
        contracts = my_round(hedge_ratios[ind] * port_val / (futures[ind]["IndexFuturePrice"] * futures[ind]["Notional"]), 0)
        if contracts < best_contracts:
            best_contracts = contracts
            best_ind = ind
            
    name = futures[best_ind]["Name"]    
    return {"HedgePositionName": name, "OptimalHedgeRatio": hedge_ratios[best_ind], "NumFuturesContract": int(best_contracts + 0.3)}
            
    


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimizeportfolio():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    outputs = []
    for test_case in data["inputs"]:
        port_val = test_case["Portfolio"]["Value"]
        sigma_s = test_case["Portfolio"]["SpotPrcVol"]
        futures = test_case["IndexFutures"]
        outputs.append(get_ans(port_val, sigma_s, futures))
        

    logging.info("My result :{}".format(outputs))
    return jsonify({"outputs": outputs});





















