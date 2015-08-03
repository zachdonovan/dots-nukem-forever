from flask import request, abort, jsonify
from bootstrap import app, get_db
from models import Player, Score


def _assemble_response(player):
    return {
        'player': player.compute_puzzle_data(),
        'friends': player.compute_friends_data(),
        'high_scores': player.compute_high_scores_data()}


@app.route('/api/v1/player_data', methods=['POST'])
def player_data():
    if not request.json or 'player' not in request.json:
        print(request, request.json)
        abort(400)

    db = get_db()

    player_data = request.json['player']
    friends = player_data['friends']
    puzzle_data = player_data['puzzle_data']
    del player_data['friends']
    del player_data['puzzle_data']

    player = Player.get_or_create(player_data)
    db.session.query(Player).filter(
        Player.social_id == player.social_id).update(player_data)

    for friend_social_id in friends:
        friend = Player.get_or_create({"social_id": friend_social_id})
        player.add_friendship(friend)

    for index, puzzle_id in enumerate(puzzle_data['puzzles']):
        Score.maybe_update_score({
            'player_social_id': player.social_id,
            'puzzle_id': puzzle_id,
            'score': puzzle_data['scores'][index],
            'stars': puzzle_data['stars'][index]})

    db.session.commit()

    return jsonify(
        _assemble_response(player))
