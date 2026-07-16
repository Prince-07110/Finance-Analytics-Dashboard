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
            margin-bottom: 20px; border: 1px solid #EAEAEA; height: 140px;
            display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-title { color: #7F8C8D; font-size: 13px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .kpi-value { color: #0A2540; font-size: 26px; font-weight: bold; margin: 5px 0 0 0; }
        </style>
    """, unsafe_allow_html=True)

    st.title("💼 Finance Analytics")
    st.subheader("Chief Financial Officer (CFO) Dashboard")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Monitor revenue, orders and financial performance using AdventureWorks data. | 📅 {c_date} | ⏰ {c_time}")

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
    df_territory = load_smart('Sales.SalesTerritory')

    if not df_order.empty and 'OrderDate' in df_order.columns:
        df_order['OrderDate'] = pd.to_datetime(df_order['OrderDate'], errors='coerce')
        df_order = df_order.dropna(subset=['OrderDate'])
        df_order['Year'] = df_order['OrderDate'].dt.year
        
        st.divider()
        st.header("🎯 Advanced Filters")
        c1, c2 = st.columns(2)
        
        year_list = sorted(df_order['Year'].unique().tolist())
        selected_years = c1.multiselect("Select Year", year_list, default=year_list)
        
        if selected_years:
            df_order = df_order[df_order['Year'].isin(selected_years)]

    tot_rev = float(df_order['TotalDue'].sum()) if not df_order.empty and 'TotalDue' in df_order.columns else 0.0
    tot_ord = len(df_order) if not df_order.empty else 0
    avg_ord_val = (tot_rev / tot_ord) if tot_ord > 0 else 0.0
    tot_tax = float(df_order['TaxAmt'].sum()) if not df_order.empty and 'TaxAmt' in df_order.columns else 0.0
    tot_freight = float(df_order['Freight'].sum()) if not df_order.empty and 'Freight' in df_order.columns else 0.0
    max_ord = float(df_order['TotalDue'].max()) if not df_order.empty and 'TotalDue' in df_order.columns else 0.0
    min_ord = float(df_order['TotalDue'].min()) if not df_order.empty and 'TotalDue' in df_order.columns else 0.0

    st.divider()
    st.header("📊 Executive KPI Cards")
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Total Revenue</p><p class='kpi-value'>${tot_rev:,.0f}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Total Orders</p><p class='kpi-value'>{tot_ord:,}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>💳 Avg Order Value</p><p class='kpi-value'>${avg_ord_val:,.0f}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>🧾 Total Tax</p><p class='kpi-value'>${tot_tax:,.0f}</p></div>", unsafe_allow_html=True)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>🚚 Total Freight</p><p class='kpi-value'>${tot_freight:,.0f}</p></div>", unsafe_allow_html=True)

    k6, k7, k8, k9, k10 = st.columns(5)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>📈 Highest Order</p><p class='kpi-value'>${max_ord:,.0f}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>📉 Lowest Order</p><p class='kpi-value'>${min_ord:,.0f}</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>💵 Avg Rev/Order</p><p class='kpi-value'>${avg_ord_val:,.0f}</p></div>", unsafe_allow_html=True)
    k9.markdown(f"<div class='kpi-box'><p class='kpi-title'>🌍 Active Territories</p><p class='kpi-value'>{len(df_territory)}</p></div>", unsafe_allow_html=True)
    k10.markdown(f"<div class='kpi-box'><p class='kpi-title'>📅 Financial Years</p><p class='kpi-value'>{df_order['Year'].nunique() if not df_order.empty else 0}</p></div>", unsafe_allow_html=True)

    st.divider()
    st.header("📈 Financial Analysis")
    
    if not df_order.empty and 'OrderDate' in df_order.columns and 'TotalDue' in df_order.columns:
        monthly_df = df_order.set_index('OrderDate').resample('ME').agg({'TotalDue':'sum'}).reset_index()
        monthly_df.columns = ['Date', 'Revenue']
        if not monthly_df.empty:
            fig_rev = px.area(monthly_df, x='Date', y='Revenue', title='Revenue Trend Over Time', color_discrete_sequence=['#0066CC'])
            fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_rev, use_container_width=True)

    st.divider()
    st.header("🌍 Revenue Breakdown & Distribution")
    c3, c4 = st.columns(2)
    
    with c3:
        if not df_order.empty and not df_territory.empty and 'TerritoryID' in df_order.columns and 'TerritoryID' in df_territory.columns:
            df_terr_rev = pd.merge(df_order, df_territory[['TerritoryID', 'Name']], on='TerritoryID', how='left')
            terr_rev_df = df_terr_rev.groupby('Name')['TotalDue'].sum().reset_index()
            terr_rev_df.columns = ['Territory', 'Revenue']
            if not terr_rev_df.empty:
                fig_terr = px.pie(terr_rev_df, values='Revenue', names='Territory', title="Revenue by Territory", hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
                fig_terr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_terr, use_container_width=True)

    with c4:
        if not df_order.empty and 'TaxAmt' in df_order.columns and 'Freight' in df_order.columns:
            scatter_df = df_order.head(1000) 
            fig_scatter = px.scatter(scatter_df, x='Freight', y='TaxAmt', size='TotalDue', title="Tax vs Freight Analysis (Sampled)", color_discrete_sequence=['#0A2540'])
            fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    st.header("🗂️ Recent Financial Transactions")
    if not df_order.empty:
        cols_to_show = [col for col in ['SalesOrderID', 'OrderDate', 'CustomerID', 'SubTotal', 'TaxAmt', 'Freight', 'TotalDue'] if col in df_order.columns]
        recent_orders = df_order[cols_to_show].sort_values(by='OrderDate', ascending=False).head(50)
        if 'OrderDate' in recent_orders.columns:
            recent_orders['OrderDate'] = recent_orders['OrderDate'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(recent_orders, use_container_width=True, hide_index=True)

    st.divider()
    st.write("### Finance Analytics Module")
    st.caption("Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Industrial Training: **O7 Services**")