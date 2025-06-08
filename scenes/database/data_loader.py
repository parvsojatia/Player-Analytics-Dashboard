import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy.engine.base import Engine
from typing import List, Dict, Optional

from scenes.config.database_config import EVENT_GROUPS

def load_players(engine: Engine) -> List[Dict]:
    """
    Load a list of players who have event data available in the database.

    Parameters:
        engine (Engine): SQLAlchemy database engine.

    Returns:
        List[Dict]: A list of dictionaries with 'label' and 'value' for dropdown components.
    """
    try:
        query = text("""
            SELECT DISTINCT p.player_id, p.name
            FROM players p
            JOIN events e ON p.player_id = e.player_id
            ORDER BY p.name
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        
        return [{"label": row.name, "value": row.player_id} for row in df.itertuples()]
    
    except Exception as e:
        print(f"[Error] Failed to load players: {str(e)}")
        return []


def load_player_matches(player_id: int, engine: Engine) -> List[Dict]:
    """
    Load all matches a player has played in, along with the opponent team name.

    Parameters:
        player_id (int): Unique ID of the player.
        engine (Engine): SQLAlchemy database engine.

    Returns:
        List[Dict]: List of match dropdown options with opponent names.
    """
    try:
        query = text("""
            SELECT DISTINCT
                m.match_id,
                CASE
                    WHEN e.team_id = t_home.team_id THEN t_away.team
                    ELSE t_home.team
                END AS opponent
            FROM events e
            JOIN matches m ON e.match_id = m.match_id
            JOIN teams t_home ON m.home_team = t_home.team
            JOIN teams t_away ON m.away_team = t_away.team
            WHERE e.player_id = :player_id
        """)
        
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={'player_id': player_id})
        
        return [{'label': f"vs {row.opponent}", 'value': row.match_id} for row in df.itertuples()]
    
    except Exception as e:
        print(f"[Error] Failed to load matches for player {player_id}: {str(e)}")
        return []


def fetch_player_events(
    player_id: int, 
    engine: Engine,
    group: str = "Attacking",
    match_ids: Optional[List[int]] = None
) -> pd.DataFrame:
    """
    Fetch filtered event data for a player by event group and matches.

    Parameters:
        player_id (int): Unique player ID.
        engine (Engine): SQLAlchemy database engine.
        group (str): Event group name (e.g., 'Attacking', 'Defending').
        match_ids (Optional[List[int]]): List of match IDs to filter by.

    Returns:
        pd.DataFrame: DataFrame containing relevant event data.
    """
    try:
        event_types = EVENT_GROUPS.get(group, ["Pass"])  # Default fallback
        
        base_query = """
            SELECT 
                type,
                location_x::FLOAT,
                location_y::FLOAT,
                shot_outcome
            FROM events
            WHERE player_id = :player_id
              AND type = ANY(:event_types)
              AND location_x BETWEEN 0 AND 120
              AND location_y BETWEEN 0 AND 80
        """

        params = {
            'player_id': player_id,
            'event_types': event_types
        }

        if match_ids:
            base_query += " AND match_id = ANY(:match_ids)"
            params['match_ids'] = list(match_ids)

        with engine.connect() as conn:
            df = pd.read_sql(text(base_query), conn, params=params)

        # Double-checking bounds to sanitize edge cases
        return df[
            df.location_x.between(0, 120) & 
            df.location_y.between(0, 80)
        ]

    except Exception as e:
        print(f"[Error] Failed to fetch events for player {player_id}: {str(e)}")
        return pd.DataFrame()
