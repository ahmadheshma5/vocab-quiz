from flask import Flask, jsonify, request, send_from_directory, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(ROOT, 'words.json')
USERS_FILE = os.path.join(ROOT, 'users.json')
BOARD_FILE = os.path.join(ROOT, 'leaderboard.json')

def read_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return default
    return default

def write_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

app = Flask(__name__, static_folder='..', static_url_path='')
app.secret_key = 'dev-secret-change-me'

@app.route('/api/words', methods=['GET','POST'])
def api_words():
    words = read_json(WORDS_FILE, [])
    if request.method == 'GET':
        return jsonify(words)
    # POST -> add word (requires login)
    if 'user' not in session:
        return jsonify({'ok':False,'msg':'Not authenticated'}), 401
    data = request.get_json() or {}
    e = data.get('english','').strip()
    a = data.get('arabic','').strip()
    if not e or not a:
        return jsonify({'ok':False,'msg':'english and arabic required'}), 400
    words.append({'english': e, 'arabic': a})
    write_json(WORDS_FILE, words)
    return jsonify({'ok':True})

@app.route('/api/register', methods=['POST'])
def api_register():
    users = read_json(USERS_FILE, {})
    data = request.get_json() or {}
    u = data.get('username','').strip()
    p = data.get('password','')
    if not u or not p:
        return jsonify({'ok':False,'msg':'username & password required'}), 400
    if u in users:
        return jsonify({'ok':False,'msg':'username exists'}), 400
    users[u] = {'hash': generate_password_hash(p)}
    write_json(USERS_FILE, users)
    return jsonify({'ok':True})

@app.route('/api/login', methods=['POST'])
def api_login():
    users = read_json(USERS_FILE, {})
    data = request.get_json() or {}
    u = data.get('username','').strip()
    p = data.get('password','')
    if not u or not p:
        return jsonify({'ok':False,'msg':'username & password required'}), 400
    if u not in users:
        return jsonify({'ok':False,'msg':'no such user'}), 400
    if not check_password_hash(users[u]['hash'], p):
        return jsonify({'ok':False,'msg':'wrong password'}), 400
    session['user'] = u
    return jsonify({'ok':True,'username':u})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)
    return jsonify({'ok':True})

@app.route('/api/current_user', methods=['GET'])
def api_current_user():
    return jsonify({'username': session.get('user')})

@app.route('/api/leaderboard', methods=['GET','POST','DELETE'])
def api_leaderboard():
    board = read_json(BOARD_FILE, [])
    if request.method == 'GET':
        # return top scores
        board.sort(key=lambda r: (-r.get('score',0), r.get('when',0)))
        return jsonify(board)
    if request.method == 'POST':
        data = request.get_json() or {}
        u = session.get('user') or data.get('username')
        s = int(data.get('score', 0))
        if not u:
            return jsonify({'ok':False,'msg':'no user'}), 400
        board.append({'username': u, 'score': s, 'when': int(data.get('when', 0) or 0)})
        board.sort(key=lambda r: (-r.get('score',0), r.get('when',0)))
        write_json(BOARD_FILE, board[:100])
        return jsonify({'ok':True})
    if request.method == 'DELETE':
        write_json(BOARD_FILE, [])
        return jsonify({'ok':True})

@app.route('/')
def index():
    return send_from_directory('..', 'quiz.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
