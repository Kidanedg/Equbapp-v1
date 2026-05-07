############################################################
# EQUB APP SYSTEMS (FULL ENTERPRISE VERSION)
# Ethiopian Digital Rotating Savings & Credit Platform
# Technology Transfer Demonstration System
############################################################

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import uuid

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Equb App Systems",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.main {
    background-color: #f8f9fa;
}

h1, h2, h3 {
    color: #0B3D91;
}

div.stButton > button {
    background-color: #0B3D91;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-weight: bold;
    width: 100%;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# APPLICATION TITLE
# =========================================================
st.title("🇪🇹 Equb App Systems")

st.markdown("""
## Ethiopian Community Finance Digital Transformation Platform

The **Equb App Systems** platform modernizes traditional Ethiopian
rotating savings and credit associations through digital technologies,
financial analytics, statistical modeling, and intelligent management systems.

This project is designed under a **Technology Transfer Initiative**
to support scalable Ethiopian fintech innovation.
""")

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
def initialize_database():

    if "equb_db" not in st.session_state:

        st.session_state.equb_db = {

            "system_info": {

                "organization": "Aksum University",

                "project": "Equb App Systems",

                "version": "2.0 Enterprise",

                "created": datetime.now()
            },

            "financials": {

                "equb_fund": 100000.0,

                "monthly_contribution": 1000.0,

                "interest_income": 0.0
            },

            "members": {},

            "transactions": [],

            "winners": [],

            "loans": [],

            "fund_history": [],

            "analytics": {

                "total_contributions": 0,

                "total_payouts": 0,

                "total_loans": 0
            },

            "equb_round": 1
        }

initialize_database()

# =========================================================
# DATABASE HELPER
# =========================================================
def db():
    return st.session_state.equb_db

# =========================================================
# MATHEMATICAL MODELING
# =========================================================
class EqubMathematics:

    @staticmethod
    def total_contributions(member_data):

        total = 0

        for member in member_data.values():

            total += member["total_paid"]

        return total

    @staticmethod
    def sustainability_ratio(fund, liabilities):

        if liabilities == 0:

            return 1.0

        return fund / liabilities

    @staticmethod
    def payout_probability(n):

        if n <= 0:

            return 0

        return 1 / n

    @staticmethod
    def compound_loan(principal, rate):

        return principal * (1 + rate)

    @staticmethod
    def expected_monthly_fund(members, contribution):

        return members * contribution

# =========================================================
# BUSINESS SERVICE LAYER
# =========================================================
class EqubService:

    @staticmethod
    def add_member(full_name, phone, city):

        member_id = str(uuid.uuid4())[:8]

        db()["members"][member_id] = {

            "member_id": member_id,

            "full_name": full_name,

            "phone": phone,

            "city": city,

            "join_date": datetime.now(),

            "total_paid": 0.0,

            "received_payout": False,

            "status": "Active"
        }

    @staticmethod
    def collect_monthly_contributions():

        members = db()["members"]

        contribution = db()["financials"]["monthly_contribution"]

        total_collection = 0

        for member_id in members:

            members[member_id]["total_paid"] += contribution

            total_collection += contribution

        db()["financials"]["equb_fund"] += total_collection

        db()["analytics"]["total_contributions"] += total_collection

        db()["transactions"].append({

            "date": datetime.now(),

            "type": "Contribution",

            "amount": total_collection,

            "description": "Monthly member contributions"
        })

        db()["fund_history"].append({

            "date": datetime.now(),

            "fund": db()["financials"]["equb_fund"]
        })

        return total_collection

    @staticmethod
    def select_winner():

        eligible_members = []

        for member_id, member in db()["members"].items():

            if not member["received_payout"]:

                eligible_members.append(member_id)

        if len(eligible_members) == 0:

            return None

        winner_id = random.choice(eligible_members)

        payout_amount = db()["financials"]["equb_fund"]

        db()["members"][winner_id]["received_payout"] = True

        db()["winners"].append({

            "round": db()["equb_round"],

            "winner": db()["members"][winner_id]["full_name"],

            "amount": payout_amount,

            "date": datetime.now()
        })

        db()["transactions"].append({

            "date": datetime.now(),

            "type": "Payout",

            "amount": payout_amount,

            "description": "Equb payout"
        })

        db()["analytics"]["total_payouts"] += payout_amount

        db()["financials"]["equb_fund"] = 0

        db()["equb_round"] += 1

        return winner_id, payout_amount

    @staticmethod
    def issue_loan(member_id, amount, rate):

        available_fund = db()["financials"]["equb_fund"]

        if amount > available_fund:

            return False

        total_due = EqubMathematics.compound_loan(
            amount,
            rate
        )

        db()["loans"].append({

            "member": db()["members"][member_id]["full_name"],

            "principal": amount,

            "interest_rate": rate,

            "total_due": total_due,

            "issue_date": datetime.now(),

            "status": "Active"
        })

        db()["financials"]["equb_fund"] -= amount

        db()["analytics"]["total_loans"] += amount

        db()["transactions"].append({

            "date": datetime.now(),

            "type": "Loan",

            "amount": amount,

            "description": "Loan issued"
        })

        return True

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
st.sidebar.title("⚙️ Navigation")

menu = st.sidebar.radio(

    "Select Module",

    [

        "Dashboard",

        "Member Management",

        "Contribution System",

        "Winner Selection",

        "Loan Management",

        "Financial Analytics",

        "Mathematical Models",

        "System Report"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ System Settings")

monthly_contribution = st.sidebar.number_input(

    "Monthly Contribution (ETB)",

    value=float(db()["financials"]["monthly_contribution"]),

    min_value=100.0
)

db()["financials"]["monthly_contribution"] = monthly_contribution

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":

    st.header("📊 Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(

        "Current Fund",

        f"{db()['financials']['equb_fund']:,.2f} ETB"
    )

    col2.metric(

        "Registered Members",

        len(db()["members"])
    )

    col3.metric(

        "Completed Winners",

        len(db()["winners"])
    )

    col4.metric(

        "Active Loans",

        len(db()["loans"])
    )

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:

        st.subheader("📈 Fund Growth Trend")

        if len(db()["fund_history"]) > 0:

            fund_df = pd.DataFrame(
                db()["fund_history"]
            )

            st.line_chart(fund_df["fund"])

        else:

            st.info("No historical fund data available.")

    with colB:

        st.subheader("📋 Financial Summary")

        summary_df = pd.DataFrame({

            "Metric": [

                "Total Contributions",

                "Total Loans",

                "Total Payouts"
            ],

            "Value": [

                db()["analytics"]["total_contributions"],

                db()["analytics"]["total_loans"],

                db()["analytics"]["total_payouts"]
            ]
        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

# =========================================================
# MEMBER MANAGEMENT
# =========================================================
elif menu == "Member Management":

    st.header("👥 Member Registration & Management")

    with st.form("member_form"):

        full_name = st.text_input("Full Name")

        phone = st.text_input("Phone Number")

        city = st.text_input("City")

        submitted = st.form_submit_button(
            "Register Member"
        )

        if submitted:

            if full_name.strip() == "":

                st.error("Full name is required.")

            else:

                EqubService.add_member(

                    full_name,

                    phone,

                    city
                )

                st.success(
                    "Member registered successfully."
                )

    st.markdown("---")

    st.subheader("📋 Registered Members")

    if len(db()["members"]) > 0:

        members_df = pd.DataFrame(
            db()["members"]
        ).T

        st.dataframe(

            members_df,

            use_container_width=True
        )

    else:

        st.info("No members registered.")

# =========================================================
# CONTRIBUTION SYSTEM
# =========================================================
elif menu == "Contribution System":

    st.header("💰 Monthly Contribution Collection")

    st.info(

        f"Current Monthly Contribution: "

        f"{monthly_contribution:,.2f} ETB"
    )

    if st.button("Collect Monthly Contributions"):

        collected = EqubService.collect_monthly_contributions()

        st.success(

            f"Successfully collected "

            f"{collected:,.2f} ETB"
        )

    st.markdown("---")

    st.subheader("📋 Transaction Records")

    if len(db()["transactions"]) > 0:

        transaction_df = pd.DataFrame(
            db()["transactions"]
        )

        st.dataframe(

            transaction_df,

            use_container_width=True
        )

# =========================================================
# WINNER SELECTION
# =========================================================
elif menu == "Winner Selection":

    st.header("🏆 Equb Winner Selection")

    st.metric(

        "Current Equb Round",

        db()["equb_round"]
    )

    if st.button("Select Winner"):

        result = EqubService.select_winner()

        if result is not None:

            winner_id, amount = result

            winner_name = db()["members"][winner_id]["full_name"]

            st.success(

                f"🎉 {winner_name} won "

                f"{amount:,.2f} ETB"
            )

        else:

            st.warning(

                "All members already received payout."
            )

    st.markdown("---")

    st.subheader("📋 Winner History")

    if len(db()["winners"]) > 0:

        winners_df = pd.DataFrame(
            db()["winners"]
        )

        st.dataframe(

            winners_df,

            use_container_width=True
        )

# =========================================================
# LOAN MANAGEMENT
# =========================================================
elif menu == "Loan Management":

    st.header("💳 Loan Management System")

    member_options = {

        member_id: data["full_name"]

        for member_id, data
        in db()["members"].items()
    }

    if len(member_options) == 0:

        st.warning("No members registered.")

    else:

        selected_member = st.selectbox(

            "Select Borrower",

            options=list(member_options.keys()),

            format_func=lambda x: member_options[x]
        )

        loan_amount = st.number_input(

            "Loan Amount",

            value=5000.0,

            min_value=100.0
        )

        interest_rate = st.slider(

            "Interest Rate",

            0.00,

            0.50,

            0.10
        )

        if st.button("Issue Loan"):

            success = EqubService.issue_loan(

                selected_member,

                loan_amount,

                interest_rate
            )

            if success:

                st.success("Loan issued successfully.")

            else:

                st.error("Insufficient Equb fund.")

    st.markdown("---")

    st.subheader("📋 Loan Records")

    if len(db()["loans"]) > 0:

        loans_df = pd.DataFrame(
            db()["loans"]
        )

        st.dataframe(

            loans_df,

            use_container_width=True
        )

# =========================================================
# FINANCIAL ANALYTICS
# =========================================================
elif menu == "Financial Analytics":

    st.header("📐 Financial Analytics & Statistics")

    total_members = len(db()["members"])

    total_contributions = \
        db()["analytics"]["total_contributions"]

    total_loans = \
        db()["analytics"]["total_loans"]

    sustainability = \
        EqubMathematics.sustainability_ratio(

            db()["financials"]["equb_fund"],

            total_loans
        )

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Total Contributions",

        f"{total_contributions:,.2f} ETB"
    )

    col2.metric(

        "Total Loans",

        f"{total_loans:,.2f} ETB"
    )

    col3.metric(

        "Sustainability Ratio",

        f"{sustainability:.2f}"
    )

    st.markdown("---")

    analytics_df = pd.DataFrame({

        "Indicator": [

            "Registered Members",

            "Current Fund",

            "Total Winners",

            "Monthly Contribution"
        ],

        "Value": [

            total_members,

            db()["financials"]["equb_fund"],

            len(db()["winners"]),

            db()["financials"]["monthly_contribution"]
        ]
    })

    st.table(analytics_df)

# =========================================================
# MATHEMATICAL MODELS
# =========================================================
elif menu == "Mathematical Models":

    st.header("📘 Mathematical & Statistical Models")

    st.markdown("""
    ## Core Equb Financial Dynamics
    """)

    st.latex(r"""
    F_t = F_{t-1} + C_t + I_t + R_t - P_t - L_t
    """)

    st.markdown("""
    Where:

    - \(F_t\): Current Equb fund
    - \(C_t\): Total member contributions
    - \(I_t\): Investment income
    - \(R_t\): Loan repayments
    - \(P_t\): Winner payout
    - \(L_t\): Loans issued
    """)

    st.markdown("---")

    st.markdown("""
    ## Winner Selection Probability
    """)

    st.latex(r"""
    P(W_i)=\frac{1}{N}
    """)

    st.markdown("""
    Where:

    - \(P(W_i)\): Probability member \(i\) wins
    - \(N\): Number of eligible members
    """)

    st.markdown("---")

    st.markdown("""
    ## Loan Growth Model
    """)

    st.latex(r"""
    A = P(1+r)
    """)

    st.markdown("""
    Where:

    - \(A\): Total repayment
    - \(P\): Principal loan amount
    - \(r\): Interest rate
    """)

    st.markdown("---")

    st.markdown("""
    ## Sustainability Condition
    """)

    st.latex(r"""
    S = \frac{F_t}{L_t}
    """)

    st.markdown("""
    Interpretation:

    - \(S > 1\): Financially stable system
    - \(S = 1\): Equilibrium state
    - \(S < 1\): Financial instability risk
    """)

# =========================================================
# SYSTEM REPORT
# =========================================================
elif menu == "System Report":

    st.header("📄 Enterprise System Report")

    report_df = pd.DataFrame({

        "Indicator": [

            "Project Name",

            "Organization",

            "Version",

            "Registered Members",

            "Current Fund",

            "Total Loans",

            "Total Winners"
        ],

        "Value": [

            db()["system_info"]["project"],

            db()["system_info"]["organization"],

            db()["system_info"]["version"],

            len(db()["members"]),

            db()["financials"]["equb_fund"],

            db()["analytics"]["total_loans"],

            len(db()["winners"])
        ]
    })

    st.dataframe(

        report_df,

        use_container_width=True
    )

    csv = report_df.to_csv(index=False)

    st.download_button(

        label="⬇ Download Report CSV",

        data=csv,

        file_name="equb_report.csv",

        mime="text/csv"
    )

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown("""
### 🇪🇹 Equb App Systems

Technology Transfer Demonstration Project

Department of Statistics  
Aksum University

Developed for Ethiopian Community Finance Digital Transformation,
Smart Cooperative Finance Systems,
and Scalable Indigenous Fintech Innovation.
""")
