from Pjono.PARSE import HTML
import os
import json

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__ascii__ = json.load(open(os.path.join(__location__, "PARSE/ascii.json"), "r"))

class Http_Response():
    """
    Http_Response object for creating a http response
    
    `respond` attributes have the raw http response
    """
    def __init__(self, headers: dict={"Connection":"Closed","Content-Type":"text/html"}, content=None, HTTP: str="HTTP/1.1", status_code=(200, "OK")):
        self.respond = f"{HTTP} {status_code[0]} {status_code[1]}"
        self.status_code = status_code
        if content:
            if isinstance(content, HTML):
                content = content.content
            for i, v in headers.items():
                self.respond += f"\n{i}: {v}"
            self.respond = f"{self.respond}\n\n"
            if type(content) == bytes:
                self.respond = self.respond.encode()
                self.respond += bytearray(content)
            else:
                self.respond += content
        else:
            for i, v in headers.items():
                if isinstance(v, list):
                    if i == "Set-Cookie":
                        for cookie in v:
                            self.respond += f"\n{i}: {cookie}"
                else:
                    self.respond += f"\n{i}: {v}"

class Http_File(Http_Response):
    """
    Http_File object for building a http response with file content.
    Used to creating http response with binary file
    """
    def __init__(self, path: str, content_type: str, attachment: bool=False, filename: str=None, headers: dict=None):
        try:
            self.content = open(path, "r").read()
        except UnicodeDecodeError:
            self.content = open(path, "rb").read()
        if headers:
            headers["Content-Type"] = content_type
        else:
            headers = {
                "Content-Type": content_type
            }
        if attachment:
            if filename:
                headers["Content-Disposition"] = f"attachment; filename={filename}"
            else:
                headers["Content-Disposition"] = f"attachment"
        super().__init__(headers, content=self.content)

class StatusCodeError(Exception):
    pass

class Http_Redirect(Http_Response):
    """
    Redirecting client to specific url with parameters or not
    """
    def __init__(self, Location: str, headers: dict={}, status_code=(302, "Found"), HTTP: str="HTTP/1.1", **params):
        self.location = Location
        if status_code[0] > 399 or status_code[0] < 300:
            raise StatusCodeError("Status code can't be lower or higher than 300")
        if params:
            self.location += "?"
            for k, v in params.items():
                value = v.replace(" ", "+")
                ascii_char = list("qwertyuiopasdfghjklzxcvbnm+.0987654321")
                for hex, char in __ascii__.items():
                    if char.lower() in ascii_char:
                        continue
                    value = value.replace(char, hex)
                self.location += f"{k}={value}"
                if not list(params).index(k) >= len(params) - 1:
                    self.location += "&"
        super().__init__({**headers,"Location":self.location}, HTTP=HTTP, status_code=status_code)
        
