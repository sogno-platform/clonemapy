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
    resp = requests.get("http://"+host+"/api/clonemap")
    if resp.status_code == 200:
        return datamodels.CloneMAP.parse_raw(resp.text)
    logging.error("AMS error")
    return None


def get_mass(host: str) -> List[datamodels.MASInfoShort]:
    resp = requests.get("http://"+host+"/api/clonemap/mas")
    if resp.status_code == 200:
        mass = []
        mas_dicts = json.loads(resp.text)
        if mas_dicts is None:
            return mass
        for i in mas_dicts:
            mass.append(datamodels.MASInfoShort.parse_obj(i))
        return mass
    logging.error("AMS error")
    return None


def post_mas(host: str, mas: datamodels.MASSpec):
    """
    post mas spec to start a mas
    """
    js = mas.json()
    resp = requests.post("http://"+host+"/api/clonemap/mas", data=js)
    if resp.status_code != 201:
        logging.error("AMS error")


def get_mas(host: str, masid: int) -> datamodels.MASInfo:
    """
    get info of mas
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid))
    if resp.status_code == 200:
        return datamodels.MASInfo.parse_raw(resp.text)
    logging.error("AMS error")
    return None


def delete_mas(host: str, masid: int):
    resp = requests.delete("http://"+host+"/api/clonemap/mas/"+str(masid))
    if resp.status_code != 201:
        logging.error("AMS error")


def get_agents(host: str, masid: int) -> datamodels.Agents:
    """
    get agents in mas
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents")
    if resp.status_code == 200:
        return datamodels.Agents.parse_raw(resp.text)
    logging.error("AMS error")
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
    resp = requests.post("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents", data=js)
    if resp.status_code != 201:
        logging.error("AMS error")


def get_agent(host: str, masid: int, agentid: int) -> datamodels.AgentInfo:
    """
    get agents in mas
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid))
    if resp.status_code == 200:
        return datamodels.AgentInfo.parse_raw(resp.text)
    logging.error("AMS error")
    return None


def get_agent_address(host: str, masid: int, agentid: int) -> datamodels.Address:
    """
    get address of agent
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid) +
                        "/address")
    if resp.status_code == 200:
        return datamodels.Address.parse_raw(resp.text)
    logging.error("AMS error")
    return None


def delete_agent(host: str, masid: int, agentid: int):
    resp = requests.delete("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agents/"+str(agentid))
    if resp.status_code != 201:
        logging.error("AMS error")


def get_agencies(host: str, masid: int) -> datamodels.Agencies:
    """
    get agencies in mas
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid)+"/agencies")
    if resp.status_code == 200:
        return datamodels.Agencies.parse_raw(resp.text)
    logging.error("AMS error")
    return None


def get_agency_info_full(host: str, masid: int, imid: int,
                         agencyid: int) -> datamodels.AgencyInfoFull:
    """
    get configuration of agency
    """
    resp = requests.get("http://"+host+"/api/clonemap/mas/"+str(masid)+"/imgroup/"+str(imid) +
                        "/agency/"+str(agencyid))
    if resp.status_code == 200:
        return datamodels.AgencyInfoFull.parse_raw(resp.text)
    logging.error("AMS error")
    return None
