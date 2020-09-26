import logging
import json
import numpy as np
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_ans(port_val, sigma_s, futures):
    best_hedge_ratio = 2
    best_index = -1
    for i in range(len(futures)):
        future = futures[i]
        hedge_ratio = future["CoRelationCoefficient"] * sigma_s / future["FuturePrcVol"]
        hedge_ratio = round(hedge_ratio, 3)
        if hedge_ratio < best_hedge_ratio:
            best_hedge_ratio = hedge_ratio
            best_index = i
            
    name = futures[best_index]["Name"]
    contracts = best_hedge_ratio * port_val / (futures[best_index]["IndexFuturePrice"] * futures[best_index]["Notional"])
    contracts = int(round(contracts, 0))
    
    return {"HedgePositionName": name, "OptimalHedgeRatio": best_hedge_ratio, "NumFuturesContract": contracts}



@app.route('/optimizeportfolio', methods=['POST'])
def evaluate_optimizeportfolio():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    outputs = []
    for test_case in data["inputs"]:
        port_val = test_case["Portfolio"]["Value"]
        sigma_s = test_case["Portfolio"]["SpotPrcVol"]
        futures = test_case["IndexFutures"]
        outputs.append(get_ans(port_val, sigma_s, futures))
        

    # logging.info("My result :{}".format(result))
    return jsonify({"outputs": outputs});



