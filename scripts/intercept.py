from flask import Flask, request
import requests
import sys
app = Flask(__name__)

# Route for the home page
@app.route('/',methods=["POST"])
def index():
    if request.method == 'POST':
        data = request.json
        if data:
            if data['method'] == "eth_accounts":
                return {'error':"This is blocked for security purposes, you should already have the wallet provided when the contract was deployed"}
            elif data['method'][:4] == "evm_":
                return {'error':"These features are disabled!"}
            response = requests.post(f"http://127.0.0.1:{int(sys.argv[1])+10001}", json=data)
            ganache_data = response.json()
            return ganache_data



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int(sys.argv[1]))
