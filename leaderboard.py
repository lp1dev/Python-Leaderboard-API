#!/usr/bin/env python3

import json
from flask import Flask
from datetime import datetime

app = Flask(__name__)
leaderboard_file = "./leaderboard.csv"

if __name__ == "__main__":
    @app.route("/")    
    def leaderboard():
        with open(leaderboard_file) as f:
            entries = parse_entries(f.readlines())
        if (len(entries)):
            entries = sorted(entries, key=lambda entry: int(entry[1]))
        return json.dumps(entries)
    
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
                "time": entry[2].replace('\n', '')
            })
            
        return json.dumps(output)
    
    @app.route("/api/<nickname>/<score>/<time>")
    def add_score(nickname, score, time):
        with open(leaderboard_file, "a+") as f:
            f.write("%s;%s;%s\n" %(nickname, score, time))
        return "OK"
        
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, PUT, OPTIONS, PATCH, DELETE")
        response.headers.add('Access-Control-Allow-Headers',"Origin, X-Requested-With, Content-Type, Accept")
        response.headers.add('Content-Type','application/json')
        return response
                    
    app.run(host="127.0.0.1", port=8084, threaded=True)
