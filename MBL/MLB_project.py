umpires = [
('hp_umpire_id', 'UHP'),
('[1b_umpire_id]', 'U1B'),
('[2b_umpire_id]', 'U2B'),
('[3b_umpire_id]', 'U3B'),
('lf_umpire_id', 'ULF'),
('rf_umpire_id', 'URF'),
]

# Insert data for pitchers and managers
"""
INSERT OR IGNORE INTO person_appearance
    (
    person_id,
    team_id,
    game_id,
    appearance_type_id
    )

	SELECT
		v_manager_id,
		v_name,
	    game_id,
	    "MM"
	FROM game_log
	WHERE v_manager_id IS NOT NULL

UNION

    SELECT
        h_manager_id,
        h_name,
        game_id,
        "MM"
    FROM game_log
    WHERE h_manager_id IS NOT NULL

UNION

    SELECT
        winning_pitcher_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        game_id,
        "AWP"
    FROM game_log
    WHERE winning_pitcher_id IS NOT NULL

UNION
	
	SELECT
        losing_pitcher_id,
        CASE
            WHEN h_score < v_score THEN h_name
            ELSE v_name
            END,
        game_id,
        "AWP"
    FROM game_log
    WHERE losing_pitcher_id IS NOT NULL

UNION

	SELECT
		saving_pitcher_id,
		CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        game_id,
        "ASP"
    FROM game_log
    WHERE saving_pitcher_id IS NOT NULL

UNION

	SELECT
		winning_rbi_batter_id, 
		CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        game_id,
        "AWB"
    FROM game_log
    WHERE winning_rbi_batter_id IS NOT NULL

UNION

	SELECT
		v_starting_pitcher_id,
		v_name,
		game_id,
		"PSP"
	FROM game_log
	WHERE v_starting_pitcher_id IS NOT NULL

UNION

	SELECT
		h_starting_pitcher_id,
		h_name,
		game_id,
		"PSP"
	FROM game_log
	WHERE h_starting_pitcher_id IS NOT NULL	
"""
