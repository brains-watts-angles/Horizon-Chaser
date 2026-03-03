import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="The Freedom Dashboard", layout="wide")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("🏠 Property & Mortgage")
sale_price = st.sidebar.number_input("Market Value ($)", value=350000)
mortgage_bal = st.sidebar.number_input("Mortgage Balance ($)", value=143707)
monthly_p_i = st.sidebar.number_input("Monthly P+I ($)", value=715.91)
monthly_escrow = st.sidebar.number_input("Monthly Escrow ($)", value=357.93)
actual_principal = 325.82 

st.sidebar.header("🛠️ Rental Reality")
monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=2200)
maint_util = st.sidebar.number_input("Maint/Utils ($/mo)", value=740)

st.sidebar.header("💳 The Debt Anchors")
heloc_bal_init = st.sidebar.number_input("HELOC Balance ($)", value=40000)
heloc_rate = st.sidebar.slider("HELOC Rate %", 5.0, 15.0, 8.25) / 100
hvac_bal_init = st.sidebar.number_input("HVAC Balance ($)", value=9000)
hvac_on_time = st.sidebar.checkbox("Pay off HVAC by July 2027? (Avoid Penalty)", value=True)
tsp_bal_init = st.sidebar.number_input("TSP Loan ($)", value=16000)

st.sidebar.header("📈 Strategy & Market")
projection_years = st.sidebar.slider("Years to Project", 5, 30, 20)
monthly_invest = st.sidebar.number_input("Monthly S&P Savings ($)", value=1141, help="Freed up HELOC + HVAC + TSP payments")
annual_return = st.sidebar.slider("Expected S&P Return %", 5.0, 15.0, 10.0) / 100

st.sidebar.header("🏂 Lifestyle")
hourly_val = st.sidebar.number_input("Your Hourly Rate ($/hr)", value=50)
hours_mo = st.sidebar.slider("Hours/Mo on Rental", 0, 20, 5)

# --- CALCULATIONS ---
realtor_fee = sale_price * 0.08
all_debts = mortgage_bal + heloc_bal_init + hvac_bal_init + tsp_bal_init
profit_tax = max(0, (sale_price - mortgage_bal - realtor_fee) * 0.15)
recapture_tax = 12000 
keep_cash_buffer = 10000
final_seed = sale_price - realtor_fee - all_debts - profit_tax - recapture_tax - keep_cash_buffer

# --- PROJECTION LOOP ---
data = []
c_prop, c_mort, c_heloc, c_hvac = sale_price, mortgage_bal, heloc_bal_init, hvac_bal_init
c_accum_keep, c_invested_sell = 0, final_seed

for yr in range(projection_years + 1):
    nw_sell = c_invested_sell + keep_cash_buffer
    equity = c_prop - c_mort
    nw_keep = equity + c_accum_keep - c_heloc - c_hvac - tsp_bal_init
    nw_keep_final = nw_keep - (hourly_val * hours_mo * 12 * yr)
    
    data.append({"Year": yr, "Sell (Passive)": nw_sell, "Keep (Active)": nw_keep_final})
    
    # Update Sell
    c_invested_sell = (c_invested_sell * (1 + annual_return)) + (monthly_invest * 12)
    
    # Update Keep (Snowball)
    ann_profit = (monthly_rent - (monthly_p_i + monthly_escrow) - maint_util) * 12
    snowball = ann_profit - (c_heloc * heloc_rate)
    # HVAC Trap: If not paid off by Year 2 and checkbox is FALSE, add penalty
    if yr == 2 and not hvac_on_time and c_hvac > 0:
        c_hvac += 3500  # Estimated back-interest penalty
    
    if c_heloc > snowball: c_heloc -= snowball
    else:
        rem = snowball - c_heloc
        c_heloc = 0
        if c_hvac > rem: c_hvac -= rem
        else:
            c_accum_keep += (rem - c_hvac)
            c_hvac = 0
    c_prop *= 1.03
    c_mort -= (actual_principal * 12)

# --- UI DISPLAY ---
st.title("The 'Freedom' Dashboard")
st.write(f"### Cash Seed: **${final_seed:,.2f}** | Debt Wiped: **${all_debts:,.2f}**")

df = pd.DataFrame(data)
st.plotly_chart(px.line(df, x="Year", y=["Sell (Passive)", "Keep (Active)"], 
              color_discrete_map={"Sell (Passive)": "#00d1b2", "Keep (Active)": "#ff3860"}), use_container_width=True)

# --- LIFE METRICS ---
st.header("🏂 The Life Value of your Decision")
diff = data[-1]["Sell (Passive)"] - data[-1]["Keep (Active)"]
total_hours_saved = hours_mo * 12 * projection_years
trips_funded = diff / 2500 

l1, l2, l3 = st.columns(3)
l1.metric("Total Time Saved", f"{total_hours_saved:,} Hours")
l2.metric("Extra Snowboard Trips", f"{int(trips_funded)} Trips")
l3.metric("Monthly Raise", f"${monthly_invest:,.2f}")

# --- RISK METER ---
st.header("⚠️ The Risk Meter (Stress Test)")
r1, r2 = st.columns(2)
with r1:
    st.subheader("The Rental Nightmare")
    eviction = st.slider("Vacancy/Damages ($)", 0, 15000, 7500)
    st.warning(f"A bad tenant year costs you **${eviction:,.2f}** and dozens of hours of stress.")

with r2:
    st.subheader("The Market Correction")
    bear = st.slider("S&P 500 returns only 7%?", 5.0, 10.0, 7.0) / 100
    # Future Value Formula: FV = P(1+r)^t + c[((1+r)^t - 1) / r]
    fv_seed = final_seed * (1 + bear)**projection_years
    fv_contrib = (monthly_invest * 12) * (((1 + bear)**projection_years - 1) / bear)
    st.error(f"In a bear market, 'Sell' path still ends at **${(fv_seed + fv_contrib + keep_cash_buffer):,.2f}**.")