import sqlite3

# Database file path
DB_FILE = "reporter/data/kranos_data.db"

# --- DDL Statements ---

CREATE_MEMBERS_TABLE = """
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    join_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Active', 'Inactive'))
);
"""

CREATE_GROUP_PLANS_TABLE = """
CREATE TABLE IF NOT EXISTS group_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    price REAL NOT NULL
);
"""

CREATE_GROUP_MEMBERSHIPS_TABLE = """
CREATE TABLE IF NOT EXISTS group_class_memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    price REAL NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (plan_id) REFERENCES group_plans(id)
);
"""

CREATE_PT_MEMBERSHIPS_TABLE = """
CREATE TABLE IF NOT EXISTS pt_memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    sessions_total INTEGER NOT NULL,
    sessions_used INTEGER DEFAULT 0,
    price REAL NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(id)
);
"""

ALL_TABLES = [
    CREATE_MEMBERS_TABLE,
    CREATE_GROUP_PLANS_TABLE,
    CREATE_GROUP_MEMBERSHIPS_TABLE,
    CREATE_PT_MEMBERSHIPS_TABLE,
]


def initialize_database():
    """Create all tables in the database if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for table_query in ALL_TABLES:
        cursor.execute(table_query)
    conn.commit()
    conn.close()
