import streamlit as st
import pandas as pd
import numpy as np
import io

# --- BANKING GRADE CALCULATION ENGINE ---
def calculate_home_loan(principal, years, rate_pa):
    if principal <= 0 or years <= 0 or rate_pa <= 0:
        return None
    
    # Monthly interest rate (Diminishing Balance)
    monthly_rate = (rate_pa / 100) / 12
    # Total months
    tenure_months = int(years * 12)
    
    # Standard EMI Formula: [P x R x (1+R)^N]/[(1+R)^N-1]
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    
    # Amortization Schedule (Yearly)
    schedule = []
    remaining_balance = principal
    
    for year in range(1, int(years) + 1):
        opening_balance = remaining_balance
        yearly_interest = 0
        yearly_principal = 0
        
        for month in range(12):
            interest_m = remaining_balance * monthly_rate
            principal_m = emi - interest_m
            remaining_balance -= principal_m
            
            yearly_interest += interest_m
            yearly_principal += principal_m
            
        schedule.append({
            "Year": year,
            "Opening Balance": round(opening_balance),
            "EMI*12": round(emi * 12),
            "Interest paid yearly": round(yearly_interest),
            "Principal paid yearly": round(yearly_principal),
            "Closing Balance": round(max(0, remaining_balance))
        })
        
    return {
        "monthly_emi": round(emi),
        "total_interest": round(total_interest),
        "total_payment": round(total_payment),
        "schedule": schedule
    }

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Home Loan Pro - Calculator", layout="wide")

