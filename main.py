import json

from flask import Flask, jsonify, request

from json_schema import generate_json_schema, generate_json_schema_v2

app = Flask(__name__)


@app.route("/v1/generate_schema", methods=["POST"])
def generate_schema_v1():
    try:
        json_data = request.get_json()
        if json_data:
            json_schema = generate_json_schema(json_data)
            return jsonify(json_schema), 200
        else:
            return "Invalid JSON data", 400
    except json.JSONDecodeError as e:
        return "Invalid JSON format: " + str(e), 400


@app.route("/v2/generate_schema", methods=["POST"])
def generate_schema_v2():
    try:
        json_data = request.get_json()
        if json_data:
            json_schema = generate_json_schema_v2(json_data)
            return jsonify(json_schema), 200
        else:
            return "Invalid JSON data", 400
    except json.JSONDecodeError as e:
        return "Invalid JSON format: " + str(e), 400


if __name__ == "__main__":
    app.run(debug=True)
