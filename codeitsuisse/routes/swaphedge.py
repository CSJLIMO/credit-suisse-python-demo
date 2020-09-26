import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
    

@app.route('/swaphedge', methods=['POST'])
def evaluate_swaphedge():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    order = int(data["accu_order"] - data["our_position"])
    if abs(order) <= 10:
        order = 0
    

    
    logging.info("My result :{}".format(order))
    return jsonify({"order": order});






