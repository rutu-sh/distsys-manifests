# BACKEND SERVER FOR HOSTING THE DINO GAME
import os
import json
import logging
from flask import Flask, send_from_directory, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask("dino-game")

SCORES_FILE_PATH = os.getenv("SCORES_FILE_PATT", "scores.json")

# Health check to verify the state of the server
@app.get("/health-check")
def health_check():
    logging.info("health called")
    return jsonify({"status": "ok"})


# Serve the main game HTML
@app.get("/")
def get_index_html():
    logging.info("serving index.html")
    return send_from_directory("game", "index.html")


# Serve user scores HTML page
@app.get("/user-scores.html")
def user_scores_html():
    logging.info("serving user_scores.html")
    return send_from_directory("game", "user_scores.html")


# Save the score
@app.post("/save-score")
def save_score():
    logging.info("save score called")

    # read the request
    data = request.get_json()
    name = data.get("name")
    score = int(data.get("score"))

    # Here you would save the score to a file or database
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
        scores[name] = sorted(scores[name], reverse=True)[:5] # save top 5 scores of this user

    # write the scores to the file 
    with open(SCORES_FILE_PATH, "w") as f:
        json.dump(scores, f)
    
    logging.info(f"score saved for user {name}")
 
    return jsonify({"status": "success"})


# API endpoint to get scores for a user
@app.get("/user-scores")
def user_scores():
    name = request.args.get("name")

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


# Endpoint to fetch all scores as JSON
@app.get("/scores")
def get_scores():

    logging.info("fetching all scores")

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

    logging.info("fetched all scores!")

    return jsonify(leaderboard)


if __name__ == "__main__":
    logging.info("starting app...")
    app.run(debug=False, port=8080)
