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
import logging
import clonemapy.datamodels as datamodels
import os
import queue
from typing import List

Host = "http://logger:11000"


def alive() -> bool:
    resp = requests.get(Host+"/api/alive")
    if resp.status_code == 200:
        return True
    return False


def post_logs(masid: int, logs: List[datamodels.LogMessage]):
    """
    post array of log messages to logger
    """
    log_dicts = []
    for i in logs:
        log_dict = json.loads(i.json())
        log_dicts.append(log_dict)
    js = json.dumps(log_dicts)
    resp = requests.post(Host+"/api/logging/"+str(masid)+"/list", data=js)
    if resp.status_code != 201:
        logging.error("Logger error")


def get_latest_logs(masid: int, agentid: int, topic: str, num: int) -> List[datamodels.LogMessage]:
    logs = []
    resp = requests.get(Host+"/api/logging/"+str(masid)+"/"+str(agentid)+"/"+topic+"/latest/" +
                        str(num))
    if resp.status_code == 200:
        log_dicts = json.loads(resp.text)
        if log_dicts is None:
            return logs
        for i in log_dicts:
            log = datamodels.LogMessage.parse_obj(i)
            logs.append(log)
    else:
        logging.error("DF error")
    return logs


def post_timeseries_data(masid: int, ts: List[datamodels.TimeSeriesData]):
    """
    post array of time series data to logger
    """
    ts_dicts = []
    for i in ts:
        ts_dict = json.loads(i.json())
        ts_dicts.append(ts_dict)
    js = json.dumps(ts_dicts)
    resp = requests.post(Host+"/api/series/"+str(masid), data=js)
    if resp.status_code != 201:
        logging.error("Logger error")


def put_state(masid: int, agentid: int, state: datamodels.State):
    """
    update state of agent
    """
    js = state.json()
    resp = requests.post(Host+"/api/state/"+str(masid)+"/"+str(agentid), data=js)
    if resp.status_code != 201:
        logging.error("Logger error")


def update_states(masid: int, states: List[datamodels.State]):
    state_dicts = []
    for i in states:
        state_dict = json.loads(i.json())
        state_dicts.append(state_dict)
    js = json.dumps(state_dicts)
    resp = requests.post(Host+"/api/state/"+str(masid)+"/list", data=js)
    if resp.status_code != 201:
        logging.error("Logger error")


def get_state(masid: int, agentid: int) -> datamodels.State:
    """
    request state of agent
    """
    resp = requests.get(Host+"/api/state/"+str(masid)+"/"+str(agentid))
    if resp.status_code == 200:
        return datamodels.State.parse_raw(resp.text)
    return None


def send_logs(masid: int, log_queue: queue.Queue):
    """
    wait for logs in the queue and send them to logger (to be executed in seperate thread)
    """
    log_on = os.environ['CLONEMAP_LOGGING']
    while True:
        log = log_queue.get()
        if log_on == "ON":
            logs = []
            logs.append(log)
            post_logs(masid, logs)
        else:
            print(log.json())


def send_timeseries_data(masid: int, ts_queue: queue.Queue):
    """
    wait for timeseries data in the queue and send them to logger (to be executed in seperate thread)
    """
    log_on = os.environ['CLONEMAP_LOGGING']
    while True:
        ts = ts_queue.get()
        if log_on == "ON":
            tss = []
            tss.append(ts)
            post_logs(masid, tss)
        else:
            pass
