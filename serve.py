#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
from threading import Thread

from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from build import build, BUILD_ROOT, SRC_ROOT


if sys.version_info < (3, 7):
    raise Exception("Python >= 3.7 is required")


class RebuildHandler(FileSystemEventHandler):
    def __init__(self):
        self.building = False
        super(RebuildHandler, self).__init__()

    def on_any_event(self, event):
        if self.building:
            return
        if event.is_directory or event.src_path.startswith(BUILD_ROOT):
            return
        print(f"{event.src_path} changed")
        self.building = True
        build()
        self.building = False


class HTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(HTTPHandler, self).__init__(*args, directory=BUILD_ROOT, **kwargs)


class HTTPServerThread(Thread):
    def __init__(self):
        super(HTTPServerThread, self).__init__()

    def run(self):
        self.httpd = HTTPServer(("localhost", 8000), HTTPHandler)
        address = self.httpd.server_address
        print(f"serving website at http://{address[0]}:{address[1]}\n")
        self.httpd.serve_forever()

    def join(self):
        self.httpd.shutdown()
        super(HTTPServerThread, self).join()


def main():
    build()

    handler = RebuildHandler()
    observer = Observer()
    observer.schedule(handler, SRC_ROOT, recursive=True)
    observer.start()

    server = HTTPServerThread()
    server.run()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
        server.join()


if __name__ == "__main__":
    main()
