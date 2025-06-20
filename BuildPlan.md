# Build Plan: `kranos-reporter` Application

**Objective:** To construct a fully functional Streamlit application for managing memberships and generating financial reports for Kranos MMA.

This document provides all necessary instructions, specifications, and source code. Execute the following phases in sequence without deviation.

---

## **Phase 0: Project Scaffolding**

**Action:** Create the following directory and file structure. All files should be empty initially.

```
kranos-reporter/
├── .gitignore
├── README.md
├── app_specs.md
├── reporter/
│   ├── __init__.py
│   ├── app_api.py
│   ├── data/
│   │   └── (This directory will hold the database)
│   ├── database.py
│   ├── database_manager.py
│   ├── main.py
│   ├── migrate_historical_data.py
│   ├── models.py
│   ├── streamlit_ui/
│   │   ├── __init__.py
│   │   └── app.py
│   └── tests/
│       ├── __init__.py
│       └── (Test files will be created later)
├── requirements.txt
└── pyproject.toml
```

---

## **Phase 1: Configuration & Specification**

**Action:** Populate the project's configuration and specification files with the exact content below.

### **1.1 `pyproject.toml`**

**Path:** `kranos-reporter/pyproject.toml`

```toml
[tool.black]
line-length = 100

[tool.isort]
profile = "black"
line_length = 100
```

### **1.2 `requirements.txt`**

**Path:** `kranos-reporter/requirements.txt`

```text
streamlit
pandas
black
isort
pytest
```

### **1.3 `.gitignore`**

**Path:** `kranos-reporter/.gitignore`

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.pytest_cache/
.hypothesis/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database files
*.db
*.sqlite3

# IDEs
.idea/
.vscode/
```

### **1.4 `app_specs.md`**

**Path:** `kranos-reporter/app_specs.md`

# Application Specifications: Kranos Reporter

## 1. Overview

This application is a management tool for Kranos MMA, designed to handle member data, manage membership plans, and generate financial and renewal reports.

## 2. Database Schema

The application uses an SQLite database with the following tables:

| Table Name                | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| `members`                 | Stores personal information for each member. |
| `group_plans`             | Defines templates for group class plans.     |
| `group_class_memberships` | Links members to group plans.                |
| `pt_memberships`          | Tracks personal training sessions.           |

## 3. UI Tabs & Functionality

### 3.1 Members Tab

- **View:** Display all members in a table.
- **Create:** Form to add a new member.
- **Update:** Form to edit an existing member's details.
- **Delete:** Button to remove a member.

### 3.2 Group Plans Tab

- **View:** Display all group plans in a table.
- **Create:** Form to add a new group plan.
- **Update:** Form to edit an existing plan.
- **Delete:** Button to remove a plan.

### 3.3 Memberships Tab

- A master tab with a radio button to select mode: "Group Class" or "Personal Training".
- **Group Class Mode:**
    - Assign a member to a `group_plan`.
    - Record payment, start date, and end date.
    - View all active group class memberships.
- **Personal Training Mode:**
    - Record PT sessions purchased by a member.
    - Track used sessions.
    - View all active PT memberships.

### 3.4 Reporting Tab

- **Financial Report:**
    - Aggregates revenue from both group and PT memberships.
    - Filterable by a date range.
- **Renewals Report:**
    - Shows all group class memberships expiring within the next 30 days.

---

## **Phase 2: Data Modeling and Schema Definition**

**Action:** Define the data structures and the database schema.

### **2.1 `database.py`**

**Path:** `kranos-reporter/reporter/database.py`

```python
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
```

### **2.2 `models.py`**

**Path:** `kranos-reporter/reporter/models.py`

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class Member:
    id: Optional[int]
    name: str
    email: Optional[str]
    phone: Optional[str]
    join_date: str
    status: str


@dataclass
class GroupPlan:
    id: Optional[int]
    name: str
    duration_days: int
    price: float


@dataclass
class GroupClassMembership:
    id: Optional[int]
    member_id: int
    plan_id: int
    start_date: str
    end_date: str
    price: float
    payment_date: str


@dataclass
class PtMembership:
    id: Optional[int]
    member_id: int
    sessions_total: int
    sessions_used: int
    price: float
    payment_date: str
```

