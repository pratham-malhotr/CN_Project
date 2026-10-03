import hashlib
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend A is running"

@app.route('/api/status')
def status():
    # 1. Define the payload
    payload = {"backend": "A", "status": "ok"}
    
    # 2. Generate ETag (a unique fingerprint of the payload)
    etag = hashlib.md5(str(payload).encode()).hexdigest()
    
    # 3. Check if the browser already has this exact version cached
    if request.headers.get("If-None-Match") == etag:
        return "", 304  # Return 304 Not Modified
        
    # 4. If not cached, build the full 200 OK response
    response = make_response(jsonify(payload))
    response.headers['X-Backend'] = 'A'
    response.headers['Cache-Control'] = 'max-age=60'
    response.headers['ETag'] = etag
    
    return response

if __name__ == '__main__':
    # Binding to 0.0.0.0 is crucial so it is accessible across the LAN by the proxy
    app.run(host='0.0.0.0', port=3001)
