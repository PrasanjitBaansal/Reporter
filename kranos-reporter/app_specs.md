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
