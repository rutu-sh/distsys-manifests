# BACKEND SERVER FOR HOSTING THE DINO GAME
import os
import json
import logging
from flask import Flask, send_from_directory, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask("dino-game")

SCORES_FILE_PATH = os.getenv("SCORES_FILE_PATH", "scores.json")

# Health check to verify the state of the server
@app.get("/health-check")
def health_check():
    logging.info("health called")
    return jsonify({"status": "ok"})


# Serve the dino game
@app.get("/")
def get_dino_game_html():
    logging.info("serving dino.html")
    return send_from_directory("game", "trex.html")


# Display user scores
@app.get("/user")
def user_scores_html():
    logging.info("serving user.html")
    return send_from_directory("game", "user.html")


 # Save the score for a user
@app.post("/score/<name>")
def save_score(name):
    logging.info(f"save score called for user {name}")

    # read the request
    data = request.get_json()
    score = int(data.get("score"))

    # Save the score to a file or database
    logging.info(f"Score submitted: {name} - {score}")
    if os.path.exists(SCORES_FILE_PATH):
        scores_file = open(SCORES_FILE_PATH, "r")
        scores = json.load(scores_file)
        scores_file.close()
    else:
        scores = {}

    # Update scores for the name
    if name:
        if name not in scores:
            scores[name] = []
        scores[name].append(score)
        
        # save only top 5
        scores[name] = sorted(scores[name], reverse=True)[:5]

    # write the scores to the file 
    with open(SCORES_FILE_PATH, "w") as f:
        json.dump(scores, f)

    logging.info(f"score saved for user {name}")
    return jsonify({"status": "success"})


 # Get scores of a user
@app.get("/score/<name>")
def user_scores(name):
    logging.info(f"fetching all scores for user {name}")
    if os.path.exists(SCORES_FILE_PATH):
        scores_file = open(SCORES_FILE_PATH, "r")
        scores = json.load(scores_file)
        scores_file.close()
    else:
        scores = {}
    user_scores = scores.get(name, []) if name else []
    logging.info(f"fetched all scores for user {name}!")
    return jsonify({"name": name, "scores": user_scores})


 # Endpoint to fetch scores as JSON
@app.get("/scores")
def get_scores():
    logging.info("fetching scores")
    if os.path.exists(SCORES_FILE_PATH):
        scores_file = open(SCORES_FILE_PATH, "r")
        scores = json.load(scores_file)
        scores_file.close()
    else:
        scores = {}
    # Flatten to [{name, score}] for frontend compatibility
    leaderboard = []
    for name, score_list in scores.items():
        for score in score_list:
            leaderboard.append({"name": name, "score": score})
    # Sort by score descending
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    logging.info("fetched scores!")
    return jsonify(leaderboard)
