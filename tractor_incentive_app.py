import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="Tractor Incentive Calculator for Territory Officer", layout="wide")
st.title("🚜 Tractor Incentive Calculator - May 2025")

st.markdown("""
### Incentive Period: **1 May to 31 May 2025**
---
""")

designation = st.selectbox("Designation",
                           ["Territory officer", "Area Head", "Deputy RSM", "RSM", "Part Head"])

# --- Inputs
st.subheader("📥 Basic Inputs")
with st.expander("🔧 Enter Input Details", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:

        budget = st.number_input(
            "📊 Monthly Budget (Units)", min_value=0, value=0)
        achieved = st.number_input("✅ Units Achieved", min_value=0, value=0)
        resale_budget = st.number_input(
            "📦 Resale Budget", min_value=0, value=0)
        resale_achieved = st.number_input(
            "🎯 Resale Achieved", min_value=0, value=0)

        temp_invoice_done_by_20th = st.number_input(
            "🗓️Temporary Invoice Sales QTY done by 20 May?", min_value=0, value=0)

    with col2:
        rotavator = st.number_input(
            "🔩 Units Sold with Rotavator", min_value=0, value=0)
        canopy = st.number_input(
            "🛡️ Units Sold with Canopy", min_value=0, value=0)
        rx_supreme = st.number_input(
            "🚜 New 47 Rx Supreme Units Sold", min_value=0, value=0)
        zero_sales_upazila = st.number_input(
            "🧭 Units Sold in Zero Sales Upazila last year", min_value=0, value=0)
        exchange_units = st.number_input(
            "♻️ Units with Exchange Bonus", min_value=0, value=0)

    with col3:
        dp_20 = st.number_input(
            "💰 Units with 20% Down Payment", min_value=0, value=0)
        dp_30 = st.number_input(
            "💸 Units with 30% Down Payment", min_value=0, value=0)
        cash_sales = st.number_input(
            "💵 Cash Sales Units", min_value=0, value=0)
        installment_collection = st.number_input(
            "No of file from where 1st Installment Collected (Previous MRO Files)", min_value=0, value=0)
        smart_choice_above_sop = st.number_input(
            "Smart Choice Sales (Above SOP)", min_value=0, value=0)
        credit_note_units = st.number_input(
            "Credit Note Units", min_value=0, value=0)

# --- Core Calculation


def acheived_percentage(achieved, budget):
    if budget == 0:
        budget = 1
    return achieved / budget


achievement_pct = acheived_percentage(achieved, budget)


def calculate_per_unit_incentive(budget, achieved):
    global achievement_pct
    if achievement_pct >= 1.25:
        return 4000
    elif achievement_pct >= 1.0:
        return 3000
    elif achievement_pct >= 0.8:
        return 1000
    else:
        return 0


unit_incentive = calculate_per_unit_incentive(budget, achieved)
early_invoice_incentive = unit_incentive * 1.25 * \
    temp_invoice_done_by_20th  # 25% extra for temp invoice done by 20th
basic_incentive = (achieved - temp_invoice_done_by_20th) * \
    unit_incentive + early_invoice_incentive

# --- Additional Incentives
add_incentives = (
    rotavator * 500 +
    canopy * 500 +
    rx_supreme * 5000 +
    zero_sales_upazila * 1000 +
    exchange_units * 1000 +
    dp_20 * 1000 +
    dp_30 * 1500 +
    cash_sales * 5000 +
    installment_collection * 1000 +
    smart_choice_above_sop * 6000 +
    (resale_achieved - smart_choice_above_sop) * 4500
)

# --- Penalty
penalty = credit_note_units * 1500

total_before_multiplier = basic_incentive + add_incentives - penalty


# --- Designation Logic if required
if designation == "Area Head":
    total_except_multiplier = total_before_multiplier * 0.5
elif designation == "Deputy RSM":
    total_except_multiplier = total_before_multiplier * 0.4
elif designation == "RSM":
    total_except_multiplier = total_before_multiplier * 0.3
elif designation == "Part Head":
    total_except_multiplier = total_before_multiplier * 0.15
else:
    total_except_multiplier = total_before_multiplier

# --- Multiplier Logic
# Multiplier logic based on designation and achievement percentage

multiplier = 1.0
if designation == "Territory officer" and achievement_pct >= 1.75 and resale_achieved >= (resale_budget + 1):
    multiplier = 2.0
elif designation == "Territory officer" and achievement_pct >= 1.6 and resale_achieved >= (resale_budget + 1):
    multiplier = 1.5
elif designation == "Territory officer" and achievement_pct >= 1.4 and resale_achieved >= (resale_budget + 1):
    multiplier = 1.25

elif designation != "Territory officer" and achievement_pct >= 1.65 and resale_achieved >= (resale_budget + 1):
    multiplier = 2.0
elif designation != "Territory officer" and achievement_pct >= 1.5 and resale_achieved >= (resale_budget + 1):
    multiplier = 1.5
elif designation != "Territory officer" and achievement_pct >= 1.3 and resale_achieved >= (resale_budget + 1):
    multiplier = 1.25

final_incentive = total_except_multiplier * multiplier

# --- Results
st.subheader("📊 Incentive Summary")
colA, colB, colC = st.columns(3)

colA.write(f"**Per Unit Incentive:** Tk {unit_incentive:,.0f}")
colA.write(f"**Early Invoice Incentive:** Tk {early_invoice_incentive:,.0f}")
colA.write(f"**Basic Incentive:** Tk {basic_incentive:,.0f}")

colB.write(f"**Additional Incentives:** Tk {add_incentives:,.0f}")
colB.write(f"**Penalty:** Tk {penalty:,.0f}")
colB.write(f"**Total Before Multiplier:** Tk {total_before_multiplier:,.0f}")

colC.write(
    f"**Total Before Multiplier (Designation Logic):** Tk {total_except_multiplier:,.0f}")
colC.write(f"**Multiplier Applied:** x {multiplier}")

st.markdown("---")
st.success(f"🎯 **Final Incentive: Tk {final_incentive:,.0f}**")

style_metric_cards()
