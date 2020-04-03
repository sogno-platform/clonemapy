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
