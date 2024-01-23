from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response
from motors import Motors

app = Flask(__name__)
m = Motors(20, 21, 16, 12)

@app.route('/control')
def control():
    return render_template('index.html')

def handle_data(x, y):
    if y > 0:
        m.forward_for_ms(200)
    else:
        m.backward_for_ms(200)

@app.route('/control/data', methods=["POST"])
def control_data():
    req = request.get_json()

    print(f"x is {req['x']} and y is {req['y']}")

    handle_data(req['x'], req['y'])
    
    return "Thx brah"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

