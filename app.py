import streamlit as st
import pandas as pd
import plotly.express as px


data = pd.read_csv('dummy_sample.csv')

st.sidebar.title("Dashboard Navigation")
tabs = st.sidebar.radio("Select Tab", ['Overview', 'Company Analysis', 'Fund Analysis', 'Geographical Analysis', 'Theme Analysis'])

if tabs == 'Overview':
    st.title("Overview of Investments and Emissions")

    total_investment = data['Investment ($M)'].sum()
    total_capital = data['Total Capital Committed ($B)'].sum()
    total_emissions = data['Total Emissions by Fund (tons of CO2e)'].sum()

    st.metric("Total Investment ($M)", f"${total_investment:.2f}M")
    st.metric("Total Capital Committed ($B)", f"${total_capital:.2f}B")
    st.metric("Total Emissions (tons of CO2e)", f"{total_emissions:,.0f} tons")
    top_funds = data.groupby('Fund')['Investment ($M)'].sum().nlargest(5)
    fig_investment = px.bar(top_funds, x=top_funds.index, y='Investment ($M)', title="Top 5 Funds by Investment")
    st.plotly_chart(fig_investment)
elif tabs == 'Company Analysis':
    st.title("Company Analysis")
    company = st.selectbox("Select a Company", data['Company Name'].unique())
    
    company_data = data[data['Company Name'] == company]
    
    st.write(f"Details for {company}:")
    st.write(company_data)
    fig_company = px.bar(company_data, x='Fund', y='Investment ($M)', title=f"Investments by {company}")
    st.plotly_chart(fig_company)

elif tabs == 'Fund Analysis':
    st.title("Fund Analysis")
    fund = st.selectbox("Select a Fund", data['Fund'].unique())
    
    fund_data = data[data['Fund'] == fund]
    
    st.write(f"Details for {fund}:")
    st.write(fund_data)
    
    fig_scope = px.bar(fund_data, x='Company Name', y=['Scope 1 Emissions (tons of CO2e)', 'Scope 2 Emissions (tons of CO2e)', 'Scope 3 Emissions (tons of CO2e)'],
                       title=f"Emissions by Scope for {fund}")
    st.plotly_chart(fig_scope)

elif tabs == 'Geographical Analysis':
    st.title("Geographical Analysis")
    
    fig_map = px.scatter_geo(data, locations="Country", locationmode="country names",
                             size="Country Capital Catalyzed ($M)", hover_name="Country",
                             title="Capital Catalyzed by Country")
    st.plotly_chart(fig_map)
elif tabs == 'Theme Analysis':
    st.title("Theme Analysis")
    
    theme = st.selectbox("Select a Theme", data['Theme'].unique())
    
    theme_data = data[data['Theme'] == theme]
    
    st.write(f"Details for {theme}:")
    st.write(theme_data)

    fig_theme = px.bar(theme_data, x='Company Name', y='Theme Capital Catalyzed ($M)',
                       title=f"Capital Catalyzed by Theme: {theme}")
    st.plotly_chart(fig_theme)
