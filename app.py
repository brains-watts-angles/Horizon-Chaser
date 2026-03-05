import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 0. GLOBAL CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.title("🎮 Simulator Controls")

st.sidebar.header("🏠 Property & Market")
ESTIMATED_HOUSE_VALUE = st.sidebar.slider("Current House Value ($)", 250000, 500000, 350000, 5000)
ANNUAL_APPRECIATION_RATE = st.sidebar.slider("Annual Appreciation (%)", 0, 10, 3) / 100
MONTHLY_RENT_INCOME = st.sidebar.slider("Monthly Rent ($)", 1500, 3500, 2300, 50)
ANNUAL_RENT_INCREASE = 0.02 
INFLATION_RATE = 0.03

st.sidebar.header("💳 Debt & PITI")
MORTGAGE_BALANCE = st.sidebar.number_input("Mortgage Balance ($)", value=143000.0)
MORTGAGE_RATE = st.sidebar.number_input("Mortgage Interest Rate (%)", value=3.25) / 100
STARTING_MONTHLY_PRINCIPAL = st.sidebar.number_input("Monthly Principal ($)", value=350.0)
STARTING_MONTHLY_INTEREST = st.sidebar.number_input("Monthly Interest ($)", value=380.0)
STARTING_MONTHLY_TAX = st.sidebar.number_input("Monthly Tax ($)", value=250.0)
STARTING_MONTHLY_INSURANCE = st.sidebar.number_input("Monthly Insurance ($)", value=120.0)

HELOC_BALANCE = st.sidebar.number_input("HELOC Balance ($)", value=40000.0)
HELOC_ANNUAL_RATE = 0.0825 # [cite: 2026-03-04]
HELOC_MONTHLY_PAYMENT = 591.00 

st.sidebar.header("📈 Market & Tax Trends")
SP500_ANNUAL_RETURN = st.sidebar.slider("S&P 500 Annual Return (%)", 1, 15, 10) / 100
ANNUAL_TAX_INCREASE = st.sidebar.slider("Annual Property Tax Increase (%)", 0, 10, 3) / 100

# ==========================================
# 1. FIXED DATA (FROM YOUR RECORDS)
# ==========================================
MONTHLY_GROSS = 5447.87
MANDATORY_DEDUCTIONS = 1644.63
TSP_LOAN_PAYMENT = 469.89
TSP_LOAN_BALANCE = 16000
HOURLY_RATE = 31.43 # Your pay stub rate [cite: 2026-02-24]

HVAC_BALANCE = 9000.00
HVAC_MONTHLY_PAYMENT = 0.00
FURNISHMENTS = 6000.00
MONTHLY_MAINTENANCE_RESERVE = 740.00

TRIPS_PER_YEAR = 4 # [cite: 2026-03-04]
MILES_ROUND_TRIP = 500 # [cite: 2026-03-04]
IRS_MILEAGE_RATE = 0.67
LODGING_PER_TRIP = 150.00
MEALS_PER_TRIP = 50.00
DRIVE_TIME_PER_TRIP = 12.0 # [cite: 2026-03-04]
LABOR_TIME_PER_TRIP = 10.0 # [cite: 2026-03-04]
ADMIN_TIME_PER_MONTH = 3.0 # [cite: 2026-03-04]

# ==========================================
# 2. LOGIC: INTERMEDIATE CALCULATIONS
# ==========================================
TOTAL_MONTHLY_PITI_PAYMENT = STARTING_MONTHLY_PRINCIPAL + STARTING_MONTHLY_INTEREST + STARTING_MONTHLY_TAX + STARTING_MONTHLY_INSURANCE

ANNUAL_TRAVEL_COST = ((MILES_ROUND_TRIP * IRS_MILEAGE_RATE) + LODGING_PER_TRIP + MEALS_PER_TRIP) * TRIPS_PER_YEAR
MONTHLY_TRAVEL_BURDEN = ANNUAL_TRAVEL_COST / 12
TOTAL_MONTHLY_RENTAL_LABOR_HOURS = ((DRIVE_TIME_PER_TRIP + LABOR_TIME_PER_TRIP) * TRIPS_PER_YEAR / 12) + ADMIN_TIME_PER_MONTH # [cite: 2026-03-04]
monthly_labor_value = TOTAL_MONTHLY_RENTAL_LABOR_HOURS * HOURLY_RATE

net_sales_price = ESTIMATED_HOUSE_VALUE * 0.92
total_tax_hit = ((net_sales_price - 184500 - 70000) * 0.15) + (70000 * 0.25)
final_sp500_seed = net_sales_price - MORTGAGE_BALANCE - HELOC_BALANCE - HVAC_BALANCE - FURNISHMENTS - TSP_LOAN_BALANCE - total_tax_hit - 20000

# --- THE REALITY CHECK LOGIC ---

# 1. Total Monthly Outflow (Cash leaving your pocket)
total_monthly_outflow = (
    MANDATORY_DEDUCTIONS + 
    TSP_LOAN_PAYMENT + 
    HELOC_MONTHLY_PAYMENT + 
    HVAC_MONTHLY_PAYMENT + 
    TOTAL_MONTHLY_PITI_PAYMENT + 
    MONTHLY_MAINTENANCE_RESERVE + 
    MONTHLY_TRAVEL_BURDEN
)

