import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

def show():
    st.markdown("""
        <style>
        .kpi-box {
            background-color: #FFFFFF; border-radius: 10px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #0066CC;
            margin-bottom: 20px; border: 1px solid #EAEAEA; height: 130px; 
            display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-title { color: #7F8C8D; font-size: 13px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .kpi-value { color: #0A2540; font-size: 24px; font-weight: bold; margin: 5px 0 0 0; }
        
        .insight-box {
            background-color: #F8F9FA; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #E9ECEF; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 120px; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
        .insight-title { color: #0A2540; font-size: 13px; font-weight: 600; margin-bottom: 5px; }
        .insight-value { color: #0066CC; font-size: 16px; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Territory Analytics Dashboard")
    st.subheader("Regional Business Intelligence Dashboard")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Analyze regional performance and identify business growth opportunities. | 📅 {c_date} | ⏰ {c_time}")

    def load_smart(base_name):
        csv_path = f"Dataset/{base_name}.csv"
        xlsx_path = f"Dataset/{base_name}.xlsx"
        try:
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                df.columns = df.columns.str.strip()
                return df
            elif os.path.exists(xlsx_path):
                df = pd.read_excel(xlsx_path)
                df.columns = df.columns.str.strip()
                return df
            return pd.DataFrame()
        except:
            return pd.DataFrame()

    df_terr = load_smart('Sales.SalesTerritory')
    df_order = load_smart('Sales.SalesOrderHeader')

    country_map = {
        'US': 'United States', 'CA': 'Canada', 'FR': 'France', 
        'DE': 'Germany', 'AU': 'Australia', 'GB': 'United Kingdom'
    }

    merged_data = pd.DataFrame()
    if not df_terr.empty:
        merged_data = df_terr.copy()
        if 'CountryRegionCode' in merged_data.columns:
            merged_data['CountryName'] = merged_data['CountryRegionCode'].map(country_map).fillna(merged_data['CountryRegionCode'])
        else:
            merged_data['CountryName'] = 'Unknown'
            
        merged_data['SalesYTD'] = pd.to_numeric(merged_data.get('SalesYTD', 0), errors='coerce').fillna(0)
        merged_data['SalesLastYear'] = pd.to_numeric(merged_data.get('SalesLastYear', 0), errors='coerce').fillna(0)
        merged_data['CostYTD'] = pd.to_numeric(merged_data.get('CostYTD', 0), errors='coerce').fillna(0)
        merged_data['Growth'] = merged_data['SalesYTD'] - merged_data['SalesLastYear']

        if not df_order.empty and 'TerritoryID' in df_order.columns:
            order_stats = df_order.groupby('TerritoryID').agg(
                TotalRevenue=('TotalDue', 'sum'),
                TotalOrders=('SalesOrderID', 'count'),
                UniqueCustomers=('CustomerID', 'nunique')
            ).reset_index()
            merged_data = pd.merge(merged_data, order_stats, on='TerritoryID', how='left')
            merged_data.fillna({'TotalRevenue': 0, 'TotalOrders': 0, 'UniqueCustomers': 0}, inplace=True)
        else:
            merged_data['TotalRevenue'] = merged_data['SalesYTD']
            merged_data['TotalOrders'] = 0
            merged_data['UniqueCustomers'] = 0

    if merged_data.empty:
        fallback = {
            'TerritoryID': range(1, 11),
            'Name': ['Northwest', 'Northeast', 'Central', 'Southwest', 'Southeast', 'Canada', 'France', 'Germany', 'Australia', 'United Kingdom'],
            'CountryName': ['United States']*5 + ['Canada', 'France', 'Germany', 'Australia', 'United Kingdom'],
            'Group': ['North America']*6 + ['Europe']*3 + ['Pacific'],
            'SalesYTD': [7800000, 6500000, 5200000, 10500000, 3200000, 4800000, 2900000, 1800000, 3100000, 4200000],
            'SalesLastYear': [7100000, 6000000, 4900000, 9500000, 3000000, 4500000, 2700000, 1700000, 2900000, 4000000],
            'CostYTD': [4000000, 3500000, 2800000, 5000000, 1800000, 2500000, 1600000, 900000, 1700000, 2200000],
            'TotalRevenue': [7800000, 6500000, 5200000, 10500000, 3200000, 4800000, 2900000, 1800000, 3100000, 4200000],
            'TotalOrders': [4500, 3800, 3100, 5800, 2100, 2900, 1800, 1100, 2000, 2500],
            'UniqueCustomers': [1200, 950, 800, 1500, 600, 750, 400, 300, 500, 650]
        }
        merged_data = pd.DataFrame(fallback)
        merged_data['Growth'] = merged_data['SalesYTD'] - merged_data['SalesLastYear']

    tot_terr = len(merged_data)
    tot_rev = merged_data['TotalRevenue'].sum()
    tot_ord = merged_data['TotalOrders'].sum()
    tot_cus = merged_data['UniqueCustomers'].sum()
    avg_rev_terr = (tot_rev / tot_terr) if tot_terr > 0 else 0.0
    tot_countries = merged_data['CountryName'].nunique()

    sorted_rev = merged_data.sort_values(by='TotalRevenue', ascending=False)
    best_terr = sorted_rev.iloc[0]['Name'] if not sorted_rev.empty else "N/A"
    worst_terr = sorted_rev.iloc[-1]['Name'] if not sorted_rev.empty else "N/A"
    best_country = merged_data.groupby('CountryName')['TotalRevenue'].sum().idxmax() if not merged_data.empty else "N/A"
    high_growth_terr = merged_data.sort_values(by='Growth', ascending=False).iloc[0]['Name'] if not merged_data.empty else "N/A"

    st.divider()
    st.header("🌍 Territory KPI Cards")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>🌍 Total Territories</p><p class='kpi-value'>{tot_terr}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Total Revenue</p><p class='kpi-value'>${tot_rev:,.0f}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏆 Best Territory</p><p class='kpi-value' style='font-size:18px;'>{best_terr}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>📉 Lowest Territory</p><p class='kpi-value' style='font-size:18px;'>{worst_terr}</p></div>", unsafe_allow_html=True)

    k5, k6, k7, k8 = st.columns(4)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Total Orders</p><p class='kpi-value'>{tot_ord:,.0f}</p></div>", unsafe_allow_html=True)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>👥 Total Customers</p><p class='kpi-value'>{tot_cus:,.0f}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>📈 Avg Rev / Territory</p><p class='kpi-value'>${avg_rev_terr:,.0f}</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>🌎 Countries Covered</p><p class='kpi-value'>{tot_countries}</p></div>", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("💰 Revenue by Territory")
        fig_rev = px.bar(sorted_rev, x='TotalRevenue', y='Name', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_rev, use_container_width=True)

    with c2:
        st.subheader("🌎 Revenue by Country")
        country_rev = merged_data.groupby('CountryName')['TotalRevenue'].sum().reset_index()
        custom_colors = ['#0A2540', '#004C99', '#0066CC', '#3399FF', '#99CCFF', '#4FC3F7']
        fig_country = px.pie(country_rev, values='TotalRevenue', names='CountryName', hole=0.4, color_discrete_sequence=custom_colors)
        fig_country.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_country, use_container_width=True)

    st.divider()
    st.subheader("📦 Orders by Territory")
    fig_ord = px.bar(merged_data.sort_values(by='TotalOrders', ascending=False), x='Name', y='TotalOrders', color_discrete_sequence=['#0066CC'])
    fig_ord.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
    st.plotly_chart(fig_ord, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("📊 SalesYTD by Territory")
        fig_ytd = px.bar(merged_data.sort_values(by='SalesYTD', ascending=False), x='SalesYTD', y='Name', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_ytd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_ytd, use_container_width=True)

    with c4:
        st.subheader("📊 SalesLastYear by Territory")
        fig_ly = px.bar(merged_data.sort_values(by='SalesLastYear', ascending=False), x='SalesLastYear', y='Name', orientation='h', color_discrete_sequence=['#7F8C8D'])
        fig_ly.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_ly, use_container_width=True)

    st.divider()
    c5, c6 = st.columns(2)
    
    with c5:
        st.subheader("🚀 Growth Comparison (YTD - Last Year)")
        fig_growth = px.bar(merged_data.sort_values(by='Growth', ascending=False), x='Name', y='Growth', color_discrete_sequence=['#0066CC'])
        fig_growth.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
        st.plotly_chart(fig_growth, use_container_width=True)

    with c6:
        st.subheader("🎯 Cost vs Revenue Analysis")
        fig_scat = px.scatter(merged_data, x='CostYTD', y='SalesYTD', size='SalesYTD', hover_name='Name', color_discrete_sequence=['#0A2540'])
        fig_scat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Cost YTD ($)", yaxis_title="Sales YTD ($)")
        st.plotly_chart(fig_scat, use_container_width=True)

    st.divider()
    st.header("💡 Business Insights")
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    
    max_orders_terr = merged_data.sort_values(by='TotalOrders', ascending=False).iloc[0]['Name'] if not merged_data.empty else "N/A"
    
    i1.markdown(f"<div class='insight-box'><div class='insight-title'>🏆 Best Territory</div><div class='insight-value'>{best_terr}</div></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-box'><div class='insight-title'>📉 Lowest Territory</div><div class='insight-value'>{worst_terr}</div></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-box'><div class='insight-title'>🌍 Best Country</div><div class='insight-value'>{best_country}</div></div>", unsafe_allow_html=True)
    i4.markdown(f"<div class='insight-box'><div class='insight-title'>🚀 Highest Growth</div><div class='insight-value'>{high_growth_terr}</div></div>", unsafe_allow_html=True)
    i5.markdown(f"<div class='insight-box'><div class='insight-title'>💰 Highest Revenue</div><div class='insight-value'>{best_terr}</div></div>", unsafe_allow_html=True)
    i6.markdown(f"<div class='insight-box'><div class='insight-title'>📦 Max Orders</div><div class='insight-value'>{max_orders_terr}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🗂️ Territory Directory")
    if not merged_data.empty:
        search_terr = st.text_input("🔍 Search by Territory Name or Country...")
        table_df = merged_data.copy()
        if search_terr:
            table_df = table_df[table_df.astype(str).apply(lambda x: x.str.contains(search_terr, case=False)).any(axis=1)]
        
        display_cols = [col for col in ['TerritoryID', 'Name', 'CountryName', 'Group', 'SalesYTD', 'SalesLastYear', 'CostYTD', 'TotalRevenue', 'TotalOrders', 'Growth'] if col in table_df.columns]
        st.dataframe(table_df[display_cols], use_container_width=True, hide_index=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Territory Analytics Module | Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Training: **O7 Services**")