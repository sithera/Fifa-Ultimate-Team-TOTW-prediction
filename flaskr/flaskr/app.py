from flask import Flask, request, render_template

from data.DBHandler import DBHandler

app = Flask(__name__)


@app.route("/")
def main():
    # db = DBHandler()
    # output = db.get_all_players()
    return render_template('fifa.html')

if __name__ == "__main__":
    app.run()

