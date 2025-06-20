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

    all_members = app_api.get_all_members() # List of Member objects
    # Handle case where all_members might be empty
    if not all_members:
        st.warning("No members found. Please add members in the 'Members' tab first.")
        return

    if mode == "Group Class":
        with st.expander("Add New Group Class Membership"):
            with st.form("new_gc_membership_form", clear_on_submit=True):
                selected_member = st.selectbox(
                    "Member",
                    all_members,
                    format_func=lambda m: m.name if m else "Select Member",
                    index=None, # Add placeholder
                    placeholder="Select Member..."
                )

                all_plans = app_api.get_all_group_plans() # List of GroupPlan objects
                if not all_plans:
                    st.warning("No group plans found. Please add plans in the 'Group Plans' tab first.")
                    # Disable form submission or handle appropriately
                    submitted = st.form_submit_button("Add Membership", disabled=True)
                else:
                    selected_plan_object = st.selectbox(
                        "Plan",
                        all_plans,
                        format_func=lambda p: p.name if p else "Select Plan",
                        index=None, # Add placeholder
                        placeholder="Select Plan..."
                    )
                    start_date = st.date_input("Start Date", value=date.today())
                    payment_date = st.date_input("Payment Date", value=date.today())

                    submitted = st.form_submit_button("Add Membership")

                if submitted:
                    if selected_member and selected_plan_object:
                        member_id = selected_member.id
                        plan_id = selected_plan_object.id
                        app_api.add_new_group_class_membership(member_id, plan_id, start_date, payment_date)
                        st.success(f"Added group membership for {selected_member.name}")
                    elif not selected_member:
                        st.error("Please select a member.")
                    elif not selected_plan_object:
                        st.error("Please select a plan.")


        st.subheader("Active Group Class Memberships")
        gc_memberships = app_api.get_all_group_class_memberships()
        st.table(gc_memberships)

    elif mode == "Personal Training":
        with st.expander("Add New PT Membership"):
            with st.form("new_pt_membership_form", clear_on_submit=True):
                selected_member = st.selectbox(
                    "Member",
                    all_members,
                    format_func=lambda m: m.name if m else "Select Member",
                    index=None, # Add placeholder
                    placeholder="Select Member..."
                )
                sessions_total = st.number_input("Number of Sessions", min_value=1, step=1)
                price = st.number_input("Total Price", min_value=0.0, format="%.2f")
                payment_date = st.date_input("Payment Date", value=date.today())

                submitted = st.form_submit_button("Add PT Sessions")
                if submitted:
                    if selected_member:
                        member_id = selected_member.id
                        app_api.add_new_pt_membership(member_id, sessions_total, price, payment_date)
                        st.success(f"Added PT sessions for {selected_member.name}")
                    else:
                        st.error("Please select a member.")

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
