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
