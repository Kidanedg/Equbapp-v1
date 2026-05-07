############################################################
# EQUB APP SYSTEMS (TECHNOLOGY TRANSFER READY)
# Ethiopian Equb Digital Finance Platform
# Web → Mobile → Desktop Architecture
############################################################

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Equb App Systems",
    layout="wide",
    page_icon="🇪🇹"
)

# =========================================================
# WELCOME SECTION
# =========================================================
st.title("🇪🇹 Equb App Systems")

st.markdown("""
## 👋 Welcome to Equb App Systems

Welcome to the **Equb App Systems**, a modern digital platform designed to support
traditional Ethiopian rotating savings and credit associations (**Equb**).

This system transforms traditional community-based financial practices into a
secure and intelligent digital ecosystem using:

- Mathematical and statistical modeling
- Financial simulation systems
- Digital contribution management
- Loan and savings analytics
- Smart financial tracking and reporting

The platform is designed as a **Technology Transfer Project** with future scalability
towards:

✅ Web-based systems
✅ Mobile applications
✅ Desktop enterprise systems
✅ Cloud-based financial platforms

---

## 🎯 Main Objectives

- Digitize traditional Equb operations
- Improve financial transparency
- Automate contribution management
- Support equitable payout mechanisms
- Enhance sustainability using analytics
- Build scalable Ethiopian fintech solutions

---

## 🇪🇹 Ethiopian Equb Practices Included

This system incorporates common Ethiopian Equb practices such as:

- Monthly member contributions
- Rotational payout systems
- Lottery/winner-based payout mechanisms
- Community trust structures
- Emergency support systems
- Social savings culture
- Loan services for members
- Penalty handling for late payments

---

## 🙏 Acknowledgment

This project is developed under a **Technology Transfer Initiative**.

Special thanks to the **Technology Transfer Office, Aksum University**
for supporting and funding this innovative digital community finance project.
""")

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
def init_db():

    if "db" not in st.session_state:

        st.session_state.db = {

            "equb_fund": 50000.0,

            "members": {},

            "transactions": [],

            "history": [],

            "winners": [],

            "loans": [],

            "monthly_contribution": 1000.0,

            "equb_round": 1
        }

def db_get(key):
    return st.session_state.db[key]

def db_set(key, value):
    st.session_state.db[key] = value

def db_append(key, value):
    st.session_state.db[key].append(value)

init_db()

# =========================================================
# MATHEMATICAL MODEL
# =========================================================
class EqubModel:

    @staticmethod
    def total_contribution(contributions):
        return sum(contributions.values())

    @staticmethod
    def payout_amount(total_fund):
        return total_fund

    @staticmethod
    def random_winner(member_list):
        return random.choice(member_list)

    @staticmethod
    def loan_interest(amount, rate):
        return amount * (1 + rate)

# =========================================================
# BUSINESS SERVICE LAYER
# =========================================================
class EqubService:

    @staticmethod
    def add_member(name, phone, city):

        members = db_get("members")

        members[name] = {
            "phone": phone,
            "city": city,
            "joined": datetime.now(),
            "total_paid": 0,
            "received": False
        }

        db_set("members", members)

    @staticmethod
    def collect_contributions():

        members = db_get("members")
        contribution = db_get("monthly_contribution")

        total = 0

        for m in members:

            members[m]["total_paid"] += contribution
            total += contribution

        db_set("members", members)

        fund = db_get("equb_fund")
        fund += total

        db_set("equb_fund", fund)

        db_append("transactions", {
            "time": datetime.now(),
            "type": "Contribution",
            "amount": total
        })

        return total

    @staticmethod
    def select_winner():

        members = db_get("members")

        eligible = [
            m for m in members
            if not members[m]["received"]
        ]

        if len(eligible) == 0:
            return None, 0

        winner = EqubModel.random_winner(eligible)

        payout = db_get("equb_fund")

        members[winner]["received"] = True

        db_set("members", members)

        db_append("winners", {
            "round": db_get("equb_round"),
            "winner": winner,
            "amount": payout,
            "time": datetime.now()
        })

        db_append("transactions", {
            "time": datetime.now(),
            "type": "Payout",
            "amount": payout
        })

        db_set("equb_fund", 0)

        db_set(
            "equb_round",
            db_get("equb_round") + 1
        )

        return winner, payout

    @staticmethod
    def issue_loan(member, amount, rate):

        fund = db_get("equb_fund")

        if amount > fund:
            return False

        total_due = EqubModel.loan_interest(amount, rate)

        db_append("loans", {
            "member": member,
            "amount": amount,
            "interest_rate": rate,
            "total_due": total_due,
            "status": "Active",
            "date": datetime.now()
        })

        db_set("equb_fund", fund - amount)

        db_append("transactions", {
            "time": datetime.now(),
            "type": "Loan",
            "amount": amount
        })

        return True

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Equb Navigation")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Members",
        "Contributions",
        "Equb Winners",
        "Loan System",
        "Analytics",
        "Mathematical Model"
    ]
)

st.sidebar.markdown("---")

monthly_contribution = st.sidebar.number_input(
    "Monthly Contribution",
    value=1000.0
)

