# simulator.py
"""
simulator.py - RF10
Genera datos de jugadas de fútbol americano ficticias para pruebas y demostraciones.
Uso random.choices() con ponderaciones para crear libros de jugadas con mucho juego terrestre o mucho juego aéreo.

"""

import json
import csv
import random
import uuid
from datetime import datetime

from exceptions import ValidationError


# Grupos de datos para elegir aleatoriamente

OFFENSE_FORMATIONS = [
    "SHOTGUN", "I_FORMATION", "SINGLEBACK",
    "GUN_TRIPS", "PISTOL", "WILDCAT", "EMPTY_SET"
]

PLAY_TYPES = ["run", "pass", "special"]

DOWN_DISTANCES = [
    "1st&10", "2nd&long", "2nd&short",
    "3rd&long", "3rd&short", "4th&1"
]

HASH_POSITIONS = ["left", "middle", "right"]

TAGS_POOL = [
    "red_zone", "short_yardage", "blitz_beater", "goal_line",
    "two_minute", "power_run", "play_action", "screen_game",
    "trick_play", "motion"
]

RUN_NAMES = [
    "HB Dive Left", "HB Dive Right", "Power Right", "Power Left",
    "Counter Left", "QB Sneak", "Sweep Right", "Toss Left", "Draw Play"
]

PASS_NAMES = [
    "Slant Route", "Go Route", "Curl Route", "Crossing Route",
    "Screen Pass", "Comeback Route", "Post Route", "PA Bootleg",
    "Four Verticals", "Smash Concept"
]

SPECIAL_NAMES = [
    "Field Goal", "Punt", "Kickoff", "Onside Kick", "Fake Punt"
]


# Core functions 

def generate_play(play_type=None, formation=None):
    """Generate one random play with realistic football data.

    Args:
        play_type: force a specific type ("run", "pass", "special"). Random if None.
        formation: force a specific formation string. Random if None.

    Returns:
        dict with all the play data

    Raises:
        ValidationError: if play_type is not valid
    """
    if play_type is None:
        play_type = random.choice(PLAY_TYPES)

    if play_type not in PLAY_TYPES:
        raise ValidationError(
            f"play_type must be one of {PLAY_TYPES}, got '{play_type}'"
        )

    # Pick a name and realistic yardage based on play type
    if play_type == "run":
        name = random.choice(RUN_NAMES)
        # runs average around 4-5 yards, gauss gives us a bell curve
        yards = round(random.gauss(4.5, 2.5), 1)
    elif play_type == "pass":
        name = random.choice(PASS_NAMES)
        # passes go further but more variance
        yards = round(random.gauss(8.0, 5.5), 1)
    else:
        name = random.choice(SPECIAL_NAMES)
        yards = round(random.uniform(0.0, 50.0), 1)


# Limitaremos las yardas para evitar números negativos desmesurados.
# (Los sacks ocurren, pero -30 yardas es demasiado)

    yards = max(yards, -5.0)

    if formation is None:
        formation = random.choice(OFFENSE_FORMATIONS)

    return {
        "id": f"play_{uuid.uuid4().hex[:8]}",
        "name": name,
        "play_type": play_type,
        "formation": formation,
        "description": f"{name} out of {formation} formation",
        "yards": yards,
        "success_rate": round(random.uniform(0.30, 0.85), 2),
        "down_distance": random.choice(DOWN_DISTANCES),
        "hash_position": random.choice(HASH_POSITIONS),
        "tags": random.sample(TAGS_POOL, k=random.randint(1, 3)),
        "created_at": datetime.now().isoformat(),
    }


def generate_plays(n, play_type=None, formation=None):
    """Generate a list of n random plays.

    Args:
        n: how many plays to generate (must be >= 0)
        play_type: optional, filter all plays to this type
        formation: optional, filter all plays to this formation

    Returns:
        list of play dicts (empty list if n=0)

    Raises:
        ValidationError: if n is negative
    """
    if n < 0:
        raise ValidationError(f"n must be 0 or positive, got {n}")

    return [generate_play(play_type, formation) for _ in range(n)]


def generate_playbook(name, n_plays=20, offense_type="balanced"):
    """Generate a full playbook with random plays inside.

    Args:
        name: name of the playbook (can't be empty)
        n_plays: number of plays to include (default 20)
        offense_type: "balanced", "run_heavy", or "pass_heavy"

    Returns:
        dict with playbook data including the plays list

    Raises:
        ValidationError: if name is empty or n_plays is negative
    """
    if not name or not name.strip():
        raise ValidationError("Playbook name can't be empty")

    if n_plays < 0:
        raise ValidationError(f"n_plays must be 0 or positive, got {n_plays}")

    # Weights control how often each play type appears
    # [run_weight, pass_weight, special_weight]
    weights_map = {
        "run_heavy":  [0.60, 0.30, 0.10],
        "pass_heavy": [0.20, 0.70, 0.10],
        "balanced":   [0.40, 0.50, 0.10],
    }
    weights = weights_map.get(offense_type, weights_map["balanced"])

    plays = []
    for _ in range(n_plays):
        # random.choices returns a list so we grab index 0
        p_type = random.choices(PLAY_TYPES, weights=weights, k=1)[0]
        plays.append(generate_play(p_type))

    return {
        "id": f"pb_{uuid.uuid4().hex[:8]}",
        "name": name,
        "offense_type": offense_type,
        "plays": plays,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }



def save_to_json(data, filepath):
    """Save a dict or list to a JSON file.

    Args:
        data: the thing to save
        filepath: path to the output file (string)
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[simulator] Saved JSON to {filepath}")


def save_plays_to_csv(plays, filepath):
    """Save a list of play dicts to a CSV file.

    Tags are stored as a pipe-separated string (e.g. "red_zone|power_run")
    because CSV doesn't support lists natively.

    Args:
        plays: list of play dicts
        filepath: path to the output CSV file
    """
    if not plays:
        print("[simulator] No plays to save, skipping CSV export.")
        return

    # Build fieldnames from the first play's keys
    fieldnames = [k for k in plays[0].keys() if k != "tags"]
    fieldnames.append("tags")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for play in plays:
            row = {k: v for k, v in play.items() if k != "tags"}
            row["tags"] = "|".join(play.get("tags", []))
            writer.writerow(row)

    print(f"[simulator] Saved {len(plays)} plays to {filepath}")
