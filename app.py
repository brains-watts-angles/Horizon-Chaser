import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go



# ==========================================
# 1. INCOME & PAYCHECK
# ==========================================
MONTHLY_GROSS = 5447.87
MANDATORY_DEDUCTIONS = 1644.63
TSP_LOAN_PAYMENT = 469.89
TSP_CONTRIBUTION = 272.39

# ==========================================
# 2. THE RENTAL (KEEP SCENARIO)
# ==========================================

st.sidebar.header("🏠 Rental Property Settings")
# Market Growth and Equity
ESTIMATED_HOUSE_VALUE = st.sidebar.slider(
    "Current House Value ($)", 
    min_value=250000, max_value=500000, value=350000, step=5000
)
ANNUAL_APPRECIATION_RATE = 0.03 # 3% growth in home value

# Income & Maintenance
MONTHLY_RENT_INCOME = st.sidebar.slider(
    "Monthly Rent ($)", 
    min_value=1500, max_value=3500, value=2300, step=50
)
ANNUAL_RENT_INCREASE = 0.02     # 2% growth in rent prices

# Expenses
MONTHLY_MAINTENANCE_RESERVE = 740.00 # Your ~$8,800/year "burn"

# The "Life" Cost
HOURLY_RATE = 31.43              # From your pay stub

# Travel Logistics
TRIPS_PER_YEAR = 4               
MILES_ROUND_TRIP = 500           
IRS_MILEAGE_RATE = 0.67          
LODGING_PER_TRIP = 150.00        
MEALS_PER_TRIP = 50.00           

# Calculate Monthly Money Drain
ANNUAL_TRAVEL_COST = ((MILES_ROUND_TRIP * IRS_MILEAGE_RATE) + LODGING_PER_TRIP + MEALS_PER_TRIP) * TRIPS_PER_YEAR
MONTHLY_TRAVEL_BURDEN = ANNUAL_TRAVEL_COST / 12

# Calculate Monthly Time Drain
DRIVE_TIME_PER_TRIP = 12.0
LABOR_TIME_PER_TRIP = 10.0  # Weekend warrior hours
ADMIN_TIME_PER_MONTH = 3.0  # Phone calls, bills, etc.

TOTAL_MONTHLY_RENTAL_LABOR_HOURS = ((DRIVE_TIME_PER_TRIP + LABOR_TIME_PER_TRIP) * TRIPS_PER_YEAR / 12) + ADMIN_TIME_PER_MONTH


# ==========================================
# 3. THE DEBT MONSTERS
# ==========================================

# Mortgage Details
MORTGAGE_BALANCE = 143000.00
MORTGAGE_RATE = 0.0325

# Starting PITI Breakdown (Found on your statement)
# Separating these allows us to track 'Asset Growth' vs 'Pure Expense'
st.sidebar.header("💳 Debt & PITI")
STARTING_MONTHLY_PRINCIPAL = st.sidebar.number_input("Monthly Principal ($)", value=350.0)
STARTING_MONTHLY_INTEREST = st.sidebar.number_input("Monthly Interest ($)", value=380.0)
STARTING_MONTHLY_TAX = st.sidebar.number_input("Monthly Tax ($)", value=250.0)
STARTING_MONTHLY_INSURANCE = st.sidebar.number_input("Monthly Insurance ($)", value=120.0)

# Derived Variable for the Monthly Budget
TOTAL_MONTHLY_PITI_PAYMENT = (
    STARTING_MONTHLY_PRINCIPAL + 
    STARTING_MONTHLY_INTEREST + 
    STARTING_MONTHLY_TAX + 
    STARTING_MONTHLY_INSURANCE
)

# The Logic will derive the 'Principal & Interest' portion:
# STARTING_P_AND_I = TOTAL_MONTHLY_PITI_PAYMENT - STARTING_MONTHLY_TAX - STARTING_MONTHLY_INSURANCE


# HELOC: High interest
HELOC_BALANCE = st.sidebar.number_input("HELOC Balance ($)", value=40000.0)
HELOC_ANNUAL_RATE = 0.0825      # placeholder for ~8%
HELOC_MONTHLY_PAYMENT = 591.00 

# HVAC: The interest "bomb" timer
HVAC_BALANCE = 9000.00
HVAC_ANNUAL_RATE = 0.00       # 0% for now? 
HVAC_MONTHLY_PAYMENT = 0.00   # Your current "interest-dodge" payment

# TSP Loan
TSP_LOAN_BALANCE = 16000

#Sister Debt
FURNISHMENTS = 6000 #TBD Awaiting Furnishing Appraisal

# ==========================================
# 4. THE INDEPENDENT FUTURE (Scenario Targets)
# ==========================================

# Independence Costs (The "Sanity Move")
INDEPENDENCE_RENT_ESTIMATE = 1800.00
INDEPENDENCE_UTILITIES = 250.00
INDEPENDENCE_FOOD_SURPLUS = 200.00 # Extra cost vs living with parents
INFLATION_RATE = 0.03         # 3% for cost of living increases