---

## **Phase 3: Data Access Layer**

**Action:** Implement the `database_manager.py` file. This is the only module that will directly interact with the database.

**Path:** `kranos-reporter/reporter/database_manager.py`

```python
import sqlite3
from typing import List, Optional, Tuple

from reporter.database import DB_FILE
from reporter.models import (
    GroupClassMembership,
    GroupPlan,
    Member,
    PtMembership,
)


def get_connection():
    """Gets a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# --- Member Operations ---

def get_all_members() -> List[Member]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY name")
    members = [Member(**row) for row in cursor.fetchall()]
    conn.close()
    return members


def add_member(member: Member) -> Member:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO members (name, email, phone, join_date, status) VALUES (?, ?, ?, ?, ?)",
        (member.name, member.email, member.phone, member.join_date, member.status),
    )
    member.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return member


# --- Group Plan Operations ---

def get_all_group_plans() -> List[GroupPlan]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM group_plans ORDER BY name")
    plans = [GroupPlan(**row) for row in cursor.fetchall()]
    conn.close()
    return plans


def add_group_plan(plan: GroupPlan) -> GroupPlan:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO group_plans (name, duration_days, price) VALUES (?, ?, ?)",
        (plan.name, plan.duration_days, plan.price),
    )
    plan.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return plan


# --- Group Class Membership Operations ---

def get_all_group_class_memberships() -> List[Tuple[str, str, str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT m.name as member_name, gp.name as plan_name, gcm.start_date, gcm.end_date
        FROM group_class_memberships gcm
        JOIN members m ON gcm.member_id = m.id
        JOIN group_plans gp ON gcm.plan_id = gp.id
        ORDER BY gcm.end_date DESC
    """
    )
    memberships = cursor.fetchall()
    conn.close()
    return [(row["member_name"], row["plan_name"], row["start_date"], row["end_date"]) for row in memberships]


def add_group_class_membership(membership: GroupClassMembership) -> GroupClassMembership:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO group_class_memberships
        (member_id, plan_id, start_date, end_date, price, payment_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            membership.member_id,
            membership.plan_id,
            membership.start_date,
            membership.end_date,
            membership.price,
            membership.payment_date,
        ),
    )
    membership.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return membership


# --- PT Membership Operations ---

def get_all_pt_memberships() -> List[Tuple[str, int, int]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT m.name as member_name, pt.sessions_total, pt.sessions_used
        FROM pt_memberships pt
        JOIN members m ON pt.member_id = m.id
        ORDER BY m.name
    """
    )
    memberships = cursor.fetchall()
    conn.close()
    return [(row["member_name"], row["sessions_total"], row["sessions_used"]) for row in memberships]


def add_pt_membership(membership: PtMembership) -> PtMembership:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pt_memberships
        (member_id, sessions_total, sessions_used, price, payment_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            membership.member_id,
            membership.sessions_total,
            membership.sessions_used,
            membership.price,
            membership.payment_date,
        ),
    )
    membership.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return membership
```

---

## **Phase 4: Business Logic (API) Layer**

**Action:** Implement the `app_api.py` file. This layer orchestrates data operations and contains business logic.

**Path:** `kranos-reporter/reporter/app_api.py`