# 2. Cash-in-Pocket (Liquid Cash)
# This is what you actually FEEL in Salmon [cite: 2026-03-04]
cash_in_pocket_keep = (MONTHLY_GROSS + MONTHLY_RENT_INCOME) - total_monthly_outflow
cash_in_pocket_sell = (MONTHLY_GROSS - MANDATORY_DEDUCTIONS - 1800.00 - 250.00 - 200.00)

# 3. The "Honest" Landlord Wage (Cash Profit / Labor Hours)
# This removes the "Equity" smoke and mirrors
cash_profit_gap = cash_in_pocket_keep - cash_in_pocket_sell
landlord_hourly_wage_cash = cash_profit_gap / max(0.01, TOTAL_MONTHLY_RENTAL_LABOR_HOURS)

# ==========================================
# 3. THE 20-YEAR SIMULATION ENGINE
# ==========================================
years = 20
months = years * 12
data = []

# Initial Simulation States
current_sp500_balance = final_sp500_seed
running_mortgage_balance = MORTGAGE_BALANCE
running_heloc_balance = HELOC_BALANCE
running_monthly_tax = STARTING_MONTHLY_TAX
running_monthly_insurance = STARTING_MONTHLY_INSURANCE
running_monthly_maintenance = MONTHLY_MAINTENANCE_RESERVE
monthly_p_and_i = STARTING_MONTHLY_PRINCIPAL + STARTING_MONTHLY_INTEREST
payoff_year = None

for month in range(1, months + 1):
    # --- 1. S&P 500 GROWTH ---
    current_sp500_balance *= (1 + SP500_ANNUAL_RETURN)**(1/12)
    current_sp500_balance += 500.00 
    
    # --- 2. ANNUAL COST CREEP ---
    if month % 12 == 0:
        running_monthly_tax *= (1 + ANNUAL_TAX_INCREASE)
        running_monthly_insurance *= (1 + INFLATION_RATE)
        running_monthly_maintenance *= (1 + INFLATION_RATE)

    # --- 3. AMORTIZATION (Mortgage & HELOC) ---
    # Mortgage 3.25%
    m_interest = running_mortgage_balance * (MORTGAGE_RATE / 12)
    m_principal = monthly_p_and_i - m_interest
    running_mortgage_balance = max(0, running_mortgage_balance - m_principal)
    
    # HELOC 8.25%
    h_interest = running_heloc_balance * (HELOC_ANNUAL_RATE / 12)
    h_principal = HELOC_MONTHLY_PAYMENT - h_interest
    running_heloc_balance = max(0, running_heloc_balance - h_principal)
    
    # Tracking Payoff
    if running_mortgage_balance <= 0 and payoff_year is None:
        payoff_year = month / 12

    # --- 4. ASSET EQUITY ---
    house_value = ESTIMATED_HOUSE_VALUE * (1 + ANNUAL_APPRECIATION_RATE)**(month/12)
    current_house_equity = house_value - running_mortgage_balance - running_heloc_balance

    data.append({
        "Year": month / 12, 
        "Sell Scenario (S&P 500)": current_sp500_balance, 
        "Keep Scenario (Home Equity)": current_house_equity
    })

df_sim = pd.DataFrame(data)

# ==========================================
# 4. DASHBOARD DISPLAY
# ==========================================
st.title("The Sanity Simulator: Salmon to Boise")
# Replace your current col1, col2, col3 with this:
st.title("The Sanity Simulator: Salmon to Boise")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("S&P 500 Seed", f"${final_sp500_seed:,.2f}")

with col2:
    # This now shows actual spendable cash difference
    st.metric(
        "Monthly Cash-in-Pocket Gap", 
        f"${cash_profit_gap:,.2f}",
        help="How much more (or less) spendable cash you have each month by keeping the rental."
    )

with col3:
    # This is the 'Honest' wage
    st.metric(
        "Cash-Based Landlord Wage", 
        f"${landlord_hourly_wage_cash:,.2f}/hr", 
        delta=f"{landlord_hourly_wage_cash - HOURLY_RATE:,.2f} vs Job",
        help="Your hourly rate based ONLY on spendable cash, not home equity."
    )

if payoff_year: st.success(f"🏠 Mortgage Free in {payoff_year:.1f} years.")

st.subheader("Total Wealth Projection: 20 Years")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_sim['Year'], y=df_sim['Sell Scenario (S&P 500)'], mode='lines', name='Sell & Invest', line=dict(color='#00FF00', width=4)))
fig.add_trace(go.Scatter(x=df_sim['Year'], y=df_sim['Keep Scenario (Home Equity)'], mode='lines', name='Keep Rental', line=dict(color='#0000FF', width=4)))
fig.update_layout(xaxis_title="Years", yaxis_title="Total Wealth ($)", hovermode="x unified", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Future Outlook
year_20_rent = MONTHLY_RENT_INCOME * (1.02**20)
year_20_net = year_20_rent - running_monthly_tax - running_monthly_insurance - running_monthly_maintenance
st.metric("Estimated Monthly Net (Year 20)", f"${year_20_net:,.2f}")

# Cash in Pocket (The "Feel Good" Number)
monthly_cash_in_pocket = (
    MONTHLY_RENT_INCOME 
    - TOTAL_MONTHLY_PITI_PAYMENT 
    - HELOC_MONTHLY_PAYMENT 
    - MONTHLY_MAINTENANCE_RESERVE 
    - MONTHLY_TRAVEL_BURDEN
)

st.metric("Actual Cash-in-Pocket", f"${monthly_cash_in_pocket:,.2f}", help="This is the actual liquid cash left over each month after ALL bills and reserves are paid.")
