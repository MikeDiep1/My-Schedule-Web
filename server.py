from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
from datetime import datetime
import os
import stat


def get_body_params(body):
    if not body:
        return {}
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict

# if file_extension in mime_types:
#         full_path = f"static/{content_types[file_extension]}/{file_name}"
#         if check_file(full_path) == False:
#             return open("static/html/403.html").read(), "text/html; charset=utf-8"
#         elif file_extension in br_list: #read for binary type
#             return open(full_path, "br").read(), mime_types[file_extension]
#         return open(full_path).read(), mime_types[file_extension]
#     return open("static/html/404.html").read(), "text/html; charset=utf-8"

def submission_to_table(item):
    """TODO: Takes a dictionary of form parameters and returns an HTML table row

    An example input dictionary might look like: 
    {
     'event': 'Sleep',
     'day': 'Sun',
     'start': '01:00',
     'end': '11:00', 
     'phone': '1234567890', 
     'location': 'Home',
     'extra': 'Have a nice dream', 
     'url': 'https://example.com'
    }
    """
    tableRow = f"""
    <tr>
        <td>{item.get('eventName')}</td>
        <td>{item.get('dowdropdown')}</td>
        <td>{item.get('start time')}</td>
        <td>{item.get('end time')}</td>
        <td>{item.get('phoneNum')}</td>
        <td>{item.get('location')}</td>
        <td>{item.get('extraInfo')}</td>
        <td>{item.get('extraURL')}</td>
    </tr>
    """
    return tableRow


# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
def handle_req(url, body=None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/MyForm.html?name=joe` then the `url` parameter will have
    the value "/MyForm.html?name=joe"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """

    MIME_type = {".html": "text/html", ".css": "text/css", ".js": "application/javascript", ".png": "image/png", 
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".mp3": "audio/mpeg", ".txt": "text/plain"}

    #if file --> [.png, .jpg, .html....] extension
        #return true
    #else
        #return false

    # Get rid of any query string parameters
    url, * query_string = url.split("?", 1)
    print(url)
    param = {}
    if len(query_string) != 0:
        param = get_body_params(query_string[0])

    # Parse any form parameters submitted via POST
    parameters = get_body_params(body)

    if url == "/EventLog.html":
        return (
            """
        <!DOCTYPE html>
        <html lang="en">
            <head>
              <link rel="stylesheet" href="/css/Style.css">
              <script src="/js/javaScript.js"></script>
              <title> Event Submission </title>
            </head>
            <body>
                <header>
                <ul class="navBar">
                    <li><a href="MySchedule.html">Home</a></li>
                    <li style="float:right"><a href="AboutMe.html">About Me</a></li>
                    <li class="dropdown">
                    <a href="javascript:void(0)" class="dropbtn">Days of the Week</a>
                    <div class="dropdown-content">
                        <a href="Monday.html">Monday</a>
                        <a href="Tuesday.html">Tuesday</a>
                        <a href="Wednesday.html">Wednesday</a>
                        <a href="Thursday.html">Thursday</a>
                        <a href="Friday.html">Friday</a>
                        <a href="Saturday.html">Saturday</a>
                        <a href="Sunday.html">Sunday</a>
                    </div>
                    </li>
                    <li><a class="active" href="MyForm.html">Form Input</a></li>
                </ul>
                </header>
                <h1> My New Events </h1>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Day</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Phone</th>
                                <th>Location</th>
                                <th>Extra Info</th>
                                <th>URL</th>
                            </tr>
                        </thead>
                        <tbody>
                        """
                + (submission_to_table(parameters))
            + """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>""",
            "text/html; charset=utf-8",
        )

    elif os.path.exists("static/html" + url):
        if url.endswith(".html"):
            if (os.stat("static/html" + url).st_mode & stat.S_IROTH) > 0:
                return open("static/html" + url).read(), "text/html"
            else:
                return open("static/html/403.html").read(), "text/html; charset=utf-8"

    elif url.endswith(".css"):
        return open("static" + url).read(), "text/css"

    elif url.endswith(".js"):
        return open("static" + url).read(), "text/javascript"

    elif url.endswith(".png"):
        return open(("static" + url), "br").read(), "image/png"

    elif url.endswith(".jpg") or url.endswith(".jpeg"):
        return open(("static" + url), "br").read(), "image/jpeg"
    elif url.endswith(".mp3"):
        return open("static" + url, "br").read(), "audio/mpeg"
    
    # elif url.endswith(".txt"):

    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8"


class RequestHandler(BaseHTTPRequestHandler):
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body


    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        self.log_response(response_code, self.path, headers)


    def log_response(self, response, request, headers):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        log_line = f"{current_time}, {headers}, {request}, {response}\n"
        
        # Open the log file in append mode and write the log line
        with open("response.log", "a") as log_file:
            log_file.write(log_line)


    def do_GET(self):
        if self.path.startswith("/static"):
            self.path = "/" + os.path.basename(self.path)

        if self.path.startswith("/calculator"):
            self.path, *query_string = self.path.split("?", 1)
            param = {} 
            if query_string:
                param = get_body_params(query_string[0])
                
            if param['integer'] != "" and param['integer2'] != "" and param['anotherdowdropdown'] != "":
                if param['anotherdowdropdown'] == "Add":
                    answer =  int(param['integer']) + int(param['integer2'])
                elif param['anotherdowdropdown'] == "Subtract":
                    answer =  int(param['integer']) - int(param['integer2'])
                elif param['anotherdowdropdown'] == "Multiply":
                    answer =  int(param['integer']) * int(param['integer2'])
                elif param['anotherdowdropdown'] == "Divide":
                    answer =  int(param['integer']) / int(param['integer2'])

                calc_page = f"<html><body>{answer}</body></html>"

                self.__c_send_response(
                    calc_page,
                    307,
                    {
                        "Content-Type": "text/html",
                        "Content-Length": len(calc_page),
                        "X-Content-Type-Options": "nosniff",
                    },
                )
        elif self.path.startswith("/redirect"):
            self.path, *query_string = self.path.split("?", 1)
            param = {} 
            if query_string:
                param = get_body_params(query_string[0])

            if param['dowdropdown'] == 'Youtube':
                self.__c_send_response(
                    b'',  
                    307,
                    {"Location": "https://www.youtube.com/results?search_query=" + param['searchEngine']}  
                )
            elif param['dowdropdown'] == 'Google':
                self.__c_send_response(
                    b'',  
                    307,
                    {"Location": "https://www.google.com/search?q=" + param['searchEngine']}  
                )
        else:
            message, content_type = handle_req(self.path)
            # Convert the return value into a byte string for network transmission
            if type(message) == str:
                message = bytes(message, "utf8")

            self.__c_send_response(
                message,
                200,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )


    def do_POST(self):
        body = self.__c_read_body()
        message, content_type = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()