from flask import Flask

from data.DBHandler import DBHandler

app = Flask(__name__)


@app.route("/")
def main():
    db = DBHandler()
    output = db.get_all_players()
    return output

if __name__ == "__main__":
    app.run()

