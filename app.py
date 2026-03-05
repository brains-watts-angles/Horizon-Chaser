import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 0. GLOBAL CONTROLS (SIDEBAR)
# ==========================================
st.sidebar.title("🎮 Simulator Controls")

st.sidebar.header("🏠 Property & Market")
ESTIMATED_HOUSE_VALUE = st.sidebar.slider("Current House Value ($)", 250000, 600000, 350000, 5000)
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
HELOC_ANNUAL_RATE = 0.0825
HELOC_MONTHLY_PAYMENT = st.sidebar.number_input("HELOC Monthly Payment ($)", value=591.0)

st.sidebar.header("📈 Market & Tax Trends")
SP500_ANNUAL_RETURN = st.sidebar.slider("S&P 500 Annual Return (%)", 1, 15, 10) / 100
ANNUAL_TAX_INCREASE = st.sidebar.slider("Annual Property Tax Increase (%)", 0, 10, 3) / 100

# ==========================================
# 1. FIXED DATA (RECORDS & LOGISTICS)
# ==========================================
MONTHLY_GROSS = 5447.87 #
MANDATORY_DEDUCTIONS = 1644.63
TSP_LOAN_PAYMENT = 469.89
TSP_LOAN_BALANCE = 16000
HOURLY_RATE = 31.43 #

HVAC_BALANCE = 9000.00
HVAC_MONTHLY_PAYMENT = 0.00
FURNISHMENTS = 6000.00
MONTHLY_MAINTENANCE_RESERVE = 740.00 #

# Travel & Labor Logistics
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

# Annual & Monthly Travel Burden
ANNUAL_TRAVEL_COST = ((MILES_ROUND_TRIP * IRS_MILEAGE_RATE) + LODGING_PER_TRIP + MEALS_PER_TRIP) * TRIPS_PER_YEAR
MONTHLY_TRAVEL_BURDEN = ANNUAL_TRAVEL_COST / 12

# Monthly Labor Value (The cost of your creative time)
TOTAL_MONTHLY_RENTAL_LABOR_HOURS = ((DRIVE_TIME_PER_TRIP + LABOR_TIME_PER_TRIP) * TRIPS_PER_YEAR / 12) + ADMIN_TIME_PER_MONTH
monthly_labor_value = TOTAL_MONTHLY_RENTAL_LABOR_HOURS * HOURLY_RATE

# Sell Waterfall (One-time liquidity event)
net_sales_price = ESTIMATED_HOUSE_VALUE * 0.92
total_profit = net_sales_price - 184500
cap_gains_portion = max(0, total_profit - 70000)
total_tax_hit = (70000 * 0.25) + (cap_gains_portion * 0.15)
final_sp500_seed = net_sales_price - MORTGAGE_BALANCE - HELOC_BALANCE - HVAC_BALANCE - FURN
