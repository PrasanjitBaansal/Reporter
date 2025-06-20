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