```python
from datetime import date, timedelta
from typing import List, Tuple

from reporter import database_manager
from reporter.models import (
    GroupClassMembership,
    GroupPlan,
    Member,
    PtMembership,
)


# --- Member API ---
def get_all_members() -> List[Member]:
    return database_manager.get_all_members()


def add_new_member(name: str, email: str, phone: str, join_date: date) -> Member:
    new_member = Member(
        id=None,
        name=name,
        email=email,
        phone=phone,
        join_date=join_date.isoformat(),
        status="Active",
    )
    return database_manager.add_member(new_member)


# --- Group Plan API ---
def get_all_group_plans() -> List[GroupPlan]:
    return database_manager.get_all_group_plans()


def add_new_group_plan(name: str, duration_days: int, price: float) -> GroupPlan:
    new_plan = GroupPlan(id=None, name=name, duration_days=duration_days, price=price)
    return database_manager.add_group_plan(new_plan)


# --- Group Class Membership API ---
def get_all_group_class_memberships() -> List[Tuple[str, str, str, str]]:
    return database_manager.get_all_group_class_memberships()


def add_new_group_class_membership(
    member_id: int, plan_id: int, start_date: date, payment_date: date
) -> GroupClassMembership:
    plans = {plan.id: plan for plan in get_all_group_plans()}
    selected_plan = plans[plan_id]
    end_date = start_date + timedelta(days=selected_plan.duration_days)

    new_membership = GroupClassMembership(
        id=None,
        member_id=member_id,
        plan_id=plan_id,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        price=selected_plan.price,
        payment_date=payment_date.isoformat(),
    )
    return database_manager.add_group_class_membership(new_membership)


# --- PT Membership API ---
def get_all_pt_memberships() -> List[Tuple[str, int, int]]:
    return database_manager.get_all_pt_memberships()


def add_new_pt_membership(
    member_id: int, sessions_total: int, price: float, payment_date: date
) -> PtMembership:
    new_membership = PtMembership(
        id=None,
        member_id=member_id,
        sessions_total=sessions_total,
        sessions_used=0,
        price=price,
        payment_date=payment_date.isoformat(),
    )
    return database_manager.add_pt_membership(new_membership)
```

---

## **Phase 5: UI Layer**

**Action:** Implement the Streamlit user interface.

**Path:** `kranos-reporter/reporter/streamlit_ui/app.py`

