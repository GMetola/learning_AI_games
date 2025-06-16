from flask import Flask, render_template, request, jsonify
from src.api.game_api import GameAPI

app = Flask(__name__)
game_api = GameAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.json
    game_id = game_api.start_game(data)
    return jsonify({"game_id": game_id})

@app.route('/api/make_move', methods=['POST'])
def make_move():
    data = request.json
    result = game_api.make_move(data)
    return jsonify(result)

@app.route('/api/get_game_state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    state = game_api.get_game_state(game_id)
    return jsonify(state)

if __name__ == '__main__':
    app.run(debug=True)