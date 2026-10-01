from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend B is running"

@app.route('/api/status')
def status():
    # Return the expected JSON with the "B" identifier
    response = make_response(jsonify({"backend": "B", "status": "ok"}))
    # Add the expected custom header
    response.headers['X-Backend'] = 'B'
    return response

if __name__ == '__main__':
    # Binding to 0.0.0.0 is crucial so it is accessible across the LAN by the proxy
    app.run(host='0.0.0.0', port=3002)
