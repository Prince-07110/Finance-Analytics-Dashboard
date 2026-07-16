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

    st.title("📦 Product Analytics Dashboard")
    st.subheader("Product Performance Intelligence")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Analyze product performance and optimize business growth. | 📅 {c_date} | ⏰ {c_time}")

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

    df_prod = load_smart('Production.Product')
    df_cat = load_smart('Production.ProductCategory')
    df_subcat = load_smart('Production.ProductSubcategory')
    df_sales = load_smart('Sales.SalesOrderDetail')

    merged_prod = pd.DataFrame()
    sales_merged = pd.DataFrame()

    if not df_prod.empty:
        merged_prod = df_prod.copy()
        if not df_subcat.empty and 'ProductSubcategoryID' in merged_prod.columns and 'ProductSubcategoryID' in df_subcat.columns:
            merged_prod = pd.merge(merged_prod, df_subcat[['ProductSubcategoryID', 'ProductCategoryID', 'Name']], on='ProductSubcategoryID', how='left')
            merged_prod.rename(columns={'Name_x': 'ProductName', 'Name_y': 'Subcategory'}, inplace=True)
            if 'Name' in merged_prod.columns:
                merged_prod.rename(columns={'Name': 'Subcategory'}, inplace=True)
        else:
            merged_prod['Subcategory'] = "Unknown"
            merged_prod['ProductCategoryID'] = 0
            if 'Name' in merged_prod.columns:
                merged_prod.rename(columns={'Name': 'ProductName'}, inplace=True)

        if not df_cat.empty and 'ProductCategoryID' in merged_prod.columns and 'ProductCategoryID' in df_cat.columns:
            merged_prod = pd.merge(merged_prod, df_cat[['ProductCategoryID', 'Name']], on='ProductCategoryID', how='left')
            merged_prod.rename(columns={'Name': 'Category'}, inplace=True)
        else:
            merged_prod['Category'] = "Unknown"

        if not df_sales.empty and 'ProductID' in merged_prod.columns and 'ProductID' in df_sales.columns:
            df_sales['LineTotal'] = pd.to_numeric(df_sales['OrderQty'] * df_sales['UnitPrice'], errors='coerce')
            sales_merged = pd.merge(df_sales, merged_prod[['ProductID', 'ProductName', 'Category', 'Subcategory']], on='ProductID', how='inner')

    if sales_merged.empty or merged_prod.empty:
        prod_fallback = {
            'ProductID': range(1, 11),
            'ProductName': ['Mountain-200 Black', 'Road-150 Red', 'Mountain-200 Silver', 'Road-250 Black', 'Touring-1000 Blue', 'Mountain-100 Black', 'Road-350-W Yellow', 'Touring-2000 Blue', 'Mountain-500 Silver', 'Road-550-W Yellow'],
            'Category': ['Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes', 'Bikes'],
            'Subcategory': ['Mountain Bikes', 'Road Bikes', 'Mountain Bikes', 'Road Bikes', 'Touring Bikes', 'Mountain Bikes', 'Road Bikes', 'Touring Bikes', 'Mountain Bikes', 'Road Bikes'],
            'Color': ['Black', 'Red', 'Silver', 'Black', 'Blue', 'Black', 'Yellow', 'Blue', 'Silver', 'Yellow'],
            'Size': ['38', '44', '42', '48', '50', '38', '40', '54', '42', '44'],
            'StandardCost': [1500, 1200, 1400, 1100, 900, 800, 700, 600, 500, 400],
            'ListPrice': [2500, 2000, 2300, 1800, 1500, 1400, 1200, 1000, 900, 750],
            'FinishedGoodsFlag': [1]*10,
            'SellStartDate': ['2023-01-01']*10
        }
        merged_prod = pd.DataFrame(prod_fallback)
        
        sales_fallback = {
            'ProductName': prod_fallback['ProductName'],
            'Category': prod_fallback['Category'],
            'Subcategory': prod_fallback['Subcategory'],
            'OrderQty': [500, 400, 350, 300, 250, 200, 150, 100, 80, 50],
            'LineTotal': [1250000, 800000, 805000, 540000, 375000, 280000, 180000, 100000, 72000, 37500]
        }
        sales_merged = pd.DataFrame(sales_fallback)

    tot_products = len(merged_prod)
    avg_price = merged_prod['ListPrice'].mean() if 'ListPrice' in merged_prod.columns else 0.0
    avg_cost = merged_prod['StandardCost'].mean() if 'StandardCost' in merged_prod.columns else 0.0
    tot_cat = merged_prod['Category'].nunique() if 'Category' in merged_prod.columns else 0
    tot_subcat = merged_prod['Subcategory'].nunique() if 'Subcategory' in merged_prod.columns else 0
    finished_goods = int(merged_prod['FinishedGoodsFlag'].sum()) if 'FinishedGoodsFlag' in merged_prod.columns else tot_products
    
    prod_rev_df = sales_merged.groupby('ProductName')['LineTotal'].sum().reset_index()
    prod_qty_df = sales_merged.groupby('ProductName')['OrderQty'].sum().reset_index()
    
    highest_rev_prod = prod_rev_df.sort_values(by='LineTotal', ascending=False).iloc[0]['ProductName'] if not prod_rev_df.empty else "N/A"
    best_sell_prod = prod_qty_df.sort_values(by='OrderQty', ascending=False).iloc[0]['ProductName'] if not prod_qty_df.empty else "N/A"

    st.divider()
    st.header("🎯 Product KPI Cards")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Total Products</p><p class='kpi-value'>{tot_products:,}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Highest Rev Product</p><p class='kpi-value' style='font-size:16px;'>{str(highest_rev_prod)[:25]}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏆 Best Selling Product</p><p class='kpi-value' style='font-size:16px;'>{str(best_sell_prod)[:25]}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>💵 Avg List Price</p><p class='kpi-value'>${avg_price:,.2f}</p></div>", unsafe_allow_html=True)

    k5, k6, k7, k8 = st.columns(4)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>💲 Avg Standard Cost</p><p class='kpi-value'>${avg_cost:,.2f}</p></div>", unsafe_allow_html=True)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>🎯 Total Categories</p><p class='kpi-value'>{tot_cat}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>📂 Total Subcategories</p><p class='kpi-value'>{tot_subcat}</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>📈 Finished Goods</p><p class='kpi-value'>{finished_goods:,}</p></div>", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("💰 Top 10 Products by Revenue")
        fig_rev = px.bar(prod_rev_df.sort_values(by='LineTotal').tail(10), x='LineTotal', y='ProductName', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_rev, use_container_width=True)

    with c2:
        st.subheader("📦 Top 10 Products by Quantity")
        fig_qty = px.bar(prod_qty_df.sort_values(by='OrderQty', ascending=False).head(10), x='ProductName', y='OrderQty', color_discrete_sequence=['#0066CC'])
        fig_qty.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
        st.plotly_chart(fig_qty, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("⚠️ Worst Selling Products (Revenue)")
        worst_rev = prod_rev_df[prod_rev_df['LineTotal'] > 0].sort_values(by='LineTotal').head(10)
        fig_worst = px.bar(worst_rev, x='LineTotal', y='ProductName', orientation='h', color_discrete_sequence=['#E74C3C'])
        fig_worst.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_worst, use_container_width=True)

    with c4:
        st.subheader("🍩 Revenue by Category")
        cat_rev = sales_merged.groupby('Category')['LineTotal'].sum().reset_index()
        custom_colors = ['#0A2540', '#004C99', '#0066CC', '#3399FF', '#99CCFF']
        fig_cat = px.pie(cat_rev, values='LineTotal', names='Category', hole=0.4, color_discrete_sequence=custom_colors)
        fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()
    st.subheader("📊 Revenue by Subcategory")
    subcat_rev = sales_merged.groupby('Subcategory')['LineTotal'].sum().reset_index().sort_values(by='LineTotal', ascending=False).head(15)
    fig_subcat = px.bar(subcat_rev, x='Subcategory', y='LineTotal', color_discrete_sequence=['#0066CC'])
    fig_subcat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
    st.plotly_chart(fig_subcat, use_container_width=True)

    st.divider()
    c5, c6 = st.columns(2)
    
    with c5:
        st.subheader("💵 Price Distribution")
        if 'ListPrice' in merged_prod.columns:
            fig_price = px.histogram(merged_prod[merged_prod['ListPrice'] > 0], x='ListPrice', nbins=20, color_discrete_sequence=['#0A2540'])
            fig_price.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="List Price ($)", yaxis_title="Count")
            st.plotly_chart(fig_price, use_container_width=True)

    with c6:
        st.subheader("💲 Standard Cost Distribution")
        if 'StandardCost' in merged_prod.columns:
            fig_cost = px.histogram(merged_prod[merged_prod['StandardCost'] > 0], x='StandardCost', nbins=20, color_discrete_sequence=['#0066CC'])
            fig_cost.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Standard Cost ($)", yaxis_title="Count")
            st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()
    st.subheader("🎯 Cost vs Price Analysis")
    if 'ListPrice' in merged_prod.columns and 'StandardCost' in merged_prod.columns:
        scatter_df = merged_prod[(merged_prod['ListPrice'] > 0) & (merged_prod['StandardCost'] > 0)]
        fig_scatter = px.scatter(scatter_df, x='StandardCost', y='ListPrice', hover_name='ProductName', color_discrete_sequence=['#0066CC'])
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Standard Cost ($)", yaxis_title="List Price ($)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    st.header("💡 Business Insights")
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    
    max_price = merged_prod['ListPrice'].max() if 'ListPrice' in merged_prod.columns else 0.0
    max_cost = merged_prod['StandardCost'].max() if 'StandardCost' in merged_prod.columns else 0.0
    top_cat = cat_rev.sort_values(by='LineTotal', ascending=False).iloc[0]['Category'] if not cat_rev.empty else "N/A"
    top_subcat = subcat_rev.iloc[0]['Subcategory'] if not subcat_rev.empty else "N/A"
    
    i1.markdown(f"<div class='insight-box'><div class='insight-title'>🏆 Best Selling</div><div class='insight-value' style='font-size:13px;'>{str(best_sell_prod)[:20]}</div></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-box'><div class='insight-title'>💰 High Rev Product</div><div class='insight-value' style='font-size:13px;'>{str(highest_rev_prod)[:20]}</div></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-box'><div class='insight-title'>📈 Highest Price</div><div class='insight-value'>${max_price:,.0f}</div></div>", unsafe_allow_html=True)
    i4.markdown(f"<div class='insight-box'><div class='insight-title'>💲 Highest Cost</div><div class='insight-value'>${max_cost:,.0f}</div></div>", unsafe_allow_html=True)
    i5.markdown(f"<div class='insight-box'><div class='insight-title'>📦 Largest Category</div><div class='insight-value' style='font-size:14px;'>{top_cat}</div></div>", unsafe_allow_html=True)
    i6.markdown(f"<div class='insight-box'><div class='insight-title'>🎯 Best Subcategory</div><div class='insight-value' style='font-size:14px;'>{top_subcat}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🗂️ Product Directory")
    if not merged_prod.empty:
        search_prod = st.text_input("🔍 Search by Product Name...")
        table_df = merged_prod.copy()
        if search_prod:
            table_df = table_df[table_df['ProductName'].astype(str).str.contains(search_prod, case=False)]
        
        display_cols = [col for col in ['ProductID', 'ProductName', 'Category', 'Subcategory', 'Color', 'Size', 'StandardCost', 'ListPrice', 'FinishedGoodsFlag', 'SellStartDate'] if col in table_df.columns]
        st.dataframe(table_df[display_cols].head(100), use_container_width=True, hide_index=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Product Analytics Module | Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Training: **O7 Services**")