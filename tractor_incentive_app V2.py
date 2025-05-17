import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards

# import os
# import base64

# from local_modules
from congratsAnimation import animate_confetti
from calculations import calculate_incentive

st.set_page_config(
    page_title="Tractor Incentive Calculator for Territory Officer", layout="wide")

st.title("🚜 Tractor Incentive Calculator - May 2025")

st.markdown("""
### Incentive Period: **1 May to 31 May 2025**
---""")

# Path to your PDF inside the resources folder
pdf_path = "resources/Sales_Team_Incentive_May2025.pdf"

with open(pdf_path, "rb") as f:
    st.download_button(
        label="📥 Download Incentive Circular (PDF)",
        data=f,
        file_name="Sales_Team_Incentive_May2025.pdf",
        mime="application/pdf"
    )
# st.markdown("""---""")

designation = st.selectbox("Designation",
                           ["Territory officer", "Area Head", "Deputy RSM", "RSM", "Part Head"])

# Number of territories supervised
num_territories = 1
if designation != "Territory officer":
    num_territories = st.number_input(
        "Number of Territories Supervised", min_value=1, value=1)

# --- Inputs
st.subheader("Basic Inputs")
with st.expander("🔧 Enter Input Details", expanded=True):
    for i in range(num_territories):
        st.markdown(f"### Territory {i+1}")
        col1, col2, col3 = st.columns(3)

        with col1:
            budget = st.number_input(
                f"📊 Monthly Budget (Units) - ", min_value=0, value=0, key=f"budget_{i}")
            achieved = st.number_input(
                f"✅ Units Achieved - ", min_value=0, value=0, key=f"achieved_{i}")
            resale_budget = st.number_input(
                f"📦 Resale Budget - ", min_value=0, value=0, key=f"resale_budget_{i}")
            resale_achieved = st.number_input(
                f"🎯 Resale Achieved - ", min_value=0, value=0, key=f"resale_achieved_{i}")

            temp_invoice_done_by_20th = st.number_input(
                f"🗓️Temporary Invoice Sales QTY done by 20 May - ", min_value=0, value=0, key=f"temp_invoice_{i}")

        with col2:
            rotavator = st.number_input(
                f"🔩 Units Sold with Rotavator - ", min_value=0, value=0, key=f"rotavator_{i}")
            canopy = st.number_input(
                f"💫 Units Sold with Canopy - ", min_value=0, value=0, key=f"canopy_{i}")
            rx_supreme = st.number_input(
                f"🚜 New 47 Rx Supreme Units Sold - ", min_value=0, value=0, key=f"rx_supreme_{i}")
            zero_sales_upazila = st.number_input(
                f"🧣 Units Sold in Zero Sales Upazila last year - ", min_value=0, value=0, key=f"zero_sales_{i}")
            exchange_units = st.number_input(
                f"♻️ Units with Exchange Bonus - ", min_value=0, value=0, key=f"exchange_{i}")

        with col3:
            dp_20 = st.number_input(
                f"💰 Units with 20% Down Payment - ", min_value=0, value=0, key=f"dp20_{i}")
            dp_30 = st.number_input(
                f"💸 Units with 30% Down Payment - ", min_value=0, value=0, key=f"dp30_{i}")
            cash_sales = st.number_input(
                f"💵 Cash Sales Units - ", min_value=0, value=0, key=f"cash_{i}")
            installment_collection = st.number_input(
                f"No of file from where 1st Installment Collected (Previous MRO Files) - ", min_value=0, value=0, key=f"installment_{i}")
            smart_choice_above_sop = st.number_input(
                f"Smart Choice Sales (Above SOP) - ", min_value=0, value=0, key=f"smart_{i}")
            credit_note_units = st.number_input(
                f"Credit Note Units - ", min_value=0, value=0, key=f"credit_{i}")

# --- Results
st.subheader("📊 Incentive Summary")

total_final_incentive = 0
for i in range(num_territories):
    inputs = {
        "achieved": st.session_state[f"achieved_{i}"],
        "budget": st.session_state[f"budget_{i}"],
        "resale_budget": st.session_state[f"resale_budget_{i}"],
        "resale_achieved": st.session_state[f"resale_achieved_{i}"],
        "temp_invoice": st.session_state[f"temp_invoice_{i}"],
        "rotavator": st.session_state[f"rotavator_{i}"],
        "canopy": st.session_state[f"canopy_{i}"],
        "rx_supreme": st.session_state[f"rx_supreme_{i}"],
        "zero_sales": st.session_state[f"zero_sales_{i}"],
        "exchange": st.session_state[f"exchange_{i}"],
        "dp20": st.session_state[f"dp20_{i}"],
        "dp30": st.session_state[f"dp30_{i}"],
        "cash": st.session_state[f"cash_{i}"],
        "installment": st.session_state[f"installment_{i}"],
        "smart": st.session_state[f"smart_{i}"],
        "credit": st.session_state[f"credit_{i}"],
    }

    result = calculate_incentive(inputs, designation)

    st.markdown(f"""
    ### 📍 Territory #{i+1} Summary:
    - Units Incentive: TK {result['unit_incentive']:,.0f}
    - Base Incentive: Tk {result['base_incentive']:,.0f}
    - Add-ons: Tk {result['add_ons']:,.0f}
    - Penalty: Tk {result['penalty']:,.0f}
    - Multiplier Applied: x{result['multiplier']}
    - Final Incentive: **Tk {result['final']:,.0f}**
    """)

    total_final_incentive += result['final']

# st.success(
#     f"🎉 Total Incentive across all Territories: Tk {total_final_incentive:,.0f}")
animate_confetti(total_final_incentive)


style_metric_cards()
