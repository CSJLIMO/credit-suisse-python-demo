import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

gr = []
vis = []
n = 0
m = 0

def dfs(x, y):
    global n, m, vis
    # print("dfs", x, y)
    vis[x][y] = 1
    dx = [0, 0, 1, -1, 1, 1, -1, -1]
    dy = [1, -1, 0, 0, 1, -1, 1, -1]

    for i in range(8):
        if 0<=x+dx[i] and x+dx[i]<n and 0<=y+dy[i] and y+dy[i]<m:
            if gr[x+dx[i]][y+dy[i]] != "*" and vis[x+dx[i]][y+dy[i]] == 0:
                dfs(x+dx[i], y+dy[i])
    

def get_ans():
    global n, m, vis
    n = len(gr)
    m = len(gr[0])
    for i in range(n):
        temp = []
        for j in range(m):
            temp.append(0)
        vis.append(temp)
        
    ans = 0
    for i in range(n):
        for j in range(m):
            if vis[i][j] == 0 and gr[i][j] == "1":
                ans += 1
                dfs(i, j)
                
    return ans



@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    n = len(data)
    m = len(data[0])
    for i in range(n):
        temp = []
        for j in range(m):
            temp.append(data[i][j])
        gr.append(temp)
    
    result = get_ans()
    
    # logging.info("My result :{}".format(result))
    return jsonify({"answer": result});



