import requests
import cmapy.schemas as schemas

Host = "http://ams:9000"

def get_agency_config(masid, agencyid):
    resp = requests.get(Host+"/api/clonemap/mas/"+str(masid)+"/agencies/"+str(agencyid))
    conf = schemas.AgencyConfig()
    conf.from_json(resp.text)
    return conf