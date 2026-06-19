from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


PORT = 8501
ROOT = Path(__file__).resolve().parent


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


def main() -> None:
    address = ("localhost", PORT)
    server = ThreadingHTTPServer(address, AppHandler)
    url = f"http://{address[0]}:{address[1]}/index.html"
    print("Skill2Salary AI Pro is running")
    print(f"Open: {url}")
    webbrowser.open(url)
    server.serve_forever()


if __name__ == "__main__":
    main()
