from flask import *
import sqlite3
import uuid

app = Flask("restraunt")


@app.route('/api/signup', methods=['POST'])
def signup():
    conn = sqlite3.connect("restraunt.db")
    cur = conn.cursor()

    body = request.get_json()
    name = body["name"]
    password = body["password"]
    role = body["role"]
    id = str(uuid.uuid4())

    cur.execute(
        "INSERT INTO users VALUES(?,?,?,?)",
        [id, name, password, role]
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "User Created Successfully"
    }), 200


@app.route('/api/login', methods=['POST'])
def login():
    conn = sqlite3.connect("restraunt.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    body = request.get_json()
    name = body['name']
    password = body['password']

    cur.execute("SELECT * FROM users WHERE name = ?", [name])
    user = cur.fetchone()

    if not user:
        conn.close()
        return jsonify({"status": "user does not exist"}), 404

    if user["password"] != password:
        conn.close()
        return jsonify({"status": "wrong password"}), 401

    token = str(uuid.uuid4())

    cur.execute(
        "INSERT INTO sessions VALUES(?,?)",
        (token, user["id"])
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "login success",
        "token": token
    }), 200


@app.route('/api/profile', methods=["GET"])
def get_profile():
    conn = sqlite3.connect("restraunt.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    token = request.headers.get("Authorization")

    if not token:
        conn.close()
        return jsonify({"status": "unauthorised attempt"}), 403

    cur.execute("SELECT * FROM sessions WHERE token = ?", [token])
    ssn = cur.fetchone()

    if not ssn:
        conn.close()
        return jsonify({"status": "invalid session"}), 401

    cur.execute("SELECT * FROM users WHERE id = ?", [ssn["userid"]])
    user = cur.fetchone()

    conn.close()

    return jsonify({
        "status": "user is logged in",
        "name" : user["name"],
        "role" : user["role"]
    }), 200


@app.route('/')
def home():
    return render_template('index.html')


app.run(port=5000)

