# tests/test_simulator.py
"""
Tests for simulator.py (RF10)
Covers: T20, T21 from the test plan + extra cases
"""

import pytest
from simulator import (
    generate_play,
    generate_plays,
    generate_playbook,
    save_to_json,
    save_plays_to_csv,
    PLAY_TYPES,
    OFFENSE_FORMATIONS,
)
from exceptions import ValidationError


# generate_play() tests 

class TestGeneratePlay:
    """Tests for the single play generator."""

    def test_returns_all_required_keys(self):
        """A generated play must have all the fields we need."""
        play = generate_play()
        required_keys = [
            "id", "name", "play_type", "formation",
            "description", "yards", "success_rate",
            "down_distance", "hash_position", "tags", "created_at"
        ]
        for key in required_keys:
            assert key in play, f"Missing key: {key}"

    def test_play_type_is_valid(self):
        """play_type should always be one of our valid types."""
        play = generate_play()
        assert play["play_type"] in PLAY_TYPES

    def test_formation_is_valid(self):
        """formation should always be one of our valid formations."""
        play = generate_play()
        assert play["formation"] in OFFENSE_FORMATIONS

    def test_forced_play_type(self):
        """When we force a play_type it should respect it."""
        play = generate_play(play_type="run")
        assert play["play_type"] == "run"

    def test_forced_formation(self):
        """When we force a formation it should respect it."""
        play = generate_play(formation="SHOTGUN")
        assert play["formation"] == "SHOTGUN"

    def test_yards_not_too_negative(self):
        """Yards should never be below -5 (we clamp them)."""
        # Run this a bunch of times to catch edge cases
        for _ in range(50):
            play = generate_play()
            assert play["yards"] >= -5.0, f"Yards too low: {play['yards']}"

    def test_success_rate_in_valid_range(self):
        """Success rate should always be between 0 and 1."""
        for _ in range(20):
            play = generate_play()
            assert 0.0 <= play["success_rate"] <= 1.0

    def test_invalid_play_type_raises_error(self):
        """Passing a made-up play type should raise ValidationError."""
        with pytest.raises(ValidationError):
            generate_play(play_type="kickflip")

    def test_tags_is_a_list(self):
        """Tags should be a list, not a string or anything else."""
        play = generate_play()
        assert isinstance(play["tags"], list)
        assert len(play["tags"]) >= 1

    def test_id_is_unique(self):
        """Two plays generated back to back should have different IDs."""
        play1 = generate_play()
        play2 = generate_play()
        assert play1["id"] != play2["id"]


# generate_plays() tests

class TestGeneratePlays:
    """Tests for the bulk play generator."""

    def test_generates_correct_number(self):
        """T20 - generate_plays(100) should return exactly 100 plays."""
        plays = generate_plays(100)
        assert len(plays) == 100

    def test_empty_list_when_n_is_zero(self):
        """T21 - generate_plays(0) should return an empty list."""
        plays = generate_plays(0)
        assert plays == []

    def test_negative_n_raises_error(self):
        """Negative n should raise ValidationError, not crash."""
        with pytest.raises(ValidationError):
            generate_plays(-5)

    def test_all_plays_have_correct_type_when_forced(self):
        """When we force play_type all plays should have that type."""
        plays = generate_plays(20, play_type="pass")
        for play in plays:
            assert play["play_type"] == "pass"

    def test_returns_list_of_dicts(self):
        """Each element should be a dict (a play)."""
        plays = generate_plays(5)
        assert isinstance(plays, list)
        for play in plays:
            assert isinstance(play, dict)


# generate_playbook() tests 

class TestGeneratePlaybook:
    """Tests for the playbook generator."""

    def test_basic_playbook_structure(self):
        """A generated playbook should have all required fields."""
        pb = generate_playbook("Test Offense")
        assert "id" in pb
        assert "name" in pb
        assert "plays" in pb
        assert "offense_type" in pb

    def test_correct_number_of_plays(self):
        """n_plays should control how many plays are inside."""
        pb = generate_playbook("Quick Offense", n_plays=10)
        assert len(pb["plays"]) == 10

    def test_empty_name_raises_error(self):
        """Empty playbook name should raise ValidationError."""
        with pytest.raises(ValidationError):
            generate_playbook("")

    def test_whitespace_name_raises_error(self):
        """Name with only spaces should also raise ValidationError."""
        with pytest.raises(ValidationError):
            generate_playbook("   ")

    def test_negative_n_plays_raises_error(self):
        """Negative n_plays should raise ValidationError."""
        with pytest.raises(ValidationError):
            generate_playbook("Bad", n_plays=-1)

    def test_run_heavy_has_more_runs(self):
        """run_heavy offense should have more run plays than pass plays."""
        pb = generate_playbook("Run Team", n_plays=100, offense_type="run_heavy")
        runs = sum(1 for p in pb["plays"] if p["play_type"] == "run")
        passes = sum(1 for p in pb["plays"] if p["play_type"] == "pass")
        # With weight 0.6 vs 0.3, runs should be clearly more
        assert runs > passes

    def test_pass_heavy_has_more_passes(self):
        """pass_heavy offense should have more pass plays than run plays."""
        pb = generate_playbook("Air Raid", n_plays=100, offense_type="pass_heavy")
        runs = sum(1 for p in pb["plays"] if p["play_type"] == "run")
        passes = sum(1 for p in pb["plays"] if p["play_type"] == "pass")
        assert passes > runs

    def test_zero_plays_is_valid(self):
        """A playbook with 0 plays is weird but should still work."""
        pb = generate_playbook("Empty", n_plays=0)
        assert pb["plays"] == []


# save functions tests

class TestSaveFunctions:
    """Tests for the JSON and CSV save functions."""

    def test_save_to_json(self, tmp_path):
        """save_to_json should create a valid JSON file."""
        import json
        data = {"test": "data", "number": 42}
        filepath = tmp_path / "test.json"
        save_to_json(data, str(filepath))

        assert filepath.exists()
        loaded = json.loads(filepath.read_text())
        assert loaded["test"] == "data"
        assert loaded["number"] == 42

    def test_save_plays_to_csv(self, tmp_path):
        """save_plays_to_csv should create a CSV with the right number of rows."""
        import csv
        plays = generate_plays(5)
        filepath = tmp_path / "test.csv"
        save_plays_to_csv(plays, str(filepath))

        assert filepath.exists()
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 5

    def test_save_empty_plays_to_csv_does_not_crash(self, tmp_path):
        """Saving an empty list should not crash, just print a message."""
        filepath = tmp_path / "empty.csv"
        # Should not raise any exception
        save_plays_to_csv([], str(filepath))
        # File shouldn't be created either
        assert not filepath.exists()

    def test_csv_tags_are_pipe_separated(self, tmp_path):
        """Tags in CSV should be joined with | not saved as a Python list string."""
        import csv
        plays = generate_plays(1)
        filepath = tmp_path / "tags_test.csv"
        save_plays_to_csv(plays, str(filepath))

        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row = next(reader)

        # Should be "tag1|tag2" not "['tag1', 'tag2']"
        assert "[" not in row["tags"]
        assert "]" not in row["tags"]