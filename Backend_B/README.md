# Backend B (Member 3)

Backend B microservice built using Flask for the Computer Networks project.

## 1. Setup & Installation
Ensure Python 3 is installed. Install Flask:
```bash
pip install -r requirements.txt
```
*(or `pip install flask`)*

## 2. Run the Server
Run the backend service on Member 3's machine (binds to `0.0.0.0:3002`):
```bash
python3 backend_b.py
```

## 3. Verify the Endpoint
From Member 1's machine (or anywhere on the LAN), test reachability across the LAN:
```bash
curl -i http://10.128.185.228:3002/api/status
```

### Expected Response
- **Headers:** `X-Backend: B`
- **Body:** `{"backend":"B","status":"ok"}`
