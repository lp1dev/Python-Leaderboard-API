#!/usr/bin/env python3

import json
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)
leaderboard_file = "./leaderboard_fethi.csv"

if __name__ == "__main__":
    @app.route("/")    
    def leaderboard():
        routes = {
            "/api/json": {
                "method": "GET",
                "params": {},
                "description": "Return JSON formatted leaderboard data"
            },
            "/api/json/<username>": {
                "method": "GET",
                "params": {},
                "description": "Return a JSON formatted array of a specific user's scores"
            },
            "/api/score": {
                "method": "POST",
                "params": {
                    "nickname": "[string] The player's nickname",
                    "score": "[number] The player's score",
                    "time": "[number] The player's game time (in seconds)",
                    "avatar_url": "[string] The player's avatar's URL"
                },
                "description": "Add a score to the leaderboard"
            }
        }
        return json.dumps(routes)

    def parse_entries(raw_lines):
        entries = []
        for entry in raw_lines:
            if (len(entry) > 1):
                entries.append(entry.split(";"))
        return entries

    @app.route("/api/json")
    def get_json():
        output = []
        with open(leaderboard_file) as f:
            entries = parse_entries(f.readlines())
        for entry in entries:
            output.append({
                "nickname": entry[0],
                "score": entry[1],
                "time": entry[2],
                "avatar_url": entry[3].replace('\n', '')
            })
            
        return json.dumps(output)

    @app.route("/api/json/<username>")
    def get_json_by_username(username):
        output = []
        with open(leaderboard_file) as f:
            entries = parse_entries(f.readlines())
        for entry in entries:
            if entry[0] == username:
                output.append({
                "nickname": entry[0],
                "score": entry[1],
                "time": entry[2],
                "avatar_url": entry[3].replace('\n', '')
            })
        return json.dumps(output)
    
    @app.route("/api/score", methods=['POST'])
    def add_score():
        if request.json is None:
            return json.dumps({"error": "Missing parameters"}), 400
        params = request.json
        print(params)
        for param in ['nickname', 'score', 'time', 'avatar_url']:
            if param not in params.keys():
                return json.dumps({"error": "Missing parameter %s" %param}), 400
        with open(leaderboard_file, "a+") as f:
           output = "%s;%s;%s;%s\n" %(params['nickname'], params['score'], params['time'], params['avatar_url'])
           f.write(output.replace('{', '').replace('}', ''))
        return json.dumps({"message": "OK"})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, PUT, OPTIONS, PATCH, DELETE")
        response.headers.add('Access-Control-Allow-Headers',"Origin, X-Requested-With, Content-Type, Accept")
        response.headers.add('Content-Type','application/json')
        return response
                    
    app.run(host="127.0.0.1", port=8089, threaded=True)
