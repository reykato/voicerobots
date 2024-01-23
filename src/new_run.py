from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response

app = Flask(__name__)


@app.route('/control')
def control():
    return render_template('index.html')


@app.route('/control/data', methods=["POST"])
def control_data():
    req = request.get_json()

    print(f"x is {req['x']} and y is {req['y']}")
    return "Thx brah"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')