```python
import streamlit as st
from datetime import date

from reporter import app_api


def show_members_tab():
    st.subheader("Manage Members")

    # Form to add a new member
    with st.expander("Add New Member"):
        with st.form("new_member_form", clear_on_submit=True):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            join_date = st.date_input("Join Date", value=date.today())

            submitted = st.form_submit_button("Add Member")
            if submitted:
                if not name:
                    st.error("Name is required.")
                else:
                    app_api.add_new_member(name, email, phone, join_date)
                    st.success(f"Added member: {name}")

    # Display existing members
    st.subheader("All Members")
    members = app_api.get_all_members()
    if members:
        st.table([(m.name, m.email, m.phone, m.join_date, m.status) for m in members])
    else:
        st.info("No members found.")

def show_group_plans_tab():
    st.subheader("Manage Group Plans")

    with st.expander("Add New Group Plan"):
        with st.form("new_plan_form", clear_on_submit=True):
            name = st.text_input("Plan Name")
            duration_days = st.number_input("Duration (Days)", min_value=1, step=1)
            price = st.number_input("Price", min_value=0.0, format="%.2f")

            submitted = st.form_submit_button("Add Plan")
            if submitted:
                if not name:
                    st.error("Plan Name is required.")
                else:
                    app_api.add_new_group_plan(name, duration_days, price)
                    st.success(f"Added plan: {name}")

    st.subheader("All Group Plans")
    plans = app_api.get_all_group_plans()
    if plans:
        st.table([(p.name, f"{p.duration_days} days", f"${p.price:.2f}") for p in plans])
    else:
        st.info("No group plans found.")


def show_memberships_tab():
    st.subheader("Manage Memberships")

    mode = st.radio("Select Membership Type", ("Group Class", "Personal Training"))

    members = app_api.get_all_members()
    member_map = {m.name: m.id for m in members}
    member_names = list(member_map.keys())

    if mode == "Group Class":
        with st.expander("Add New Group Class Membership"):
            with st.form("new_gc_membership_form", clear_on_submit=True):
                member_name = st.selectbox("Member", member_names)

                plans = app_api.get_all_group_plans()
                plan_map = {p.name: p.id for p in plans}
                plan_names = list(plan_map.keys())
                plan_name = st.selectbox("Plan", plan_names)

                start_date = st.date_input("Start Date", value=date.today())
                payment_date = st.date_input("Payment Date", value=date.today())

                submitted = st.form_submit_button("Add Membership")
                if submitted:
                    if member_name and plan_name:
                        member_id = member_map[member_name]
                        plan_id = plan_map[plan_name]
                        app_api.add_new_group_class_membership(member_id, plan_id, start_date, payment_date)
                        st.success(f"Added group membership for {member_name}")

        st.subheader("Active Group Class Memberships")
        gc_memberships = app_api.get_all_group_class_memberships()
        st.table(gc_memberships)

    elif mode == "Personal Training":
        with st.expander("Add New PT Membership"):
            with st.form("new_pt_membership_form", clear_on_submit=True):
                member_name = st.selectbox("Member", member_names)
                sessions_total = st.number_input("Number of Sessions", min_value=1, step=1)
                price = st.number_input("Total Price", min_value=0.0, format="%.2f")
                payment_date = st.date_input("Payment Date", value=date.today())

                submitted = st.form_submit_button("Add PT Sessions")
                if submitted:
                    if member_name:
                        member_id = member_map[member_name]
                        app_api.add_new_pt_membership(member_id, sessions_total, price, payment_date)
                        st.success(f"Added PT sessions for {member_name}")

        st.subheader("Active PT Memberships")
        pt_memberships = app_api.get_all_pt_memberships()
        st.table(pt_memberships)


def run():
    st.title("Kranos MMA Reporter")

    tab1, tab2, tab3 = st.tabs(["Members", "Group Plans", "Memberships"])

    with tab1:
        show_members_tab()

    with tab2:
        show_group_plans_tab()

    with tab3:
        show_memberships_tab()
```

---

## **Phase 6: Application Entrypoint**

**Action:** Implement the `main.py` and `migrate_historical_data.py` scripts.

### **6.1 `main.py`**

**Path:** `kranos-reporter/reporter/main.py`

```python
from reporter.database import initialize_database
from reporter.streamlit_ui import app


def main():
    # Ensure the database and tables exist before running the app
    initialize_database()
    # Run the Streamlit UI
    app.run()


if __name__ == "__main__":
    main()
```

### **6.2 `migrate_historical_data.py`**

**Path:** `kranos-reporter/reporter/migrate_historical_data.py`