db_set("monthly_contribution", monthly_contribution)

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":

    st.subheader("📊 Equb Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Fund",
        f"{db_get('equb_fund'):.2f} ETB"
    )

    col2.metric(
        "Members",
        len(db_get("members"))
    )

    col3.metric(
        "Winners",
        len(db_get("winners"))
    )

    col4.metric(
        "Loans",
        len(db_get("loans"))
    )

    st.markdown("---")

    st.subheader("📈 Fund History")

    if db_get("history"):

        df_hist = pd.DataFrame(
            db_get("history"),
            columns=["Fund"]
        )

        st.line_chart(df_hist)

# =========================================================
# MEMBERS
# =========================================================
elif menu == "Members":

    st.subheader("👥 Member Registration")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    city = st.text_input("City")

    if st.button("Add Member"):

        if name:

            EqubService.add_member(
                name,
                phone,
                city
            )

            st.success("Member registered successfully")

    st.markdown("---")

    st.subheader("📋 Registered Members")

    if db_get("members"):

        df = pd.DataFrame(
            db_get("members")
        ).T

        st.dataframe(df)

# =========================================================
# CONTRIBUTIONS
# =========================================================
elif menu == "Contributions":

    st.subheader("💰 Monthly Contribution Collection")

    st.info(
        f"Current Monthly Contribution: "
        f"{monthly_contribution:.2f} ETB"
    )

    if st.button("Collect Contributions"):

        total = EqubService.collect_contributions()

        fund = db_get("equb_fund")

        db_append("history", fund)

        st.success(
            f"Total Collected: {total:.2f} ETB"
        )

# =========================================================
# WINNERS
# =========================================================
elif menu == "Equb Winners":

    st.subheader("🏆 Equb Winner Selection")

    st.write(
        f"Current Round: "
        f"{db_get('equb_round')}"
    )

    if st.button("Select Winner"):

        winner, payout = EqubService.select_winner()

        if winner:

            st.success(
                f"{winner} won "
                f"{payout:.2f} ETB"
            )

        else:

            st.warning(
                "All members already received payout"
            )

    st.markdown("---")

    st.subheader("📋 Winner History")

    if db_get("winners"):

        st.dataframe(
            pd.DataFrame(
                db_get("winners")
            )
        )

# =========================================================
# LOAN SYSTEM
# =========================================================
elif menu == "Loan System":

    st.subheader("💳 Member Loan System")

    members = list(
        db_get("members").keys()
    )

    if len(members) == 0:

        st.warning("No members registered")

    else:

        borrower = st.selectbox(
            "Select Member",
            members
        )

        amount = st.number_input(
            "Loan Amount",
            value=5000.0
        )

        rate = st.slider(
            "Interest Rate",
            0.0,
            0.5,
            0.1
        )

        if st.button("Issue Loan"):

            success = EqubService.issue_loan(
                borrower,
                amount,
                rate
            )

            if success:
                st.success("Loan issued successfully")
            else:
                st.error("Insufficient Equb fund")

    st.markdown("---")

    st.subheader("📋 Loan Records")

    if db_get("loans"):

        st.dataframe(
            pd.DataFrame(
                db_get("loans")
            )
        )

# =========================================================
# ANALYTICS
# =========================================================
elif menu == "Analytics":

    st.subheader("📐 Financial Analytics")

    members = db_get("members")

    total_members = len(members)

    total_paid = sum([
        members[m]["total_paid"]
        for m in members
    ]) if members else 0

    total_loans = sum([
        loan["amount"]
        for loan in db_get("loans")
    ]) if db_get("loans") else 0

    st.metric(
        "Total Members",
        total_members
    )

    st.metric(
        "Total Contributions",
        f"{total_paid:.2f} ETB"
    )

    st.metric(
        "Current Equb Fund",
        f"{db_get('equb_fund'):.2f} ETB"
    )

    st.metric(
        "Total Loans",
        f"{total_loans:.2f} ETB"
    )

    st.markdown("---")

    st.subheader("📋 Transactions")

    if db_get("transactions"):

        st.dataframe(
            pd.DataFrame(
                db_get("transactions")
            )
        )

# =========================================================
# MATHEMATICAL MODEL
# =========================================================
elif menu == "Mathematical Model":

    st.subheader("📘 Mathematical & Statistical Model")

    st.markdown("""
### Core Equb Financial Model
""")

    :contentReference[oaicite:0]{index=0}

    st.markdown("""
Where:

- \(F_t\): Current Equb fund
- \(C_t\): Member contributions
- \(I_t\): Investment income
- \(P_t\): Winner payout
- \(L_t\): Loans issued
- \(R_t\): Loan repayments

---

### Winner Selection Probability
""")

    :contentReference[oaicite:1]{index=1}

    st.markdown("""
Where:

- \(P(W_i)\): Probability member \(i\) wins
- \(N\): Number of eligible members

---

### Loan Growth Model
""")

    :contentReference[oaicite:2]{index=2}

    st.markdown("""
Where:

- \(A_t\): Total repayment
- \(P\): Principal loan amount
- \(r\): Interest rate

---

### Sustainability Condition
""")

    :contentReference[oaicite:3]{index=3}

    st.markdown("""
These models support:

- Sustainability analysis
- Risk analysis
- Financial forecasting
- Policy optimization
- Community financial planning
""")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown("""
### 🇪🇹 Equb App Systems

Technology Transfer Project
Department of Statistics, Aksum University

Developed for Ethiopian Community Finance Digital Transformation
""")
