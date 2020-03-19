"""
This module implements necessary client methods for the cloneMAP DF
"""
import requests
import json
import cmapy.schemas as schemas

Host = "http://df:12000"

def post_svc(masid, svc):
    """
    post service to DF
    """
    js = svc.to_json()
    resp = requests.post(Host+"/api/df/"+str(masid)+"/svc", data=js)
    svc.from_json(resp.text)
    return svc

def get_svc(masid, desc):
    """
    request services with matching description
    """
    resp = requests.get(Host+"/api/df/"+str(masid)+"/svc/desc/"+desc)
    svc_dicts = json.loads(resp.text)
    svcs = []
    if svc_dicts == None:
        return svcs
    for i in svc_dicts:
        svc = schemas.Service()
        svc.from_json_dict(i)
        svcs.append(svc)
    return svcs

def get_local_svc(masid, desc, nodeid, dist):
    """
    request local services with matching description
    """
    resp = requests.get(Host+"/api/df/"+str(masid)+"/svc/desc/"+desc+"/node/"+str(nodeid)+"/dist/"+str(dist))
    svc_dicts = json.loads(resp.text)
    svcs = []
    if svc_dicts == None:
        return svcs
    for i in svc_dicts:
        svc = schemas.Service()
        svc.from_json_dict(i)
        svcs.append(svc)
    return svcs

def delete_svc(masid, svcid):
    """
    delete service with svcid
    """
    resp = requests.delete(Host+"/api/df/"+str(masid)+"/svc/id/"+svcid)