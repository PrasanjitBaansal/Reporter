import pandas as pd
from datetime import datetime, timedelta, date

from reporter.database import initialize_database
from reporter import database_manager
from reporter.models import Member, GroupClassMembership, PtMembership, GroupPlan


def parse_date_flexible(date_str):
    """Tries to parse date string with %d/%m/%Y then %d/%m/%y."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return datetime.strptime(date_str, "%d/%m/%y")

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
        gc_df.columns = [col.strip() for col in gc_df.columns]
        for _, row in gc_df.iterrows():
            # Create Member
            member = Member(
                id=None,
                name=row["Client Name"],
                email=None,
                phone=row["Phone"],
                join_date=parse_date_flexible(row["Plan Start Date"]).strftime("%Y-%m-%d"),
                status="Active",
            )
            created_member = database_manager.add_member(member)

            # Create Membership
            start_date = parse_date_flexible(row["Plan Start Date"])
            end_date = start_date + timedelta(days=90) # Assuming 90 days for all historical data

            membership = GroupClassMembership(
                id=None,
                member_id=created_member.id,
                plan_id=default_plan_id,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                price=float(str(row["Amount"]).replace("₹", "").replace(",", "").strip()),
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
        pt_df.columns = [col.strip() for col in pt_df.columns]
        for _, row in pt_df.iterrows():
            # Create Member if not exists (simple check by name)
            all_members = {m.name: m for m in database_manager.get_all_members()}
            if row["Client Name"] not in all_members:
                member = Member(
                    id=None, name=row["Client Name"], email=None, phone=None, join_date=date.today().isoformat(), status="Active"
                )
                created_member = database_manager.add_member(member)
            else:
                created_member = all_members[row["Client Name"]]

            # Create PT Membership
            pt_membership = PtMembership(
                id=None,
                member_id=created_member.id,
                sessions_total=int(row["Session Count"]),
                sessions_used=0,
                price=float(row["Amount Paid"]),
                payment_date=parse_date_flexible(row["Payment Date"]).strftime("%Y-%m-%d"),
            )
            database_manager.add_pt_membership(pt_membership)
        print(f"Successfully migrated {len(pt_df)} PT members.")
    except FileNotFoundError:
        print("WARNING: 'Kranos MMA Members.xlsx - PT.csv' not found. Skipping migration.")


if __name__ == "__main__":
    migrate()
