
import streamlit as st
import pandas as pd
import numpy as np
import requests
from pandasql import sqldf
import os

# If csv then populate
try:
    saved_info = pd.read_csv("saved_info.csv")

    first_row = saved_info.iloc[0]
    savings_ratio = first_row.savings_ratio
    yearly_salary = first_row.yearly_salary
    # Common info
    st.text_input("Take home pay per paycheck" , key="paycheck", value = yearly_salary/26)
    paycheck = st.session_state.paycheck
    paycheck = None if paycheck.strip() == "" else float(paycheck)
    yearly_salary = None if paycheck == None else paycheck*26

    st.text_input("What % of your pay do you save every month before this new item (i.e. 10%)" , key="savings_ratio", value=str(np.round(savings_ratio*100,2)) + "%")
    savings_ratio = st.session_state.savings_ratio
    savings_ratio = None if savings_ratio.strip() == "" else savings_ratio
    savings_ratio = float(savings_ratio) if "%" not in savings_ratio else float(savings_ratio.replace("%", ""))/100
    total_savings_a_year = savings_ratio*yearly_salary if yearly_salary != None and savings_ratio != None else None

except:
    saved_info = None

    # Common info
    st.text_input("Take home pay per paycheck" , key="paycheck")
    paycheck = st.session_state.paycheck
    paycheck = None if paycheck.strip() == "" else float(paycheck)
    yearly_salary = None if paycheck == None else paycheck*26

    st.text_input("What % of your pay do you save every month (i.e. 10%)" , key="savings_ratio")
    savings_ratio = st.session_state.savings_ratio
    savings_ratio = None if savings_ratio.strip() == "" else savings_ratio
    savings_ratio = float(savings_ratio) if "%" not in savings_ratio else float(savings_ratio.replace("%", ""))/100
    total_savings_a_year = savings_ratio*yearly_salary if yearly_salary != None and savings_ratio != None else None


# Once common info is filled save as csv
if yearly_salary != None and savings_ratio != None:
    saved_info = pd.DataFrame({'yearly_salary': [yearly_salary], 'savings_ratio': [savings_ratio]})
    saved_info.to_csv("saved_info.csv", index=False)

st.text_input("Cost of the item" , key="cost_of_goods")
cost_of_goods = st.session_state.cost_of_goods
cost_of_goods = None if cost_of_goods.strip() == "" else float(cost_of_goods)

st.text_input("How often you will purchase it" , key="purchase_frequency")
purchase_frequency = st.session_state.purchase_frequency
purchase_frequency = None if purchase_frequency.strip() == "" else float(purchase_frequency)

if total_savings_a_year != None and cost_of_goods != None and purchase_frequency != None:
    total_savings_a_year = total_savings_a_year - cost_of_goods*purchase_frequency # Update savings

savings_needed_to_upkeep_purchases = 25*cost_of_goods*purchase_frequency if cost_of_goods != None and purchase_frequency != None else None
extra_years_of_working_required = savings_needed_to_upkeep_purchases/total_savings_a_year if savings_needed_to_upkeep_purchases != None and total_savings_a_year != None else None

if savings_needed_to_upkeep_purchases != None:
    st.write("Savings needed to upkeep these purchases:", "${:,.2f}".format(savings_needed_to_upkeep_purchases))
if extra_years_of_working_required != None:
    st.write("Years of extra work needed to upkeep these purchases:", str(np.round(extra_years_of_working_required,2)), "years")
