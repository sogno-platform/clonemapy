import requests
import json
import cmapy.schemas as schemas

Host = "http://logger:11000"

def post_logs(masid, logs):
    log_dicts = []
    for i in logs:
        log_dict = i.to_json_dict()
        log_dicts.append(log_dict)
    js = json.dumps(log_dicts)
    resp = requests.post(Host+"/api/logging/"+str(masid)+"/list", data=js)

def put_state(masid, agentid, state):
    js = state.to_json()
    resp = requests.post(Host+"/api/state/"+str(masid)+"/"+str(agentid), data=js)

def get_state(masid, agentid):
    resp = requests.get(Host+"/api/state/"+str(masid)+"/"+str(agentid))
    state = schemas.State()
    state.from_json(resp.text)
    return state