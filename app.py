############################################################
# IDDIR WEB APP (TECH TRANSFER READY)
# Clean Architecture for Web → Mobile → Desktop
############################################################

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="Iddir Web System", layout="wide")

# =========================================================
# "DATABASE LAYER" (REPLACE LATER WITH REAL DB)
# =========================================================
def init_db():
    if "db" not in st.session_state:
        st.session_state.db = {
            "fund": 1000.0,
            "members": {},
            "transactions": [],
            "history": []
        }

def db_get(key):
    return st.session_state.db[key]

def db_set(key, value):
    st.session_state.db[key] = value

def db_append(key, value):
    st.session_state.db[key].append(value)

init_db()

# =========================================================
# MODEL LAYER (PURE LOGIC)
# =========================================================
class IddirModel:

    @staticmethod
    def total_contribution(contributions):
        return sum(contributions.values())

    @staticmethod
    def update_fund(F_t, C_t, r, D_t):
        return F_t + C_t + r * F_t - D_t

    @staticmethod
    def emergency(p):
        return np.random.binomial(1, p)

    @staticmethod
    def aid(F_t, A_max):
        return min(F_t, A_max)

# =========================================================
# SERVICE LAYER (BUSINESS LOGIC)
# =========================================================
class IddirService:

    @staticmethod
    def add_member(name, capacity):
        members = db_get("members")
        members[name] = {"capacity": capacity}
        db_set("members", members)

    @staticmethod
    def contribute(contributions):
        fund = db_get("fund")
        C_t = IddirModel.total_contribution(contributions)

        fund += C_t
        db_set("fund", fund)

        db_append("transactions", {
            "time": datetime.now(),
            "type": "Contribution",
            "amount": C_t
        })

        return C_t

    @staticmethod
    def process_emergency(p, A_max):
        fund = db_get("fund")

        E_t = IddirModel.emergency(p)

        if E_t == 1:
            A_t = IddirModel.aid(fund, A_max)
            fund -= A_t

            db_set("fund", fund)

            db_append("transactions", {
                "time": datetime.now(),
                "type": "Aid",
                "amount": A_t
            })

            return True, A_t
        return False, 0

    @staticmethod
    def apply_interest(r):
        fund = db_get("fund")
        fund = IddirModel.update_fund(fund, 0, r, 0)

        db_set("fund", fund)
        db_append("history", fund)

# =========================================================
# UI LAYER (WEB INTERFACE)
# =========================================================
st.title("🇪🇹 Iddir Web-Based System")
st.markdown("From Mathematical Model → Real Digital Platform")

# ---------------- NAVIGATION ----------------
menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Members",
    "Contributions",
    "Emergency",
    "Analytics"
])

# ---------------- PARAMETERS ----------------
st.sidebar.header("⚙️ Model Controls")
r = st.sidebar.slider("Interest Rate (r)", 0.0, 0.2, 0.02)
p = st.sidebar.slider("Emergency Probability (p)", 0.0, 1.0, 0.2)
A_max = st.sidebar.number_input("Max Aid", value=500.0)

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":

    st.subheader("📊 System Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Fund", f"{db_get('fund'):.2f}")
    col2.metric("Members", len(db_get("members")))
    col3.metric("Transactions", len(db_get("transactions")))

    if db_get("history"):
        st.line_chart(pd.DataFrame(db_get("history"), columns=["Fund"]))

# =========================================================
# MEMBERS
# =========================================================
elif menu == "Members":

    st.subheader("👥 Member Management")

    name = st.text_input("Member Name")
    capacity = st.number_input("Capacity", value=50.0)

    if st.button("Add Member"):
        if name:
            IddirService.add_member(name, capacity)
            st.success("Member added")

    if db_get("members"):
        st.dataframe(pd.DataFrame(db_get("members")).T)

# =========================================================
# CONTRIBUTIONS
# =========================================================
elif menu == "Contributions":

    st.subheader("💰 Contributions")

    members = db_get("members")

    contributions = {}

    for m in members:
        contributions[m] = st.number_input(f"{m}", min_value=0.0, key=m)

    if st.button("Submit Contributions"):
        C_t = IddirService.contribute(contributions)
        st.success(f"Total: {C_t:.2f}")

# =========================================================
# EMERGENCY
# =========================================================
elif menu == "Emergency":

    st.subheader("🚨 Emergency Handling")

    if st.button("Trigger Emergency"):
        occurred, amount = IddirService.process_emergency(p, A_max)

        if occurred:
            st.error(f"Emergency! Paid: {amount:.2f}")
        else:
            st.info("No emergency")

# =========================================================
# ANALYTICS
# =========================================================
elif menu == "Analytics":

    st.subheader("📐 Sustainability Analysis")

    st.markdown("Condition:")

    :contentReference[oaicite:0]{index=0}

    members = db_get("members")

    avg_c = np.mean([m["capacity"] for m in members.values()]) if members else 0

    inflow = avg_c * len(members) + r * db_get("fund")
    outflow = p * A_max

    st.write(f"Inflow: {inflow:.2f}")
    st.write(f"Outflow: {outflow:.2f}")

    if inflow >= outflow:
        st.success("Sustainable")
    else:
        st.error("Not Sustainable")

    if db_get("transactions"):
        st.dataframe(pd.DataFrame(db_get("transactions")))

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown("Technology Transfer System | Aksum University 🇪🇹")
