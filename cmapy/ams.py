"""
This module implements necessary client methods for the cloneMAP AMS
"""
import requests
import cmapy.schemas as schemas

Host = "http://ams:9000"

def get_agency_config(masid, agencyid):
    """
    get configuration of agency
    """
    resp = requests.get(Host+"/api/clonemap/mas/"+str(masid)+"/agencies/"+str(agencyid))
    conf = schemas.AgencyConfig()
    conf.from_json(resp.text)
    return conf

def get_agent_address(masid, agentid):
    """
    get address of agent
    """
    resp = requests.get(Host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid)+"/address")
    addr = schemas.Address()
    addr.from_json(resp.text)
    return addr