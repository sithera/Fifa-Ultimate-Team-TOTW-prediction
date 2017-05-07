from flask import Flask
from data.main import players
app = Flask(__name__)


@app.route("/")
def main():
    output = players()
    return output

if __name__ == "__main__":
    app.run()

