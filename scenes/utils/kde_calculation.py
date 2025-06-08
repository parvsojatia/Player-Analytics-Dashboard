import numpy as np
from scipy.stats import gaussian_kde
from functools import lru_cache

from scenes.database.data_loader import fetch_player_events
from scenes.config.database_config import engine, EVENT_GROUPS

@lru_cache(maxsize=512)
def compute_kde_cached(player_id, match_ids, group):
    """
    Computes a KDE (Kernel Density Estimate) heatmap for a specific player and group of matches.

    Parameters:
        player_id (int): Unique ID of the player.
        match_ids (tuple[int]): Tuple of match IDs.
        group (str): Event group type (e.g., 'Attacking', 'Defending').

    Returns:
        tuple: xi (x-axis grid), yi (y-axis grid), z (density values), 
               x (raw y-coordinates), y (raw x-coordinates), 
               event types, and shot outcomes (if available).
               Returns None if no data is found.
    """
    # Ensure event group is valid
    group = group if group in EVENT_GROUPS else 'Attacking'

    # Load filtered event data
    df = fetch_player_events(
        player_id=player_id,
        engine=engine,
        group=group,
        match_ids=match_ids
    )

    if df.empty:
        return None

    # Extract location data
    x = df['location_y'].values  # Pitch width
    y = df['location_x'].values  # Pitch length

    # Generate KDE
    kde = gaussian_kde([x, y])

    # Define heatmap grid
    xi = np.linspace(0, 80, 160)   # Width grid
    yi = np.linspace(0, 120, 240)  # Length grid
    xi_grid, yi_grid = np.meshgrid(xi, yi)

    # Compute density values over the grid
    z = kde(np.vstack([xi_grid.ravel(), yi_grid.ravel()])).reshape(xi_grid.shape)

    # Remove low-density noise
    z[z < z.max() * 0.08] = np.nan

    return xi, yi, z, x, y, df['type'].values, df['shot_outcome'].fillna("").values


def compute_kde(player_id, match_ids=None, group='Attacking'):
    """
    Interface function to compute KDE with caching and default handling.

    Parameters:
        player_id (int): Player ID.
        match_ids (list[int] | None): List of match IDs (optional).
        group (str): Event group (default = 'Attacking').

    Returns:
        Output of `compute_kde_cached`.
    """
    match_ids = tuple(match_ids) if match_ids else None
    return compute_kde_cached(player_id, match_ids, group)