# High-Clarity Banking CSS Fix
st.markdown("""
    <style>
    /* Force Light Theme Colors for Consistency */
    :root {
        --primary-blue: #1E40AF;
        --text-dark: #111827;
        --label-grey: #374151;
        --bg-white: #FFFFFF;
    }
    
    /* Title Styling - Bold White with Background Color */
    .main-title {
        text-align: center;
        color: #FFFFFF !important;
        background-color: #1A365D; /* Dark Blue matching the theme */
        padding: 20px;
        border-radius: 10px;
        font-weight: 800 !important;
        font-size: 42px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0px;
    }

    /* Input Box Labels Visibility */
    .stNumberInput label, .stSlider label {
        color: var(--label-grey) !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* Fixing Input Box Internal Text & Background */
    .stNumberInput input {
        color: var(--text-dark) !important;
        background-color: var(--bg-white) !important;
        font-weight: bold !important;
    }
    
    /* Input Container Styling */
    .stNumberInput, .stSlider {
        background: #F8FAFC !important;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        margin-bottom: 10px;
    }
    
    /* EMI Display Header (Large Blue Box) */
    .emi-box {
        background-color: #1A365D !important;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
    
    .emi-box h1, .emi-box p {
        color: #FFFFFF !important;
        margin: 0;
    }
    
    /* Result Cards - Optimized for single line */
    .result-card {
        background: #FFFFFF !important;
        padding: 15px 5px;
        border-radius: 10px;
        border-top: 5px solid #1A365D;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .result-card small {
        color: #64748b !important;
        text-transform: uppercase;
        font-weight: 700;
        font-size: 11px;
        margin-bottom: 5px;
    }

    .result-card b {
        color: #1A365D !important;
        font-size: 18px !important; /* Slightly smaller to fit in one line */
        white-space: nowrap; /* Forces text to stay on one line */
    }
    
    /* Action Button Visibility */
    div.stButton > button:first-child {
        background-color: #1E40AF !important;
        color: #FFFFFF !important;
        width: 100%;
        height: 60px;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LAYOUT ---
st.markdown("<h1 class='main-title'>HOME LOAN EMI CALCULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #cbd5e1; margin-bottom: 5px;'>Professional Financial Analysis & Amortization Plan</p>", unsafe_allow_html=True)

# Developer Info & Social Links
st.markdown("<p style='text-align: center; color: #FFFFFF; font-weight: bold; margin-bottom: 10px;'>Developed by: Shamsudeen Abdulla</p>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4, sc5 = st.columns([1, 1, 1, 1, 1])
with sc2:
    st.link_button("💬 WhatsApp", "https://wa.me/qr/IOBUQDQMM2X3D1", use_container_width=True)
with sc4:
    st.link_button("🔵 Facebook", "https://www.facebook.com/shamsudeen.abdulla.2025/", use_container_width=True)

st.write("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    st.markdown("<h3 style='color:#FFFFFF;'>Loan Requirements</h3>", unsafe_allow_html=True)
    p_amount = st.number_input("Loan Amount (₹)", min_value=100000, value=2500000, step=50000)
    st.caption(f"Principal Value: ₹ {p_amount:,}")
    
    tenure_years = st.slider("Tenure (Years)", min_value=1, max_value=30, value=25)
    
    int_rate = st.number_input("Interest Rate (% P.A.)", min_value=1.0, max_value=20.0, value=8.5, step=0.05)
    
    st.write("<br>", unsafe_allow_html=True)
    calculate_btn = st.button("Calculate EMI")

if calculate_btn:
    res = calculate_home_loan(p_amount, tenure_years, int_rate)
    
    if res:
        with col2:
            # Main EMI Result
            st.markdown(f"""
                <div class="emi-box">
                    <p style='font-size: 18px;'>Your Monthly Home Loan EMI</p>
                    <h1 style='font-size: 58px;'>₹ {res['monthly_emi']:,}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Supporting Results - Single line focus
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"<div class='result-card'><small>Principal</small><b>₹ {p_amount:,}</b></div>", unsafe_allow_html=True)
            with r2:
                st.markdown(f"<div class='result-card'><small>Total Interest</small><b>₹ {res['total_interest']:,}</b></div>", unsafe_allow_html=True)
            with r3:
                st.markdown(f"<div class='result-card'><small>Total Payable</small><b>₹ {res['total_payment']:,}</b></div>", unsafe_allow_html=True)

        # --- AMORTIZATION SCHEDULE ---
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FFFFFF;'>Home Loan Amortization Schedule (Yearly)</h3>", unsafe_allow_html=True)
        df_schedule = pd.DataFrame(res['schedule'])
        st.dataframe(df_schedule.style.format("{:,}"), use_container_width=True, hide_index=True)

        # --- EXCEL DOWNLOAD ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Full Report in a single professional sheet
            summary_data = {
                "LOAN SUMMARY PARAMETERS": ["Loan Amount", "Tenure (Years)", "Interest Rate (%)", "Monthly EMI", "Total Interest Paid", "Total Payable Amount"],
                "VALUE": [p_amount, tenure_years, int_rate, res['monthly_emi'], res['total_interest'], res['total_payment']]
            }
            df_sum = pd.DataFrame(summary_data)
            df_sum.to_excel(writer, sheet_name='Loan Report', index=False, startrow=1)
            
            # Amortization Data below summary
            start_row_schedule = len(df_sum) + 4
            df_schedule.to_excel(writer, sheet_name='Loan Report', index=False, startrow=start_row_schedule)
            
            workbook = writer.book
            worksheet = writer.sheets['Loan Report']
            
            # Professional Formatting
            fmt_header = workbook.add_format({'bold': True, 'bg_color': '#1A365D', 'font_color': 'white', 'border': 1, 'align': 'center'})
            fmt_cell = workbook.add_format({'border': 1, 'align': 'center'})
            fmt_money = workbook.add_format({'border': 1, 'num_format': '#,##,##0', 'align': 'center'})
            fmt_disclaimer = workbook.add_format({'italic': True, 'font_color': '#FF0000', 'font_size': 10, 'align': 'center'})
            
            # Apply header format to Summary
            for col_num, value in enumerate(df_sum.columns.values):
                worksheet.write(1, col_num, value, fmt_header)
            
            # Apply money/round format to summary values (Aligned Center)
            worksheet.write(2, 0, summary_data["LOAN SUMMARY PARAMETERS"][0], fmt_cell)
            worksheet.write(2, 1, p_amount, fmt_money)
            worksheet.write(3, 0, summary_data["LOAN SUMMARY PARAMETERS"][1], fmt_cell)
            worksheet.write(3, 1, tenure_years, fmt_cell)
            worksheet.write(4, 0, summary_data["LOAN SUMMARY PARAMETERS"][2], fmt_cell)
            worksheet.write(4, 1, int_rate, fmt_cell)
            worksheet.write(5, 0, summary_data["LOAN SUMMARY PARAMETERS"][3], fmt_cell)
            worksheet.write(5, 1, res['monthly_emi'], fmt_money)
            worksheet.write(6, 0, summary_data["LOAN SUMMARY PARAMETERS"][4], fmt_cell)
            worksheet.write(6, 1, res['total_interest'], fmt_money)
            worksheet.write(7, 0, summary_data["LOAN SUMMARY PARAMETERS"][5], fmt_cell)
            worksheet.write(7, 1, res['total_payment'], fmt_money)

            # Apply header format to Amortization Schedule
            for col_num, value in enumerate(df_schedule.columns.values):
                worksheet.write(start_row_schedule, col_num, value, fmt_header)
            
            # Apply money/round format to schedule rows (Aligned Center)
            for i, row in df_schedule.iterrows():
                worksheet.write(start_row_schedule + i + 1, 0, row['Year'], fmt_cell)
                worksheet.write(start_row_schedule + i + 1, 1, row['Opening Balance'], fmt_money)
                worksheet.write(start_row_schedule + i + 1, 2, row['EMI*12'], fmt_money)
                worksheet.write(start_row_schedule + i + 1, 3, row['Interest paid yearly'], fmt_money)
                worksheet.write(start_row_schedule + i + 1, 4, row['Principal paid yearly'], fmt_money)
                worksheet.write(start_row_schedule + i + 1, 5, row['Closing Balance'], fmt_money)

            # Add Disclaimer at the end (Aligned Center)
            disclaimer_text = "This calculator provides indicative results only. Actual loan terms may vary based on bank policies."
            worksheet.merge_range(start_row_schedule + len(df_schedule) + 2, 0, start_row_schedule + len(df_schedule) + 2, 5, disclaimer_text, fmt_disclaimer)
                
            worksheet.set_column('A:F', 25)
            
        excel_data = output.getvalue()
        st.download_button(
            label="📥 Download Detailed Banking Report (Excel)",
            data=excel_data,
            file_name=f"Home_Loan_Report_{p_amount}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.error("Please provide valid input values.")
else:
    with col2:
        st.info("Adjust the loan parameters and click 'Calculate EMI' to generate your professional banking plan.")
