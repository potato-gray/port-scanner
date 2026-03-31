# Port Scanner
A multi-threaded port scanner written in Python, with banner grabbing, CIDR support and high-risk port marking.

## Project Evolution (Day 1 to Day 10)
- **Day 01**: Basic input and try-except error handling
- **Day 02**: Simple single-threaded port scanning
- **Day 03**: Socket-based port scanning
- **Day 04**: Dual-port scanning optimization
- **Day 05**: Basic port scanning framework
- **Day 06**: Service identification for common ports
- **Day 07**: Extended service identification
- **Day 08**: Banner grabbing for service version detection
- **Day 09**: Multi-threaded fast scanning implementation
- **Day 10**: CIDR network segment support and final optimization

## Features
- Multi-threaded fast scanning
- Support CIDR network segment (e.g. 192.168.1.0/24) and IP range
- Banner grabbing for service version identification
- High-risk port warning
- Auto-save scan results to file

## Usage
1. Run the script: `python day10CIDR.py`
2. Input target IP/CIDR/IP range
3. Input port range (e.g. 1-1000)
4. Input max thread number (recommended 50-100)

## Author
potato-gray
