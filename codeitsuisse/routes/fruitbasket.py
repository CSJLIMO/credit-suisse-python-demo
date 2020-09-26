import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
    

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data();
    
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    print(data)
    logging.info("data sent for evaluation {}".format(data))
    
    dic = {'maPomegranate': 59, 'maRamubutan': 43, 'maPineapple': 8, 
           'maAvocado': 33, 'maApple': 31, 'maWatermelon': 84}
    ret = 0
    for key in data:
        ret += dic[key] * data[key]
        
    result = "{}".format(ret)
        
    # logging.info("My result :{}".format(n))
    # return jsonify({"answers": answer_dic});
    return result
















