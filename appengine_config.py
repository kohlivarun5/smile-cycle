# Copyright 2016 Google Inc.
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

# [START vendor]
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# [END vendor] 


# Step 1: first add requests and requests-toolbelt to your requirements.txt (or however you install them via pip)
# Step 2: in appengine_config.py add the following snippet:

# see https://cloud.google.com/appengine/docs/python/issue-requests#issuing_an_http_request
import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

# also monkey patch platform.platform() from https://code.google.com/p/googleappengine/issues/detail?id=12982
import platform

def patch(module):
    def decorate(func):
        setattr(module, func.func_name, func)
        return func
    return decorate


@patch(platform)
def platform():
    return 'AppEngine'
