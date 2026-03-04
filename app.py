import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. INCOME & PAYCHECK (From Stub)
# ==========================================
[span_0](start_span)MONTHLY_GROSS = 5447.87[span_0](end_span)
[span_1](start_span)[span_2](start_span)MANDATORY_DEDUCTIONS = 1644.63[span_1](end_span)[span_2](end_span)
[span_3](start_span)TSP_LOAN_PAYMENT = 469.89[span_3](end_span)
[span_4](start_span)[span_5](start_span)TSP_CONTRIBUTION = 272.39[span_4](end_span)[span_5](end_span)

# ==========================================
# 2. THE RENTAL (KEEP SCENARIO)
# ==========================================
# Loan Details
MORTGAGE_BALANCE = 143000.00
MORTGAGE_RATE = 0.0325

# Monthly Cash Flow (Placeholders)
# This is what you actually pay out of pocket each month
MONTHLY_PRINCIPAL_PAYMENT = 0.00  # Wealth builder
MONTHLY_INTEREST_PAYMENT = 0.00   # Bank profit (The "Burn")
MONTHLY_PROPERTY_TAX = 0.00       # Escrow Part A
MONTHLY_INSURANCE = 0.00          # Escrow Part B

# Income & Maintenance
MONTHLY_RENT_INCOME = 22300
MONTHLY_MAINTENANCE_RESERVE = 740.00 # Your ~$8,800/year "burn"

# ==========================================
# 3. THE DEBT MONSTERS
# ==========================================
HELOC_BALANCE = 40000.00
HELOC_PAYMENT = 591.00 

HVAC_BALANCE = 9000.00
HVAC_PAYMENT = 0.00 # Your current monthly payment
