import requests
import cmapy.schemas as schemas

Host = "http://ams:9000"

def get_agency_config(masid, agencyid):
    resp = requests.get(Host+"/api/clonemap/mas/"+str(masid)+"/agencies/"+str(agencyid))
    conf = schemas.AgencyConfig()
    conf.from_json(resp.text)
    return conf

def get_agent_address(masid, agentid):
    resp = requests.get(Host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid)+"/address")
    addr = schemas.Address()
    addr.from_json(resp.text)
    return addr