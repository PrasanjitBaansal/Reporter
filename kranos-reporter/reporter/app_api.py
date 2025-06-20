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