```python
import pandas as pd
from datetime import datetime, timedelta, date

from reporter.database import initialize_database
from reporter import database_manager
from reporter.models import Member, GroupClassMembership, PtMembership, GroupPlan


def migrate():
    print("Initializing database...")
    initialize_database()
    print("Database initialized.")

    # --- Pre-populate a default group plan if none exist ---
    if not database_manager.get_all_group_plans():
        print("No group plans found. Adding a default plan.")
        default_plan = GroupPlan(
            id=None,
            name="Default MMA - 90 Days",
            duration_days=90,
            price=12000.00
        )
        database_manager.add_group_plan(default_plan)
        print("Default plan added.")

    default_plan_id = database_manager.get_all_group_plans()[0].id

    # --- Migrate Group Class Members ---
    print("Migrating group class members from 'Kranos MMA Members.xlsx - GC.csv'...")
    try:
        gc_df = pd.read_csv("Kranos MMA Members.xlsx - GC.csv")
        for _, row in gc_df.iterrows():
            # Create Member
            member = Member(
                id=None,
                name=row["Name"],
                email=None,
                phone=row["Contact"],
                join_date=datetime.strptime(row["Joining Date"], "%d/%m/%Y").strftime("%Y-%m-%d"),
                status="Active",
            )
            created_member = database_manager.add_member(member)

            # Create Membership
            start_date = datetime.strptime(row["Joining Date"], "%d/%m/%Y")
            end_date = start_date + timedelta(days=90) # Assuming 90 days for all historical data

            membership = GroupClassMembership(
                id=None,
                member_id=created_member.id,
                plan_id=default_plan_id,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                price=float(row["Amount"]),
                payment_date=start_date.strftime("%Y-%m-%d"),
            )
            database_manager.add_group_class_membership(membership)
        print(f"Successfully migrated {len(gc_df)} group class members.")
    except FileNotFoundError:
        print("WARNING: 'Kranos MMA Members.xlsx - GC.csv' not found. Skipping migration.")

    # --- Migrate PT Members ---
    print("Migrating PT members from 'Kranos MMA Members.xlsx - PT.csv'...")
    try:
        pt_df = pd.read_csv("Kranos MMA Members.xlsx - PT.csv")
        for _, row in pt_df.iterrows():
            # Create Member if not exists (simple check by name)
            all_members = {m.name: m for m in database_manager.get_all_members()}
            if row["Name"] not in all_members:
                member = Member(
                    id=None, name=row["Name"], email=None, phone=None, join_date=date.today().isoformat(), status="Active"
                )
                created_member = database_manager.add_member(member)
            else:
                created_member = all_members[row["Name"]]

            # Create PT Membership
            pt_membership = PtMembership(
                id=None,
                member_id=created_member.id,
                sessions_total=int(row["Sessions"]),
                sessions_used=0,
                price=float(row["Amount"]),
                payment_date=datetime.strptime(row["Date"], "%d/%m/%Y").strftime("%Y-%m-%d"),
            )
            database_manager.add_pt_membership(pt_membership)
        print(f"Successfully migrated {len(pt_df)} PT members.")
    except FileNotFoundError:
        print("WARNING: 'Kranos MMA Members.xlsx - PT.csv' not found. Skipping migration.")


if __name__ == "__main__":
    migrate()
```

---

## **Phase 7: Final Documentation & Execution**

**Action:** Populate the `README.md` and then follow the execution instructions.

### **7.1 `README.md`**

**Path:** `kranos-reporter/README.md`

# Kranos Reporter

This is a Streamlit application for managing memberships and finances for Kranos MMA.

## Setup and Execution

### Step 1: Install Dependencies

Ensure you have Python 3.8+ installed. It is highly recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Create and activate a virtual environment (Windows)
python -m venv .venv
.\.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Database Migration (First-Time Setup)

Before running the application for the first time, you must migrate the historical data.

**Place the following files in the root directory of this project:**
- `Kranos MMA Members.xlsx - GC.csv`
- `Kranos MMA Members.xlsx - PT.csv`

Then, run the migration script from the root directory:

```bash
python -m reporter.migrate_historical_data
```

This will create and populate the database at `reporter/data/kranos_data.db`.

### Step 3: Run the Application

Once the database is migrated, you can run the Streamlit application:

```bash
streamlit run reporter/main.py
```

### Step 4: Code Style

This project uses `black` for code formatting and `isort` for import sorting. To maintain a consistent style, run the following commands before committing any changes:

```bash
# Sort imports
isort reporter/

# Format code
black reporter/
```

### Step 5: Run Tests

To run the automated test suite, use `pytest`:

```bash
pytest
```
---

## **Execution Workflow Summary**

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Migrate Database:**
    - Place `Kranos MMA Members.xlsx - GC.csv` and `Kranos MMA Members.xlsx - PT.csv` in the root `kranos-reporter/` directory.
    - Run: `python -m reporter.migrate_historical_data`

3.  **Run Application:**

    ```bash
    streamlit run reporter/main.py
    ```