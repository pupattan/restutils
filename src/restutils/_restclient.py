#######################################################################
# Module Name   : _restclient
# Author        : Pulak Pattanayak
# Date          : 17-05-2017
#######################################################################

#######################################################################
# Description : This modules provides classes to do REST Client side operations
#######################################################################

#######################################################################
# imports
#######################################################################
import urllib2
import ssl
import copy
import json
import httplib


#######################################################################
# classes
#######################################################################
class Result(object):
    def __init__(self, status_code, headers=None, data=None):
        self.headers = headers
        self.status = status_code
        self.data = data

    def get_header(self, header_name):
        if self.headers:
            for header in self.headers.keys():
                if header == header_name or header == header_name.lower():
                    return self.headers.get(header)
        return


class RESTClient(object):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __init__(self, base_url, **kwargs):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.content_type = kwargs.get("content_type", "application/json")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.session = kwargs.get("session")
        self.log = kwargs.get("log")

        if not self.log:
            import sys
            self.log = sys.stderr

        self.headers = {
            "Content-Type": self.content_type
        }

        if self.username:
            self.headers['X-Auth-User'] = self.username
        if self.password:
            self.headers['X-Auth-Key'] = self.password
        if self.session:
            self.headers['X-Auth-Session'] = self.session

    def get(self, url_path, **kwargs):
        return self.send_request(url_path, self.GET, **kwargs)

    def post(self, url_path, request_body="", **kwargs):
        return self.send_request(url_path, self.POST, request_body, **kwargs)

    def put(self, url_path, body="", **kwargs):
        return self.send_request(url_path, self.PUT, body, **kwargs)

    def delete(self, url_path, **kwargs):
        return self.send_request(url_path, self.DELETE, **kwargs)

    @staticmethod
    def _get_context():
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def send_request(self, url_path, request_method, request_body="", **kwargs):
        # Argument values
        headers = kwargs.get("headers")
        content_type = kwargs.get("content_type", self.content_type)
        if url_path.startswith("/"):
            url_path = url_path[1:]

        url = self.base_url+url_path
        msg = "\nURL\t\t:{}\nMethod\t:{}\n".format(url, request_method)
        self.log.write(msg)

        req_headers = copy.deepcopy(self.headers)
        if headers:
            req_headers.update(headers)
        req_headers['Content-Type'] = content_type

        if request_body:
            if isinstance(request_body, dict):
                try:
                    request_body = str(json.dumps(request_body))
                except Exception as e:
                    self.log.write(str(e))
            body_length = len(request_body)

            if body_length:
                req_headers['Content-Length'] = body_length

        response = None
        handler = urllib2.Request(url, request_body)
        handler.get_method = lambda: request_method
        if req_headers:
            for key, value in req_headers.items():
                handler.add_header(key, value)

        try:
            ctx = self._get_context()
            opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
            response = opener.open(handler)
        except Exception as e:
            self.log.write(str(e))

        # Response details
        data = None
        status_code = None
        resp_headers = dict()

        if response:
            status_code = response.getcode()
            res_string = response.read()
            if res_string:
                try:
                    data = json.loads(res_string)
                except Exception as e:
                    self.log.write(str(e))
            resp_headers = dict(response.info())

        # Set sessions
        ret_result = Result(headers=resp_headers, data=data, status_code=status_code)
        return ret_result

    def create_session(self, auth_url, body="", status=httplib.ACCEPTED, username=None, password=None):
        if username:
            self.headers['X-Auth-User'] = username
        if password:
            self.headers['X-Auth-Key'] = password
        result = self.post(auth_url, body=body)
        if result.status == status:
            session = result.get_header("X-Auth-Session")
            del self.headers['X-Auth-User']
            del self.headers['X-Auth-Key']
            self.headers['X-Auth-Session'] = session
            self.session = session
        return result

    def delete_session(self, auth_url, status=httplib.NO_CONTENT):
        result = self.delete(auth_url)
        if result.status == status:
            self.username = None
            self.password = None
            self.headers = {}
        return result