#Investments and Opportunities
MONTHLY_SP500_GOAL = 500.00
SP500_ANNUAL_RETURN = 0.10    # 10% historical average

# ==========================================
# 5. LOGIC: THE "SELL" DAY WATERFALL
# ==========================================

# 1. The Immediate "Haircut"
SELLING_COSTS_PERCENT = 0.08  
closing_costs = ESTIMATED_HOUSE_VALUE * SELLING_COSTS_PERCENT
net_sales_price = ESTIMATED_HOUSE_VALUE - closing_costs

# 2. Taxable Gain Calculation
TAX_ON_PROFIT_PERCENT = 0.15  
ORIGINAL_PURCHASE_PRICE = 184500 
ESTIMATED_DEPRECIATION_RECAPTURE = 70000

# Step A: Calculate the 'Total Profit'
total_profit = net_sales_price - ORIGINAL_PURCHASE_PRICE

# Step B: Split the profit into the two tax buckets
# We subtract recapture from profit so we don't double-tax those dollars
capital_gains_portion = max(0, total_profit - ESTIMATED_DEPRECIATION_RECAPTURE)

# 3. The Tax Hit
depreciation_tax = ESTIMATED_DEPRECIATION_RECAPTURE * 0.25
capital_gains_tax = capital_gains_portion * TAX_ON_PROFIT_PERCENT
total_tax_hit = depreciation_tax + capital_gains_tax

# 4. Debt Clearance
raw_cash_remaining = (
    net_sales_price 
    - MORTGAGE_BALANCE 
    - HELOC_BALANCE 
    - HVAC_BALANCE 
    - FURNISHMENTS 
    - TSP_LOAN_BALANCE
    - total_tax_hit
)

# 5. The "Life" Reserves (Raft, Emergency, etc.)
CASH_TO_KEEP_ON_HAND = 20000.00 

# 6. THE FINAL SEED for S&P 500
final_sp500_seed = raw_cash_remaining - CASH_TO_KEEP_ON_HAND

# ==========================================
# 6. LOGIC: MONTHLY CASH FLOW (NET TAKE-HOME)
# ==========================================

# Step 1: Calculate the 'Labor Cost' in dollars
# This translates your weekend warrior time into a dollar amount
monthly_labor_value = TOTAL_MONTHLY_RENTAL_LABOR_HOURS * HOURLY_RATE

# Scenario A: The "Status Quo" (Keep)
# We subtract the cash out AND the value of your time
current_monthly_net = (
    MONTHLY_GROSS 
    - MANDATORY_DEDUCTIONS 
    - TSP_LOAN_PAYMENT 
    - HELOC_MONTHLY_PAYMENT
    - HVAC_MONTHLY_PAYMENT
    - TOTAL_MONTHLY_PITI_PAYMENT 
    - MONTHLY_MAINTENANCE_RESERVE
    - MONTHLY_TRAVEL_BURDEN
    - monthly_labor_value         # <--- The "Time Tax"
    + MONTHLY_RENT_INCOME
)

# Scenario B: The "Independent" (Sell)
# No labor value subtracted here because your time is now YOURS
independent_monthly_net = (
    MONTHLY_GROSS 
    - MANDATORY_DEDUCTIONS 
    - INDEPENDENCE_RENT_ESTIMATE 
    - INDEPENDENCE_UTILITIES 
    - INDEPENDENCE_FOOD_SURPLUS
)

# ==========================================
# 7. LOGIC: THE "SANITY" METRIC (HOURLY LANDLORD WAGE)
# ==========================================

# Step 1: Calculate the 'Take-Home' gap
# This is how much MORE (or less) you make by keeping the rental vs. selling it
monthly_profit_gap = current_monthly_net - independent_monthly_net

# Step 2: Calculate your Landlord Hourly Wage
# Using the new total hours including the drive from Salmon
landlord_hourly_wage = monthly_profit_gap / max(0.01, TOTAL_MONTHLY_RENTAL_LABOR_HOURS)

# ==========================================
# MAIN DASHBOARD DISPLAY
# ==========================================
st.title("The Sanity Simulator: Salmon to Boise")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="S&P 500 Starting Seed", 
        value=f"${final_sp500_seed:,.2f}"
    )

with col2:
    # We calculate the delta (the difference) between Scenarios
    gap = current_monthly_net - independent_monthly_net
    st.metric(
        label="Monthly Net Gap", 
        value=f"${gap:,.2f}",
        delta=f"${gap:,.2f}"
    )

with col3:
    st.metric(
        label="Landlord Hourly Wage", 
        value=f"${landlord_hourly_wage:,.2f}/hr",
        delta=f"{landlord_hourly_wage - HOURLY_RATE:,.2f} vs Job",
        delta_color="normal"
    )
