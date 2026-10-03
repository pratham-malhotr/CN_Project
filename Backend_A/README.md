# Backend A (Member 1)

Backend A microservice built using Flask for the Computer Networks project.

## 1. Setup & Installation
Ensure Python 3 is installed. Install Flask:
```bash
pip install -r requirements.txt
```
*(or `pip install flask`)*

## 2. Run the Server
Run the backend service on Member 1's machine (binds to `0.0.0.0:3001`):
```bash
python3 backend_a.py
```

## 3. Verify the Endpoint
From any machine on the LAN, test reachability across the LAN:
```bash
curl -i http://10.128.185.50:3001/api/status
```

### Expected Response
- **Headers:** `X-Backend: A`, `Cache-Control: max-age=60`, `ETag: ...`
- **Body:** `{"backend":"A","status":"ok"}`
