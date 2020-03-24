"""
This module implements necessary client methods for the cloneMAP logger
"""
import requests
import json
import cmapy.schemas as schemas

Host = "http://logger:11000"

def post_logs(masid, logs):
    """
    post array of log messages to logger
    """
    log_dicts = []
    for i in logs:
        log_dict = i.to_json_dict()
        log_dicts.append(log_dict)
    js = json.dumps(log_dicts)
    requests.post(Host+"/api/logging/"+str(masid)+"/list", data=js)

def put_state(masid, agentid, state):
    """
    update state of agent
    """
    js = state.to_json()
    requests.post(Host+"/api/state/"+str(masid)+"/"+str(agentid), data=js)

def get_state(masid, agentid):
    """
    request state of agent
    """
    resp = requests.get(Host+"/api/state/"+str(masid)+"/"+str(agentid))
    state = schemas.State()
    state.from_json(resp.text)
    return state

def send_logs(masid, log_queue):
    """
    wait for logs in the queue and send them to logger (to be executed in seperate thread)
    """
    while True:
        log = log_queue.get()
        logs = []
        logs.append(log)
        post_logs(masid, logs)
