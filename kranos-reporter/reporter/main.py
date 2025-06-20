from reporter.database import initialize_database
from reporter.streamlit_ui import app


def main():
    # Ensure the database and tables exist before running the app
    initialize_database()
    # Run the Streamlit UI
    app.run()


if __name__ == "__main__":
    main()
