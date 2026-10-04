from flask import Flask, render_template, request, jsonify

from src.api import calculate as calculate_mortgage

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    response_data, status = calculate_mortgage(request.form)
    return jsonify(response_data), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
