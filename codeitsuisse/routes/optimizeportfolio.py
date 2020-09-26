import logging
import json
import numpy as np
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def get_ans(port_val, sigma_s, futures):
    best_hedge_ratio = 2
    best_hedge_ratio_index = -1
    for i in range(len(futures)):
        future = futures[i]
        hedge_ratio = future["CoRelationCoefficient"] * sigma_s / future["FuturePrcVol"]
        hedge_ratio = round(hedge_ratio, 3)
        if hedge_ratio < best_hedge_ratio:
            best_hedge_ratio = hedge_ratio
            best_hedge_ratio_index = i
            
    best_sigma_f = 2
    best_sigma_f_index = -1
    for i in range(len(futures)):
        future = futures[i]
        if future["FuturePrcVol"] < best_sigma_f:
            best_sigma_f = future["FuturePrcVol"]
            best_sigma_f_index = i
            
    best_index = -1
    if best_hedge_ratio_index == best_sigma_f_index:
        best_index = best_hedge_ratio_index
    else:
        future1 = futures[best_hedge_ratio_index]
        future2 = futures[best_sigma_f_index]
        contracts1 = future1["CoRelationCoefficient"] * sigma_s / future1["CoRelationCoefficient"] * port_val / (future1["IndexFuturePrice"] * future1["Notional"])
        contracts2 = future2["CoRelationCoefficient"] * sigma_s / future2["CoRelationCoefficient"] * port_val / (future2["IndexFuturePrice"] * future2["Notional"])
        if contracts1 < contracts2:
            best_index = best_hedge_ratio_index
        else:
            best_index = best_sigma_f_index
            
    name = futures[best_index]["Name"]
    contracts = best_hedge_ratio * port_val / (futures[best_index]["IndexFuturePrice"] * futures[best_index]["Notional"])
    contracts = int(round(contracts, 0))
    
    return {"HedgePositionName": name, "OptimalHedgeRatio": best_hedge_ratio, "NumFuturesContract": contracts}
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









