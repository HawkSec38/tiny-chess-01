# tiny-chess-01: Chess engine in 4KB Python for make.fun bounty
# Built by AI agent for @goodluck-oyebisi
# Strategy: Capture highest value piece, with tiebreaks for promotions and piece value

import json
import os
import sys
import urllib.error
import urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

# Piece values: pawn=1, knight/bishop=3, rook=5, queen=9, king=100
VALUE = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}


def post(path, body):
    """POST JSON to env and return response."""
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")


def board_of(fen):
    """Parse FEN into {square: piece} dict."""
    board = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        file = 0
        for c in row:
            if c.isdigit():
                file += int(c)
            else:
                board["abcdefgh"[file] + str(8 - i)] = c
                file += 1
    return board


def choose(fen, legal):
    """Select best move: highest value capture, then promotion, then cheapest piece."""
    board = board_of(fen)
    best_move = legal[0]
    best_score = -1
    
    for move in legal:
        # Get moving piece and captured piece
        mover = board[move[:2]].lower()
        victim = board.get(move[2:4])
        
        # Handle en passant
        if victim is None and mover == "p" and move[0] != move[2]:
            victim = "p"
        
        # Calculate score: captured value - moving piece value (prefer trading up)
        captured_value = VALUE[victim.lower()] if victim else 0
        promotion_value = VALUE[move[4]] if len(move) == 5 else 0
        score = captured_value * 10 + promotion_value - VALUE[mover]
        
        if score > best_score or (score == best_score and move < best_move):
            best_move = move
            best_score = score
    
    return best_move


# Main game loop
while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        move = choose(g["fen"], g["legal_moves"])
        g = post("/move", {"game": g["game"], "move": move})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)

print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
