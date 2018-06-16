import os
from flask import Flask
from flask import json, jsonify
from flask import render_template
from flask import send_from_directory
from flask import request
from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
from flask_cors import CORS

app = Flask(__name__, template_folder='dist', static_folder='dist/static')
CORS(app)

pc = PersonalCapital()

@app.route('/')
def index():
    print(request.remote_addr)

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email, password = request.get_json()['email'], request.get_json()['password']

    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        return jsonify({
            'email': email
        })

@app.route('/twoauth', methods=['POST'])
def twoauth():
    pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, request.get_json()['smsCode'])
    pc.authenticate_password(request.get_json()['password'])

    accounts_response = pc.fetch('/newaccount/getAccounts')
    accounts = accounts_response.json()['spData']
    return jsonify({
        'networth': accounts['networth'],
        'accounts': accounts['accounts']
    })


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'dist/static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<path:invalid>')
def page_not_found(*args, **kwargs):

    response = app.response_class(
        response=json.dumps(
            {
                'error': 'not found'
            }
        ),
        status=404,
        mimetype='application/json'
    )

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
