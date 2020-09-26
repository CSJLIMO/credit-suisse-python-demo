import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def diff(s1, s2):
    ret = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            ret += 1
    return ret

def star(s1, s2):
    num = 0
    for i in range(len(s1)):
        if i % 4 == 0 and s1[i] != s2[i]:
            num += 1
    if num > 1:
        return True
    return False

name_dic = {}
all_poss = []
origin_gen = 0
origin_name = 0

def get_path(path):
    global name_dic, all_poss, origin_gen, origin_name
    
    if name_dic[path[-1]] == origin_gen:
        all_poss.append(path)
        return
    
    min_diff = 1000000000
    for name in name_dic:
        if name not in path:
            min_diff = min(min_diff, diff(name_dic[path[-1]], name_dic[name]))
    for name in name_dic:
        if name not in path and diff(name_dic[path[-1]], name_dic[name]) == min_diff:
            new_path = []
            for item in path:
                new_path.append(item)
            new_path.append(name)
            get_path(new_path)

@app.route('/contact_trace', methods=['POST'])
def evaluate_contact_trace():
    global name_dic, all_poss, origin_gen, origin_name
    name_dic = {}
    all_poss = []
    
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    infected_gen = data["infected"]["genome"]
    infected_name = data["infected"]["name"]
    origin_gen = data["origin"]["genome"]
    origin_name = data["origin"]["name"]
    name_dic[infected_name] = infected_gen
    name_dic[origin_name] = origin_gen
    for item in data["cluster"]:
        name_dic[item["name"]] = item["genome"]
            
    if infected_gen == origin_gen:
        op = []
        for name in name_dic:
            if name_dic[name] == origin_gen and name != infected_name:
                op.append(infected_name + " -> " + name)
        return jsonify(op)
    
    get_path([infected_name])
    op = []
    for path in all_poss:
        ans_str = path[0]
        for i in range(1, len(path)):
            if star(name_dic[path[i-1]], name_dic[path[i]]):
                ans_str += "* -> "
                ans_str += path[i]
            else:
                ans_str += " -> "
                ans_str += path[i]
        op.append(ans_str)
    return jsonify(op)
    
        
    

    
    # logging.info("My result :{}".format(result))
    # return jsonify({"answers": answer_dic});



