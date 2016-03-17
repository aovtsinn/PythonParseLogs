import os
from flask import Flask
from flask import request
from jinja2 import Environment, FileSystemLoader
import argparse
import urllib
import GeoIP
import gzip

#to run on your own machine apt-get install python-flask (python3-flask)

env = Environment(
    loader=FileSystemLoader(os.path.join("templates")),
    trim_blocks=True)

app = Flask(__name__)

def list_log_files():
    for filename in os.listdir("/home/aovtsinn/Documents/Python/logs"):
        if not filename.startswith("access"):
            continue
        if filename.endswith(".log"):
            yield filename
        if filename.endswith(".gz"):
            yield filename

def humanize(bytes):
    if bytes < 1024:
        return "%d B" % bytes
    elif bytes < 1024 ** 2:
        return "%.1f kB" % (bytes / 1024.0)
    elif bytes < 1024 ** 3:
        return "%.1f MB" % (bytes / 1024.0 ** 2)
    else:
        return "%.1f GB" % (bytes / 1024.0 ** 3)



def parse_log_file(filename):
    if filename.endswith(".gz"):
        fh = gzip.open(os.path.join("/home/aovtsinn/Documents/Python/logs", filename))
    else:
        fh = open(os.path.join("/home/aovtsinn/Documents/Python/logs", filename))
    urls = {}
    user_bytes = {}

    for line in fh:
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
        except ValueError:
            continue # Skip garbage
        if path == "*": continue # Skip asterisk for path
        _, status_code, content_length, _ = response.split(" ")
        content_length = int(content_length)
        path = urllib.unquote(path)
        if path.startswith("/~"):
            username = path[2:].split("/")[0]
            try:
                user_bytes[username] = user_bytes[username] + content_length
            except:
                user_bytes[username] = content_length

        try:
            urls[path] = urls[path] + 1
        except:
            urls[path] = 1
    return urls, user_bytes


@app.route("/report/")
def report():
    if "/" in request.args.get("filename"):
        return "GO HOME YOU'RE DRUNK!"
    urls, user_bytes = parse_log_file(request.args.get("filename"))
    user_bytes = sorted(user_bytes.items(), key = lambda item:item[1], reverse=True)
    return env.get_template("report.html").render(
        urls = urls, 
        user_bytes = user_bytes,
        humanize = humanize)

@app.route("/")

def hello():
    return env.get_template("index.html").render(
        log_files=list_log_files())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
