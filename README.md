# CN Project Phase 1: Private Network Service Platform

## 1. Project Overview
This project demonstrates a fully local, cloud-independent network architecture simulating a real-world request lifecycle. It features a custom private DNS server, a TLS-terminated Nginx load balancer, and dual Python/Flask backend servers. This document serves as a complete setup guide, architectural overview, and troubleshooting manual for Phase 1.

## 2. Architecture & Topology
**Request Flow:** Client -> DNS Query (10.128.185.254) -> HTTPS Request (10.128.185.50) -> Backend A or B

| Component / Role | Node & Configuration Details | IP / Address Assignment |
| --- | --- | --- |
| Edge Proxy / Load Balancer | Nginx Reverse Proxy (Member 1) | `10.128.185.50` |
| Private DNS Server | dnsmasq Server (Member 2 / Samarth) | `10.128.185.254` |
| Backend Service A | Python / Flask App (Member 1 / Tattva) | `10.128.185.50` |
| Backend Service B | Python / Flask App (Member 3 / Pratham) | `10.128.185.228` |
| Network Subnet | Private LAN via Mobile Hotspot | `10.128.185.0/24` |

## 3. Setup Instructions & Commands

### A. Local LAN & Client Configuration
1. Connect all Macs to the same mobile hotspot.
2. Enforce DNS Routing on Client Macs:
   - Set macOS IPv6 to "Link-local only" to prevent hotspot overrides.
   - Clear DNS settings and add `10.128.185.254`.
   - Disable browser "Secure DNS" (DNS over HTTPS).
3. Fallback: If the hotspot aggressively blocks DNS, edit `/etc/hosts`:
   ```bash
   sudo nano /etc/hosts # Add: 10.128.185.50 app.team1.test
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   ```

### B. Backend Services (Python/Flask)
1. Install Flask (bypassing macOS PEP 668 limits if necessary):
   ```bash
   python3 -m pip install flask --break-system-packages
   ```
2. Start the servers on ports 3001 and 3002:
   ```bash
   python3 Backend_A/backend_a.py  # On port 3001
   python3 Backend_B/backend_b.py  # On port 3002
   ```
3. Verify locally:
   ```bash
   curl -i localhost:3001/api/status
   curl -i localhost:3002/api/status
   ```

### C. DNS Server Configuration (dnsmasq)
1. Disable macOS Firewall temporarily.
2. Restart the dnsmasq service to bind to the active Wi-Fi interface:
   ```bash
   sudo brew services restart dnsmasq
   ```
3. Verify DNS resolution locally:
   ```bash
   dig @127.0.0.1 app.team1.test
   ```

## 4. Phase 1 Tasks Completed
- **Task A (Private LAN):** Established the local network over a mobile hotspot. Verified cross-machine reachability using ping and documented IPv4 configurations.
- **Task B (Private DNS):** Deployed dnsmasq to route `app.team1.test` to the Edge Load Balancer (`10.128.185.50`).
- **Task C (Backend Services):** Created REST API endpoints using Python/Flask. Endpoints return JSON (`{"backend": "A", "status": "ok"}`) and dynamic `X-Backend` headers.
- **Task D (Reverse Proxy & Load Balancing):** Configured Nginx as a single entry point. Traffic is round-robin balanced between Backend A and Backend B.
- **Task E (HTTPS/TLS):** Enforced encrypted connections using TLSv1.2/TLSv1.3 by terminating local certificates at the Nginx edge.
- **Task F (HTTP Caching):** Updated the Python backends to inject `Cache-Control: max-age=60` and `ETag` headers. Validated HTTP 304 Not Modified caching behavior.
- **Task G (Protocol Flow Capture):** Leveraged Wireshark packet analysis for full network traffic verification.

## 5. Wireshark Capture Guide & Filters
To validate the network layers (Task G), use the following Wireshark methodology on the Load Balancer (Member 1):
1. **Start Capture:** Select the active Wi-Fi interface (e.g., `en0`).
2. **Filter Client Traffic:** Apply the display filter `ip.addr == 10.128.185.228` (Member 3's IP) to isolate the request flow.
3. **Key Packet Verification:**
   - **DNS (Port 53):** Look for the query to `app.team1.test` and the A Record response.
   - **TCP Handshake:** Locate the SYN, SYN-ACK, ACK packets before data exchange.
   - **TLS Handshake:** Verify ClientHello, ServerHello, and ChangeCipherSpec packets. Ensure application data is encrypted.
   - **HTTP Headers:** Check the plaintext HTTP forwarding from Nginx to Backend B on port 3002. Verify the presence of `Cache-Control: max-age=60`, `ETag`, and `X-Backend` headers.

## 6. Bugs, Errors, and Troubleshooting

### Issue 1: Flask Installation "Externally-Managed-Environment" Error
- **Bug:** macOS PEP 668 blocked `pip install flask`.
- **Resolution:** Bypassed using `--break-system-packages` flag.

### Issue 2: Mobile Hotspot IPv6 DNS Override
- **Bug:** Mobile hotspot forced an IPv6 DNS server (`2402:8100...`), causing NXDOMAIN errors on `app.team1.test`.
- **Resolution:** Disabled "Secure DNS" in browsers, disabled iCloud Private Relay, and hardcoded `/etc/hosts` to ensure 100% reliable routing.

### Issue 3: DNS Server (dnsmasq) Connection Timeout
- **Bug:** Queries to `10.128.185.254` timed out.
- **Resolution:** Disabled macOS Firewall blocking port 53 and ran `sudo brew services restart dnsmasq`.

### Issue 4: Browser "No Internet" Restriction
- **Bug:** Without cellular data, browsers blocked navigation to local custom domains.
- **Resolution:** Used terminal `curl -ik` commands to bypass browser-level internet checks and validate local LAN functionality.
