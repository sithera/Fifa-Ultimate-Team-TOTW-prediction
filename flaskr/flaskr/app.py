from flask import Flask, request, render_template, jsonify

import json

app = Flask(__name__)


@app.route("/")
def main():
    # db = DBHandler()
    # output = db.get_all_players()
    return render_template('fifa.html')

@app.route("/predicted_totw")
def predicted_totw():
    with open('mock_team_of_the_week.json') as json_data:
        return jsonify(json.load(json_data))


if __name__ == "__main__":
    app.run(debug=True)

