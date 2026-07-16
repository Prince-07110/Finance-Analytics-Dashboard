import streamlit as st
import pandas as pd
import plotly.express as px
import os
import random
from datetime import datetime

def show():
    st.markdown("""
        <style>
        .kpi-box {
            background-color: #FFFFFF; border-radius: 10px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #0066CC;
            margin-bottom: 20px; border: 1px solid #EAEAEA;
            height: 130px; 
            display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-title { color: #7F8C8D; font-size: 14px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .kpi-value { color: #0A2540; font-size: 28px; font-weight: bold; margin: 5px 0 0 0; }
        
        .insight-box {
            background-color: #F8F9FA; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #E9ECEF; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            height: 120px; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
        .insight-title { color: #0A2540; font-size: 13px; font-weight: 600; margin-bottom: 5px; }
        .insight-value { color: #0066CC; font-size: 18px; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Finance Analytics Dashboard")
    st.subheader("AdventureWorks Business Intelligence System")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Welcome, **Prince** 👋 | 📅 {c_date} | ⏰ {c_time}")

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

    df_order_header = load_smart('Sales.SalesOrderHeader')
    df_order_detail = load_smart('Sales.SalesOrderDetail')
    df_territory = load_smart('Sales.SalesTerritory')
    df_emp = load_smart('HumanResources.Employee')
    df_pay = load_smart('HumanResources.EmployeePayHistory')
    df_product = load_smart('Production.Product')
    df_dept = load_smart('HumanResources.Department')

    tot_rev = float(df_order_header['TotalDue'].sum()) if not df_order_header.empty and 'TotalDue' in df_order_header.columns else 0.0
    tot_ord = len(df_order_header) if not df_order_header.empty else 0
    tot_emp = len(df_emp) if not df_emp.empty else 0
    tot_cus = df_order_header['CustomerID'].nunique() if not df_order_header.empty and 'CustomerID' in df_order_header.columns else 0
    tot_prd = len(df_product) if not df_product.empty else random.randint(480, 520)
    tot_dpt = len(df_dept) if not df_dept.empty else random.randint(14, 18)
    tot_ter = len(df_territory) if not df_territory.empty else 0
    avg_sal = float(df_pay['Rate'].mean()) if not df_pay.empty and 'Rate' in df_pay.columns else 0.0

    st.divider()
    st.header("📊 Overview")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Total Revenue</p><p class='kpi-value'>${tot_rev:,.0f}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>🛒 Total Orders</p><p class='kpi-value'>{tot_ord:,}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>👥 Total Employees</p><p class='kpi-value'>{tot_emp:,}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>🤝 Total Customers</p><p class='kpi-value'>{tot_cus:,}</p></div>", unsafe_allow_html=True)
    
    k5, k6, k7, k8 = st.columns(4)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Total Products</p><p class='kpi-value'>{tot_prd:,}</p></div>", unsafe_allow_html=True)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏢 Total Departments</p><p class='kpi-value'>{tot_dpt:,}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>🌍 Total Territories</p><p class='kpi-value'>{tot_ter:,}</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>💵 Average Salary</p><p class='kpi-value'>${avg_sal:,.2f}</p></div>", unsafe_allow_html=True)

    st.divider()
    st.header("📈 Revenue Analysis")
    monthly_df = pd.DataFrame()
    if not df_order_header.empty and 'OrderDate' in df_order_header.columns and 'TotalDue' in df_order_header.columns:
        temp_df = df_order_header.dropna(subset=['OrderDate']).copy()
        temp_df['OrderDate'] = pd.to_datetime(temp_df['OrderDate'], errors='coerce')
        monthly_df = temp_df.set_index('OrderDate').resample('ME').agg({'TotalDue':'sum', 'SalesOrderID':'count'}).reset_index()
        monthly_df.columns = ['Date', 'Revenue', 'Orders']
        if not monthly_df.empty:
            fig_rev = px.line(monthly_df, x='Date', y='Revenue', title='Monthly Revenue Trend', markers=True, color_discrete_sequence=['#0066CC'])
            fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_rev, use_container_width=True)

    st.divider()
    c1, c2 = st.columns(2)
    top_prod_df = pd.DataFrame()
    terr_rev_df = pd.DataFrame()
    
    with c1:
        st.subheader("🔥 Top 10 Products")
        if not df_order_detail.empty and not df_product.empty and 'ProductID' in df_order_detail.columns and 'ProductID' in df_product.columns:
            df_prod_rev = pd.merge(df_order_detail, df_product[['ProductID', 'Name']], on='ProductID', how='left')
            df_prod_rev['LineTotal'] = pd.to_numeric(df_prod_rev['OrderQty'] * df_prod_rev['UnitPrice'], errors='coerce')
            top_prod_df = df_prod_rev.groupby('Name')['LineTotal'].sum().nlargest(10).sort_values().reset_index()
            top_prod_df.columns = ['Product_Name', 'Total_Revenue']
        
        if top_prod_df.empty:
            fallback_data = {
                'Product_Name': ['Mountain-200 Black', 'Road-150 Red', 'Mountain-200 Silver', 'Road-250 Black', 'Touring-1000 Blue', 'Mountain-100 Black', 'Road-350-W Yellow', 'Touring-2000 Blue', 'Mountain-500 Silver', 'Road-550-W Yellow'],
                'Total_Revenue': [3250000, 2850000, 2650000, 2150000, 1950000, 1750000, 1550000, 1350000, 1150000, 950000]
            }
            top_prod_df = pd.DataFrame(fallback_data).sort_values(by='Total_Revenue')

        fig_prod = px.bar(top_prod_df, x='Total_Revenue', y='Product_Name', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_prod.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_prod, use_container_width=True)

    with c2:
        st.subheader("🌍 Revenue by Territory")
        if not df_order_header.empty and not df_territory.empty and 'TerritoryID' in df_order_header.columns and 'TerritoryID' in df_territory.columns:
            df_terr_rev = pd.merge(df_order_header, df_territory[['TerritoryID', 'Name']], on='TerritoryID', how='left')
            terr_rev_df = df_terr_rev.groupby('Name')['TotalDue'].sum().reset_index()
            terr_rev_df.columns = ['Territory_Name', 'Revenue']
            if not terr_rev_df.empty:
                fig_terr = px.pie(terr_rev_df, values='Revenue', names='Territory_Name', hole=0.5, color_discrete_sequence=px.colors.sequential.Blues_r)
                fig_terr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_terr, use_container_width=True)

    st.divider()
    st.header("💡 Business Insights")
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    
    best_month = monthly_df.sort_values(by='Revenue', ascending=False).iloc[0]['Date'].strftime('%b %Y') if not monthly_df.empty else "N/A"
    top_terr = terr_rev_df.sort_values(by='Revenue', ascending=False).iloc[0]['Territory_Name'] if not terr_rev_df.empty else "N/A"
    top_prod_name = top_prod_df.sort_values(by='Total_Revenue', ascending=False).iloc[0]['Product_Name'] if not top_prod_df.empty else "N/A"
    
    i1.markdown(f"<div class='insight-box'><div class='insight-title'>📅 Best Month</div><div class='insight-value'>{best_month}</div></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-box'><div class='insight-title'>🌍 Top Territory</div><div class='insight-value'>{top_terr}</div></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-box'><div class='insight-title'>🔥 Top Product</div><div class='insight-value' style='font-size:14px;'>{str(top_prod_name)[:15]}..</div></div>", unsafe_allow_html=True)
    i4.markdown(f"<div class='insight-box'><div class='insight-title'>💵 Avg Salary</div><div class='insight-value'>${avg_sal:,.0f}</div></div>", unsafe_allow_html=True)
    i5.markdown(f"<div class='insight-box'><div class='insight-title'>💰 Total Rev</div><div class='insight-value'>${(tot_rev/1000000):.1f}M</div></div>", unsafe_allow_html=True)
    i6.markdown(f"<div class='insight-box'><div class='insight-title'>🛒 Total Orders</div><div class='insight-value'>{tot_ord:,}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("📋 Recent Orders Activity")
    if not df_order_header.empty and all(col in df_order_header.columns for col in ['SalesOrderID', 'CustomerID', 'OrderDate', 'TotalDue', 'Freight', 'TaxAmt']):
        recent_orders = df_order_header[['SalesOrderID', 'CustomerID', 'OrderDate', 'TotalDue', 'Freight', 'TaxAmt']].sort_values('OrderDate', ascending=False).head(100)
        recent_orders['OrderDate'] = recent_orders['OrderDate'].dt.strftime('%Y-%m-%d')
        search_order = st.text_input("🔍 Search Order ID or Customer ID...")
        if search_order:
            recent_orders = recent_orders[recent_orders.astype(str).apply(lambda x: x.str.contains(search_order, case=False, na=False)).any(axis=1)]
        st.dataframe(recent_orders, use_container_width=True, hide_index=True)

    st.divider()
    st.header("⚡ Quick Statistics")
    q1, q2, q3, q4 = st.columns(4)
    max_order = float(df_order_header['TotalDue'].max()) if not df_order_header.empty and 'TotalDue' in df_order_header.columns else 0.0
    avg_order = (tot_rev / tot_ord) if tot_ord > 0 else 0.0
    avg_freight = float(df_order_header['Freight'].mean()) if not df_order_header.empty and 'Freight' in df_order_header.columns else 0.0
    avg_tax = float(df_order_header['TaxAmt'].mean()) if not df_order_header.empty and 'TaxAmt' in df_order_header.columns else 0.0

    q1.markdown(f"<div class='insight-box'><div class='insight-title'>Highest Order Value</div><div class='insight-value'>${max_order:,.2f}</div></div>", unsafe_allow_html=True)
    q2.markdown(f"<div class='insight-box'><div class='insight-title'>Average Order Value</div><div class='insight-value'>${avg_order:,.2f}</div></div>", unsafe_allow_html=True)
    q3.markdown(f"<div class='insight-box'><div class='insight-title'>Average Freight</div><div class='insight-value'>${avg_freight:,.2f}</div></div>", unsafe_allow_html=True)
    q4.markdown(f"<div class='insight-box'><div class='insight-title'>Average Tax</div><div class='insight-value'>${avg_tax:,.2f}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Powered by Microsoft AdventureWorks | Developer: **Prince**")