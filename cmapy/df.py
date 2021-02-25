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
This module implements necessary client methods for the cloneMAP DF
"""
import requests
import json
import logging
import cmapy.datamodels as datamodels

Host = "http://df:12000"


def post_svc(masid: int, svc: datamodels.Service) -> datamodels.Service:
    """
    post service to DF
    """
    js = svc.to_json()
    resp = requests.post(Host+"/api/df/"+str(masid)+"/svc", data=js)
    if resp.status_code == 201:
        svc.from_json(resp.text)
    else:
        logging.error("DF error")
    return svc


def get_svc(masid: int, desc: str) -> list:
    """
    request services with matching description
    """
    svcs = []
    resp = requests.get(Host+"/api/df/"+str(masid)+"/svc/desc/"+desc)
    if resp.status_code == 200:
        svc_dicts = json.loads(resp.text)
        if svc_dicts is None:
            return svcs
        for i in svc_dicts:
            svc = datamodels.Service()
            svc.from_json_dict(i)
            svcs.append(svc)
    else:
        logging.error("DF error")
    return svcs


def get_local_svc(masid: int, desc: str, nodeid: int, dist: float) -> list:
    """
    request local services with matching description
    """
    svcs = []
    resp = requests.get(Host+"/api/df/"+str(masid)+"/svc/desc/"+desc+"/node/"+str(nodeid)+"/dist/" +
                        str(dist))
    if resp.status_code == 200:
        svc_dicts = json.loads(resp.text)
        if svc_dicts is None:
            return svcs
        for i in svc_dicts:
            svc = datamodels.Service()
            svc.from_json_dict(i)
            svcs.append(svc)
    else:
        logging.error("DF error")
    return svcs


def delete_svc(masid: int, svcid: int):
    """
    delete service with svcid
    """
    resp = requests.delete(Host+"/api/df/"+str(masid)+"/svc/id/"+svcid)
    if resp.status_code != 200:
        logging.error("DF error")
