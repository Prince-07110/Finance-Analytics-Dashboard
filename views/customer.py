import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
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

    st.title("👥 Customer Analytics Dashboard")
    st.subheader("Customer Intelligence & Behavior Analysis")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Understand customer behavior and identify high-value clients. | 📅 {c_date} | ⏰ {c_time}")

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

    df_order = load_smart('Sales.SalesOrderHeader')
    df_terr = load_smart('Sales.SalesTerritory')
    df_cust = load_smart('Sales.Customer')
    df_person = load_smart('Person.Person')

    cust_data = pd.DataFrame()
    
    # ADVANCED DATA MERGING & FALLBACK
    if not df_order.empty and 'CustomerID' in df_order.columns and 'TotalDue' in df_order.columns:
        df_order['OrderDate'] = pd.to_datetime(df_order['OrderDate'], errors='coerce')
        cust_data = df_order.groupby('CustomerID').agg(
            Orders=('SalesOrderID', 'count'),
            Revenue=('TotalDue', 'sum'),
            LastOrderDate=('OrderDate', 'max'),
            TerritoryID=('TerritoryID', 'first')
        ).reset_index()
        cust_data['AverageOrderValue'] = cust_data['Revenue'] / cust_data['Orders']

        if not df_terr.empty and 'TerritoryID' in df_terr.columns:
            cust_data = pd.merge(cust_data, df_terr[['TerritoryID', 'Name', 'CountryRegionCode']], on='TerritoryID', how='left')
            cust_data.rename(columns={'Name': 'Territory', 'CountryRegionCode': 'Country'}, inplace=True)
        else:
            cust_data['Territory'] = "Unknown"
            cust_data['Country'] = "Unknown"

        if not df_cust.empty and not df_person.empty and 'PersonID' in df_cust.columns and 'BusinessEntityID' in df_person.columns:
            df_merged_names = pd.merge(df_cust, df_person, left_on='PersonID', right_on='BusinessEntityID', how='inner')
            df_merged_names['CustomerName'] = df_merged_names['FirstName'].fillna('') + ' ' + df_merged_names['LastName'].fillna('')
            cust_data = pd.merge(cust_data, df_merged_names[['CustomerID', 'CustomerName']], on='CustomerID', how='left')
        else:
            cust_data['CustomerName'] = "Customer " + cust_data['CustomerID'].astype(str)

    if cust_data.empty:
        fallback = {
            'CustomerID': range(1001, 1016),
            'CustomerName': [f"Customer {i}" for i in range(1001, 1016)],
            'Territory': ['Northwest', 'Canada', 'France', 'Southwest', 'Germany', 'Australia', 'Northeast', 'Central', 'Canada', 'France', 'Germany', 'Australia', 'Southwest', 'Northwest', 'Northeast'],
            'Country': ['US', 'CA', 'FR', 'US', 'DE', 'AU', 'US', 'US', 'CA', 'FR', 'DE', 'AU', 'US', 'US', 'US'],
            'Orders': [15, 12, 18, 5, 22, 10, 8, 25, 14, 19, 7, 30, 4, 11, 21],
            'Revenue': [125000, 95000, 150000, 45000, 180000, 85000, 70000, 210000, 110000, 160000, 60000, 250000, 35000, 90000, 175000]
        }
        cust_data = pd.DataFrame(fallback)
        cust_data['AverageOrderValue'] = cust_data['Revenue'] / cust_data['Orders']
        cust_data['LastOrderDate'] = pd.to_datetime('2024-05-15')

    tot_cust = len(cust_data)
    tot_rev = cust_data['Revenue'].sum()
    tot_orders = cust_data['Orders'].sum()
    avg_rev_per_cust = (tot_rev / tot_cust) if tot_cust > 0 else 0.0
    avg_ord_per_cust = (tot_orders / tot_cust) if tot_cust > 0 else 0.0
    tot_terr_covered = cust_data['Territory'].nunique()
    
    top_cust = cust_data.sort_values(by='Revenue', ascending=False).iloc[0] if not cust_data.empty else None
    max_rev_cust_name = top_cust['CustomerName'] if top_cust is not None else "N/A"
    max_rev_cust_val = top_cust['Revenue'] if top_cust is not None else 0.0

    st.divider()
    st.header("🎯 Customer KPI Cards")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>👥 Total Customers</p><p class='kpi-value'>{tot_cust:,}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Total Revenue</p><p class='kpi-value'>${tot_rev:,.0f}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Total Orders</p><p class='kpi-value'>{tot_orders:,}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏆 Top Customer</p><p class='kpi-value' style='font-size:18px;'>{max_rev_cust_name}</p></div>", unsafe_allow_html=True)

    k5, k6, k7, k8 = st.columns(4)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>💳 Avg Rev / Customer</p><p class='kpi-value'>${avg_rev_per_cust:,.0f}</p></div>", unsafe_allow_html=True)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>🛒 Avg Orders / Cust</p><p class='kpi-value'>{avg_ord_per_cust:.1f}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>🌍 Territories Covered</p><p class='kpi-value'>{tot_terr_covered}</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>📈 Highest Cust. Rev</p><p class='kpi-value'>${max_rev_cust_val:,.0f}</p></div>", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("💰 Top 10 Customers by Revenue")
        fig_rev = px.bar(cust_data.sort_values(by='Revenue').tail(10), x='Revenue', y='CustomerName', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_rev, use_container_width=True)

    with c2:
        st.subheader("📦 Top 10 Customers by Orders")
        fig_ord = px.bar(cust_data.sort_values(by='Orders', ascending=False).head(10), x='CustomerName', y='Orders', color_discrete_sequence=['#0066CC'])
        fig_ord.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
        st.plotly_chart(fig_ord, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("💵 Revenue Distribution")
        fig_hist = px.histogram(cust_data[cust_data['Revenue'] > 0], x='Revenue', nbins=20, color_discrete_sequence=['#0A2540'])
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Revenue ($)", yaxis_title="Customer Count")
        st.plotly_chart(fig_hist, use_container_width=True)

    with c4:
        st.subheader("🌍 Customers by Territory")
        terr_cust = cust_data.groupby('Territory')['CustomerID'].count().reset_index()
        fig_terr_bar = px.bar(terr_cust.sort_values(by='CustomerID', ascending=False), x='Territory', y='CustomerID', color_discrete_sequence=['#0066CC'])
        fig_terr_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="No. of Customers")
        st.plotly_chart(fig_terr_bar, use_container_width=True)

    st.divider()
    c5, c6 = st.columns(2)
    
    with c5:
        st.subheader("🍩 Revenue by Territory")
        terr_rev = cust_data.groupby('Territory')['Revenue'].sum().reset_index()
        custom_colors = ['#0A2540', '#004C99', '#0066CC', '#3399FF', '#99CCFF']
        fig_terr_pie = px.pie(terr_rev, values='Revenue', names='Territory', hole=0.4, color_discrete_sequence=custom_colors)
        fig_terr_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_terr_pie, use_container_width=True)

    with c6:
        st.subheader("🎯 Customer Segmentation (By Revenue)")
        q33 = cust_data['Revenue'].quantile(0.33) if not cust_data.empty else 0
        q66 = cust_data['Revenue'].quantile(0.66) if not cust_data.empty else 0
        
        def segment(val):
            if val <= q33: return 'Low Value'
            elif val <= q66: return 'Medium Value'
            else: return 'High Value'
            
        cust_data['Segment'] = cust_data['Revenue'].apply(segment)
        seg_df = cust_data.groupby('Segment')['CustomerID'].count().reset_index()
        fig_seg = px.pie(seg_df, values='CustomerID', names='Segment', color_discrete_sequence=['#0A2540', '#0066CC', '#99CCFF'])
        fig_seg.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_seg, use_container_width=True)

    st.divider()
    st.subheader("📊 Average Order Value by Customer (Top 20)")
    fig_aov = px.bar(cust_data.sort_values(by='AverageOrderValue', ascending=False).head(20), x='CustomerName', y='AverageOrderValue', color_discrete_sequence=['#0066CC'])
    fig_aov.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
    st.plotly_chart(fig_aov, use_container_width=True)

    st.divider()
    st.header("💡 Business Insights")
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    
    most_active = cust_data.sort_values(by='Orders', ascending=False).iloc[0]['CustomerName'] if not cust_data.empty else "N/A"
    max_ord_val = cust_data['Orders'].max() if not cust_data.empty else 0
    top_terr_cust = terr_cust.sort_values(by='CustomerID', ascending=False).iloc[0]['Territory'] if not terr_cust.empty else "N/A"
    
    i1.markdown(f"<div class='insight-box'><div class='insight-title'>🏆 Top Customer</div><div class='insight-value' style='font-size:13px;'>{str(max_rev_cust_name)[:18]}</div></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-box'><div class='insight-title'>👑 Most Active</div><div class='insight-value' style='font-size:13px;'>{str(most_active)[:18]}</div></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-box'><div class='insight-title'>💰 Avg Revenue</div><div class='insight-value'>${avg_rev_per_cust:,.0f}</div></div>", unsafe_allow_html=True)
    i4.markdown(f"<div class='insight-box'><div class='insight-title'>📦 Highest Orders</div><div class='insight-value'>{max_ord_val}</div></div>", unsafe_allow_html=True)
    i5.markdown(f"<div class='insight-box'><div class='insight-title'>🌍 Top Territory</div><div class='insight-value' style='font-size:14px;'>{top_terr_cust}</div></div>", unsafe_allow_html=True)
    i6.markdown(f"<div class='insight-box'><div class='insight-title'>📈 High Cust Value</div><div class='insight-value'>${max_rev_cust_val:,.0f}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🗂️ Customer Directory")
    if not cust_data.empty:
        search_cust = st.text_input("🔍 Search by Customer Name or ID...")
        table_df = cust_data.copy()
        if 'LastOrderDate' in table_df.columns:
            table_df['LastOrderDate'] = pd.to_datetime(table_df['LastOrderDate']).dt.strftime('%Y-%m-%d')
            
        if search_cust:
            table_df = table_df[table_df.astype(str).apply(lambda x: x.str.contains(search_cust, case=False)).any(axis=1)]
        
        display_cols = [col for col in ['CustomerID', 'CustomerName', 'Territory', 'Country', 'Orders', 'Revenue', 'AverageOrderValue', 'LastOrderDate', 'Segment'] if col in table_df.columns]
        
        # Format currency for table display
        if 'Revenue' in table_df.columns: table_df['Revenue'] = table_df['Revenue'].apply(lambda x: f"${x:,.2f}")
        if 'AverageOrderValue' in table_df.columns: table_df['AverageOrderValue'] = table_df['AverageOrderValue'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(table_df[display_cols].head(100), use_container_width=True, hide_index=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Customer Analytics Module | Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Training: **O7 Services**")