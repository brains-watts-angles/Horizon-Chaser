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

# Debt items not in sidebar
HVAC_BALANCE = 9000.00
HVAC_MONTHLY_PAYMENT = 0.00
FURNISHMENTS = 6000.00
MONTHLY_MAINTENANCE_RESERVE = 740.00

# Travel Logistics (Salmon to Boise) [cite: 2026-03-04]
TRIPS_PER_YEAR = 4
MILES_ROUND_TRIP = 500
IRS_MILEAGE_RATE = 0.67
LODGING_PER_TRIP = 150.00
MEALS_PER_TRIP = 50.00
DRIVE_TIME_PER_TRIP = 12.0
LABOR_TIME_PER_TRIP = 10.0
ADMIN_TIME_PER_MONTH = 3.0

# ==========================================
# 2. LOGIC: INTERMEDIATE CALCULATIONS
# ==========================================
TOTAL_MONTHLY_PITI_PAYMENT = STARTING_MONTHLY_PRINCIPAL + STARTING_MONTHLY_INTEREST + STARTING_MONTHLY_TAX + STARTING_MONTHLY_INSURANCE

# Travel & Labor Costs
ANNUAL_TRAVEL_COST = ((MILES_ROUND_TRIP * IRS_MILEAGE_RATE) + LODGING_PER_TRIP + MEALS_PER_TRIP) * TRIPS_PER_YEAR
MONTHLY_TRAVEL_BURDEN = ANNUAL_TRAVEL_COST / 12
TOTAL_MONTHLY_RENTAL_LABOR_HOURS = ((DRIVE_TIME_PER_TRIP + LABOR_TIME_PER_TRIP) * TRIPS_PER_YEAR / 12) + ADMIN_TIME_PER_MONTH
monthly_labor_value = TOTAL_MONTHLY_RENTAL_LABOR_HOURS * HOURLY_RATE

# Sell Waterfall Logic
SELLING_COSTS_PERCENT = 0.08
net_sales_price = ESTIMATED_HOUSE_VALUE * (1 - SELLING_COSTS_PERCENT)
total_profit = net_sales_price - 184500 # Original Purchase Price
cap_gains_portion = max(0, total_profit - 70000) # Depreciation Recapture adjustment
total_tax_hit = (70000 * 0.25) + (cap_gains_portion * 0.15)
final_sp500_seed = net_sales_price - MORTGAGE_BALANCE - HELOC_BALANCE - HVAC_BALANCE - FURNISHMENTS - TSP_LOAN_BALANCE - total_tax_hit - 20000 # $20k Raft Fund

# Monthly Net Scenarios
current_monthly_net = (MONTHLY_GROSS - MANDATORY_DEDUCTIONS - TSP_LOAN_PAYMENT - HELOC_MONTHLY_PAYMENT - HVAC_MONTHLY_PAYMENT - TOTAL_MONTHLY_PITI_PAYMENT - MONTHLY_MAINTENANCE_RESERVE - MONTHLY_TRAVEL_BURDEN - monthly_labor_value + MONTHLY_RENT_INCOME)
independent_monthly_net = (MONTHLY_GROSS - MANDATORY_DEDUCTIONS - 1800.00 - 250.00 - 200.00) # Rent, Utils, Food
landlord_hourly_wage = (current_monthly_net - independent_monthly_net) / max(0.01, TOTAL_MONTHLY_RENTAL_LABOR_HOURS)

# ==========================================
# 3. THE 20-YEAR SIMULATION ENGINE
# ==========================================
years = 20
months = years * 12
data = []
current_sp500_balance = final_sp500_seed
running_mortgage_balance = MORTGAGE_BALANCE
running_monthly_tax = STARTING_MONTHLY_TAX
monthly_p_and_i = STARTING_MONTHLY_PRINCIPAL + STARTING_MONTHLY_INTEREST
payoff_year = None

for month in range(1, months + 1):
    # Grow S&P 500
    current_sp500_balance *= (1 + SP500_ANNUAL_RETURN)**(1/12)
    current_sp500_balance += 500.00 # Monthly S&P Goal
    
    # Update Tax Creep
    if month % 12 == 0: running_monthly_tax *= (1 + ANNUAL_TAX_INCREASE)

    # Amortization
    interest_this_month = running_mortgage_balance * (MORTGAGE_RATE / 12)
    principal_this_month = monthly_p_and_i - interest_this_month
    running_mortgage_balance = max(0, running_mortgage_balance - principal_this_month)
    
    if running_mortgage_balance <= 0 and payoff_year is None: payoff_year = month / 12

    house_value = ESTIMATED_HOUSE_VALUE * (1 + ANNUAL_APPRECIATION_RATE)**(month/12)
    current_house_equity = house_value - running_mortgage_balance

    # Inside your 'for month in range(1, months + 1):' loop:

# 1. HELOC Amortization (New!)
heloc_interest = running_heloc_balance * (HELOC_ANNUAL_RATE / 12)
heloc_principal = HELOC_MONTHLY_PAYMENT - heloc_interest
running_heloc_balance = max(0, running_heloc_balance - heloc_principal)

# 2. Insurance & Maintenance Creep (New!)
# We inflate these by the 3% inflation rate every year
if month % 12 == 0:
    running_monthly_insurance *= (1 + INFLATION_RATE)
    running_monthly_maintenance *= (1 + INFLATION_RATE)

# 3. Updated Total Equity Calculation
# Equity = House Value - Mortgage Balance - HELOC Balance
current_house_equity = house_value - running_mortgage_balance - running_heloc_balance
    
    data.append({"Year": month / 12, "Sell Scenario (S&P 500)": current_sp500_balance, "Keep Scenario (Home Equity)": current_house_equity})

df_sim = pd.DataFrame(data)

# ==========================================
# 4. DASHBOARD DISPLAY
# ==========================================
st.title("The Sanity Simulator: Salmon to Boise")
col1, col2, col3 = st.columns(3)
col1.metric("S&P 500 Seed", f"${final_sp500_seed:,.2f}")
col2.metric("Monthly Net Gap", f"${(current_monthly_net - independent_monthly_net):,.2f}")
col3.metric("Landlord Hourly Wage", f"${landlord_hourly_wage:,.2f}/hr", delta=f"{landlord_hourly_wage - HOURLY_RATE:,.2f} vs Job")

if payoff_year: st.success(f"🏠 Mortgage Free in {payoff_year:.1f} years.")

st.subheader("Total Wealth Projection: 20 Years")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_sim['Year'], y=df_sim['Sell Scenario (S&P 500)'], mode='lines', name='Sell & Invest', line=dict(color='#00FF00', width=4)))
fig.add_trace(go.Scatter(x=df_sim['Year'], y=df_sim['Keep Scenario (Home Equity)'], mode='lines', name='Keep Rental', line=dict(color='#0000FF', width=4)))
fig.update_layout(xaxis_title="Years", yaxis_title="Total Wealth ($)", hovermode="x unified", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Future Outlook
year_20_rent = MONTHLY_RENT_INCOME * (1.02**20)
year_20_net = year_20_rent - running_monthly_tax - (STARTING_MONTHLY_INSURANCE * (1.03**20)) - (MONTHLY_MAINTENANCE_RESERVE * (1.03**20))
st.metric("Estimated Monthly Net (Year 20)", f"${year_20_net:,.2f}")
