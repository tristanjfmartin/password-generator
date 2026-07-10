from flask import Flask, render_template, request, jsonify
from password_gen import generate_password

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    length = data.get("length", 12)

    if not isinstance(length, int) or isinstance(length, bool) or not (8 <= length <= 64):
        return jsonify({"error": "Length must be an integer between 8 and 64"}), 400

    use_upper = bool(data.get("use_upper", True))
    use_digits = bool(data.get("use_digits", True))
    use_symbols = bool(data.get("use_symbols", True))

    password = generate_password(length, use_upper, use_digits, use_symbols)
    return jsonify({"password": password})


if __name__ == "__main__":
    app.run(debug=True)
