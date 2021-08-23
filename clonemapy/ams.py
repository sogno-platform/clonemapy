# Copyright 2020 Institute for Automation of Complex Power Systems,
# E.ON Energy Research Center, RWTH Aachen University
#
# This project is licensed under either of
# - Apache License, Version 2.0
# - MIT License
# at your option.
#
# Apache License, Version 2.0:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module implements necessary client methods for the cloneMAP AMS
"""
import requests
import logging
import json
from typing import List
import clonemapy.datamodels as datamodels


def alive(host: str) -> bool:
    resp = requests.get("http://"+host+"/api/alive")
    if resp.status_code == 200:
        return True
    return False


def get_clonemap(host: str) -> datamodels.CloneMAP:
    url = "http://"+host+"/api/clonemap"
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.CloneMAP.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def get_mass(host: str) -> List[datamodels.MASInfoShort]:
    url = "http://"+host+"/api/clonemap/mas"
    resp = requests.get(url)
    if resp.status_code == 200:
        mass = []
        mas_dicts = json.loads(resp.text)
        if mas_dicts is None:
            return mass
        for i in mas_dicts:
            mass.append(datamodels.MASInfoShort.parse_obj(i))
        return mass
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def get_mass_by_name(host: str, mas_name: str) -> List[int]:
    url = "http://"+host+"/api/clonemap/mas/name/"+mas_name
    resp = requests.get(url)
    if resp.status_code == 200:
        mass = json.loads(resp.text)
        return mass
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def post_mas(host: str, mas: datamodels.MASSpec):
    """
    post mas spec to start a mas
    """
    js = mas.json()
    url = "http://"+host+"/api/clonemap/mas"
    resp = requests.post(url, data=js)
    if resp.status_code != 201:
        logging.error("AMS error for POST "+url+" Code: "+str(resp.status_code)+", Body: " +
                      resp.text)


def get_mas(host: str, masid: int) -> datamodels.MASInfo:
    """
    get info of mas
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.MASInfo.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def delete_mas(host: str, masid: int):
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)
    resp = requests.delete(url)
    if resp.status_code != 200:
        logging.error("AMS error for DELETE "+url+" Code: "+str(resp.status_code)+", Body: " +
                      resp.text)


def delete_all_mass(host: str):
    url = "http://"+host+"/api/clonemap/mas"
    resp = requests.delete(url)
    if resp.status_code != 200:
        logging.error("AMS error for DELETE "+url+" Code: "+str(resp.status_code)+", Body: " +
                      resp.text)


def get_agents(host: str, masid: int) -> datamodels.Agents:
    """
    get agents in mas
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents"
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.Agents.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def get_agents_by_name(host: str, masid: int, agent_name) -> List[int]:
    """
    get agents in mas by name
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/name/"+agent_name
    resp = requests.get(url)
    if resp.status_code == 200:
        agents = json.loads(resp.text)
        return agents
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def post_agents(host: str, masid: int, im_specs: List[datamodels.ImageGroupSpec]):
    """
    post agents
    """
    im_dicts = []
    for i in im_specs:
        im_dict = json.loads(i.json())
        im_dicts.append(im_dict)
    js = json.dumps(im_dicts)
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents"
    resp = requests.post(url, data=js)
    if resp.status_code != 201:
        logging.error("AMS error for POST "+url+" Code: "+str(resp.status_code)+", Body: " +
                      resp.text)


def get_agent(host: str, masid: int, agentid: int) -> datamodels.AgentInfo:
    """
    get agents in mas
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid)
    resp = requests.get()
    if resp.status_code == 200:
        return datamodels.AgentInfo.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def get_agent_address(host: str, masid: int, agentid: int) -> datamodels.Address:
    """
    get address of agent
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid) + "/address"
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.Address.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def delete_agent(host: str, masid: int, agentid: int):
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid)
    resp = requests.delete(url)
    if resp.status_code != 200:
        logging.error("AMS error for DELETE "+url+" Code: "+str(resp.status_code)+", Body: " +
                      resp.text)


def put_agent_custom(host: str, masid: int, agentid: int, custom: str):
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid) + "/custom"
    resp = requests.put(url, data=custom)
    if resp.status_code != 200:
        logging.error("AMS error for PUT "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)


def get_agencies(host: str, masid: int) -> datamodels.Agencies:
    """
    get agencies in mas
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/agencies"
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.Agencies.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def get_agency_info_full(host: str, masid: int, imid: int,
                         agencyid: int) -> datamodels.AgencyInfoFull:
    """
    get configuration of agency
    """
    url = "http://"+host+"/api/clonemap/mas/"+str(masid)+"/imgroup/"+str(imid) + "/agency/"
    url += str(agencyid)
    resp = requests.get(url)
    if resp.status_code == 200:
        return datamodels.AgencyInfoFull.parse_raw(resp.text)
    logging.error("AMS error for GET "+url+" Code: "+str(resp.status_code)+", Body: "+resp.text)
    return None


def new_agent(host: str, image: str, secret: str, masid: int, name: str, custom: str):
    im_group_config = datamodels.ImageGroupConfig(image=image, secret=secret)
    agent_spec = datamodels.AgentSpec(nodeid=0, name=name, custom=custom)
    agent_specs = [agent_spec]
    im_group_spec = datamodels.ImageGroupSpec(config=im_group_config, agents=agent_specs)
    im_group_specs = [im_group_spec]
    post_agents(host, masid, im_group_specs)


def update_or_create_agent(host: str, image: str, secret: str, masid: int, name: str, custom: str):
    agents = get_agents_by_name(host, masid, name)
    if agents is None:
        new_agent(host, image, secret, masid, name, custom)
        return
    if len(agents) > 1:
        logging.error("agent "+name+" already exists")
        return
    agentid = agents[0]
    put_agent_custom(host, masid, agentid, custom)


if __name__ == "__main__":
    update_or_create_agent("137.226.133.171:30009",
                           "registry.git-ce.rwth-aachen.de/ebc/projects/ebc_acs0017_bmwi_agent/agents_python/agentlib:base",
                           "agentlib", 0,
                           "superagent",
                           "blabla")
    agents = get_agents("137.226.133.171:30009", 0)
    print(agents)
