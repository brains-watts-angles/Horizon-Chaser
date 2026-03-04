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

# Market Growth and Equity
ESTIMATED_HOUSE_VALUE = 350000.00
ANNUAL_APPRECIATION_RATE = 0.03 # 3% growth in home value

# Income & Maintenance
MONTHLY_RENT_INCOME = 2300.00
ANNUAL_RENT_INCREASE = 0.02     # 2% growth in rent prices

# Expenses
MONTHLY_MAINTENANCE_RESERVE = 740.00 # Your ~$8,800/year "burn"

# The "Life" Cost
MONTHLY_RENTAL_LABOR_HOURS = 10.0 # Time spent on property/tenants
HOURLY_RATE = 31.43              # From your pay stub

# ==========================================
# 3. THE DEBT MONSTERS
# ==========================================

# Mortgage Details
MORTGAGE_BALANCE = 143000.00
MORTGAGE_RATE = 0.0325

# HELOC: High interest
HELOC_BALANCE = 40000.00
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
SELLING_COSTS_PERCENT = 0.08  # 8% for Realtor fees, repairs to sell, etc.
closing_costs = ESTIMATED_HOUSE_VALUE * SELLING_COSTS_PERCENT
net_sales_price = ESTIMATED_HOUSE_VALUE - closing_costs

# 2. Taxable Gain Calculation
# You only pay Capital Gains on the PROFIT, not the whole check
TAX_ON_PROFIT_PERCENT = 0.15  # 0% if you've lived there 2 of last 5 years
ORIGINAL_PURCHASE_PRICE = 200000.00 # Placeholder: What you bought it for
total_gain = net_sales_price - ORIGINAL_PURCHASE_PRICE

# 3. The Tax Hit
# Depreciation Recapture is a "catch-up" tax on what you've claimed over the years
depreciation_tax = ESTIMATED_DEPRECIATION_RECAPTURE * 0.25
capital_gains_tax = total_gain * TAX_ON_PROFIT_PERCENT
total_tax_hit = depreciation_tax + capital_gains_tax

# 4. Debt Clearance
# This is where we kill the monsters to find the "Raw Cash" left
raw_cash_remaining = (
    net_sales_price 
    - MORTGAGE_BALANCE 
    - HELOC_BALANCE 
    - HVAC_BALANCE 
    - FURNISHMENTS 
    - total_tax_hit
)

# 5. The "Life" Reserves
# Money for the river raft and the emergency fund
CASH_TO_KEEP_ON_HAND = 20000.00 # Placeholder

# 6. THE FINAL SEED
# This is the number that actually goes into the S&P 500
final_sp500_seed = raw_cash_remaining - CASH_TO_KEEP_ON_HAND


# ==========================================
# 7. LOGIC: MONTHLY CASH FLOW (NET TAKE-HOME)
# ==========================================

# Scenario A: The "Status Quo" (Keep)
# We calculate what actually hits your pocket after ALL house and debt costs
current_monthly_net = (
    MONTHLY_GROSS 
    - MANDATORY_DEDUCTIONS 
    - TSP_LOAN_PAYMENT 
    - HELOC_MONTHLY_PAYMENT
    - HVAC_MONTHLY_PAYMENT
    - MORTGAGE_PITI           # Placeholder for P+I+T+I
    - MONTHLY_MAINTENANCE_RESERVE
    + MONTHLY_RENT_INCOME
)

# Scenario B: The "Independent" (Sell)
# No more rental income, but no more debt or house costs
# You pay your own rent and utilities now
independent_monthly_net = (
    MONTHLY_GROSS 
    - MANDATORY_DEDUCTIONS 
    - INDEPENDENCE_RENT_ESTIMATE 
    - INDEPENDENCE_UTILITIES 
    - INDEPENDENCE_FOOD_SURPLUS
)


####Sample code below this line####




# ==========================================
# 8. LOGIC: TAXES & DEPRECIATION RECAPTURE
# ==========================================

