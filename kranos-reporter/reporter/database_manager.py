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
