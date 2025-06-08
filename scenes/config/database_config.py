import os
from sqlalchemy import create_engine

# Database configuration
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

# Create engine with SQLAlchemy 2.x compatibility
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}",
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False  # Set to True for debugging SQL queries
)

# database_config.txt
EVENT_GROUPS = {
    "Attacking": ["Pass", "Shot", "Dribble", "Carry", "Cross"],
    "Defensive": ["Duel", "Interception", "Block", "Clearance"]
}
COLOR_MAPPING = {
    "Attacking": "#e41a1c",
    "Defensive": "#377eb8"
}

