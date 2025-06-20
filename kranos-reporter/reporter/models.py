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
