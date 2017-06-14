from flask import Flask, render_template, jsonify

import json

app = Flask(__name__)


@app.route("/<fixture>")
def main(fixture):
    return render_template('fifa.html')


@app.route("/predicted_totw/<fixture>")
def predicted_totw(fixture):
    file = 'team_of_the_week{}.json'.format(fixture)
    with open(file) as json_data:
        return jsonify(json.load(json_data))


if __name__ == "__main__":
    app.run(debug=True)

