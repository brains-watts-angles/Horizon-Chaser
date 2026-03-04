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
# 5. SALE MECHANICS (FOR SEED CALCULATION)
# ==========================================
SELLING_COSTS_PERCENT = 0.08  # 8% for Realtor fees, repairs to sell, etc.
TAX_ON_PROFIT_PERCENT = 0.15  # 0% if you've lived there 2 of last 5 years

# ==========================================
# 6. LOGIC: THE "SELL" DAY CALCULATION
# ==========================================

# 1. Calculate the 'Haircut' (Selling costs)
closing_costs = ESTIMATED_SALE_PRICE * SELLING_COSTS_PERCENT

# 2. Calculate the Net Profit
# This clears every single debt monster in one shot
net_proceeds = (
    ESTIMATED_SALE_PRICE 
    - closing_costs 
    - MORTGAGE_BALANCE 
    - HELOC_BALANCE 
    - HVAC_BALANCE
    - FURNISHMENTS
)
# This 'net_proceeds' is your S&P 500 Starting Seed!


####Sample code below this line####









