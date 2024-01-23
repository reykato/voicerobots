from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response
from motors import Motors

app = Flask(__name__)


@app.route('/control')
def control():
    m = Motors(20, 21, 16, 12)
    return render_template('index.html')


@app.route('/control/data', methods=["POST"])
def control_data():
    req = request.get_json()

    print(f"x is {req['x']} and y is {req['y']}")

    m.forward_for_ms(100)
    
    return "Thx brah"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')