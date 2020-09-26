import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    
    n = len(data)
    m = len(data[0])
    vis = []
    for i in range(n):
        temp = []
        for j in range(m):
            temp.append(0)
        vis.append(temp)
        
    dx = [0, 0, 1, -1, 1, 1, -1, -1]
    dy = [1, -1, 0, 0, 1, -1, 1, -1]
    
    dfs_list = []
    ans = 0
    for i in range(n):
        for j in range(m):
            if data[i][j] == "1" and vis[i][j] == 0:
                ans += 1
                dfs_list.append([i, j])
            while len(dfs_list) > 0:
                X = dfs_list[-1][0]
                Y = dfs_list[-1][1]
                if vis[X][Y] == 1:
                    dfs_list.pop()
                    continue
                vis[X][Y] = 1
                for k in range(8):
                    if 0<=X+dx[k] and X+dx[k]<n and 0<=Y+dy[k] and Y+dy[k]<m:
                        if data[X+dx[k]][Y+dy[k]] != "*":
                            dfs_list.append([X+dx[k], Y+dy[k]])

    # logging.info("My result :{}".format(result))
    return jsonify({"answer": ans});










