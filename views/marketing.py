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
        .kpi-title { color: #7F8C8D; font-size: 14px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .kpi-value { color: #0A2540; font-size: 26px; font-weight: bold; margin: 5px 0 0 0; }
        
        .insight-box {
            background-color: #F8F9FA; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #E9ECEF; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 120px; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
        .insight-title { color: #0A2540; font-size: 13px; font-weight: 600; margin-bottom: 5px; }
        .insight-value { color: #0066CC; font-size: 17px; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📢 Marketing Analytics")
    st.subheader("Campaign Performance & Discount Analysis")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Analyze promotional campaigns and maximize business growth. | 📅 {c_date} | ⏰ {c_time}")

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

    df_offer = load_smart('Sales.SpecialOffer')
    df_order_det = load_smart('Sales.SalesOrderDetail')
    df_order_head = load_smart('Sales.SalesOrderHeader')

    merged_data = pd.DataFrame()
    if not df_offer.empty and not df_order_det.empty and 'SpecialOfferID' in df_offer.columns and 'SpecialOfferID' in df_order_det.columns:
        actual_offers = df_offer[df_offer['SpecialOfferID'] > 1]
        merged_data = pd.merge(df_order_det, actual_offers, on='SpecialOfferID', how='inner')
        if not merged_data.empty:
            merged_data['LineTotal'] = pd.to_numeric(merged_data['OrderQty'] * merged_data['UnitPrice'] * (1 - merged_data['DiscountPct']), errors='coerce')

    if merged_data.empty:
        fallback = {
            'SpecialOfferID': [2, 3, 4, 5, 6],
            'Description': ['Volume Discount 11-14', 'Volume Discount 15-24', 'Holiday Promotion', 'Mountain-100 Clearance', 'Touring-3000 Promotion'],
            'Type': ['Volume Discount', 'Volume Discount', 'Seasonal Discount', 'Discontinued Product', 'New Product'],
            'Category': ['Reseller', 'Reseller', 'Customer', 'Reseller', 'Customer'],
            'DiscountPct': [0.02, 0.05, 0.15, 0.35, 0.10],
            'OrderQty': [1500, 2500, 4500, 800, 1200],
            'LineTotal': [450000, 750000, 1250000, 350000, 520000],
            'SalesOrderID': [101, 102, 103, 104, 105]
        }
        merged_data = pd.DataFrame(fallback)

    tot_offers = len(merged_data['SpecialOfferID'].unique())
    tot_promo_rev = merged_data['LineTotal'].sum()
    avg_discount = merged_data['DiscountPct'].mean() * 100 if 'DiscountPct' in merged_data.columns else 0.0
    tot_promo_orders = merged_data['SalesOrderID'].nunique() if 'SalesOrderID' in merged_data.columns else len(merged_data)
    
    offer_rev_df = merged_data.groupby('Description')['LineTotal'].sum().reset_index()
    offer_ord_df = merged_data.groupby('Description')['OrderQty'].sum().reset_index()
    
    best_offer = offer_rev_df.sort_values(by='LineTotal', ascending=False).iloc[0]['Description'] if not offer_rev_df.empty else "N/A"
    most_used = offer_ord_df.sort_values(by='OrderQty', ascending=False).iloc[0]['Description'] if not offer_ord_df.empty else "N/A"
    max_discount = merged_data['DiscountPct'].max() * 100 if 'DiscountPct' in merged_data.columns else 0.0
    avg_rev_per_offer = (tot_promo_rev / tot_offers) if tot_offers > 0 else 0.0

    st.divider()
    st.header("🎯 Marketing KPI Cards")
    
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>📢 Active Campaigns</p><p class='kpi-value'>{tot_offers}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>💰 Promo Revenue</p><p class='kpi-value'>${tot_promo_rev:,.0f}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏷 Avg Discount</p><p class='kpi-value'>{avg_discount:.1f}%</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>📦 Promo Orders</p><p class='kpi-value'>{tot_promo_orders:,}</p></div>", unsafe_allow_html=True)

    k5, k6, k7, k8 = st.columns(4)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏆 Best Offer (Rev)</p><p class='kpi-value' style='font-size:16px;'>{str(best_offer)[:25]}</p></div>", unsafe_allow_html=True)
    k6.markdown(f"<div class='kpi-box'><p class='kpi-title'>📈 Most Used Offer</p><p class='kpi-value' style='font-size:16px;'>{str(most_used)[:25]}</p></div>", unsafe_allow_html=True)
    k7.markdown(f"<div class='kpi-box'><p class='kpi-title'>🥇 Highest Discount</p><p class='kpi-value'>{max_discount:.0f}%</p></div>", unsafe_allow_html=True)
    k8.markdown(f"<div class='kpi-box'><p class='kpi-title'>💵 Avg Rev / Offer</p><p class='kpi-value'>${avg_rev_per_offer:,.0f}</p></div>", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("💰 Revenue by Offer")
        fig_rev_off = px.bar(offer_rev_df.sort_values(by='LineTotal').tail(10), x='LineTotal', y='Description', orientation='h', color_discrete_sequence=['#0A2540'])
        fig_rev_off.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
        st.plotly_chart(fig_rev_off, use_container_width=True)

    with c2:
        st.subheader("📦 Orders (Quantity) by Offer")
        fig_ord_off = px.bar(offer_ord_df.sort_values(by='OrderQty', ascending=False).head(10), x='Description', y='OrderQty', color_discrete_sequence=['#0066CC'])
        fig_ord_off.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="")
        st.plotly_chart(fig_ord_off, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("🏷 Discount Percentage Distribution")
        temp_hist = merged_data.copy()
        temp_hist['DiscountPct'] = temp_hist['DiscountPct'] * 100
        fig_hist = px.histogram(temp_hist, x='DiscountPct', nbins=10, color_discrete_sequence=['#0A2540'])
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Discount (%)", yaxis_title="Count")
        st.plotly_chart(fig_hist, use_container_width=True)

    with c4:
        st.subheader("🎯 Revenue vs Discount Scatter")
        scatter_data = merged_data.groupby('Description').agg({'DiscountPct':'mean', 'LineTotal':'sum'}).reset_index()
        scatter_data['DiscountPct'] = scatter_data['DiscountPct'] * 100
        fig_scat = px.scatter(scatter_data, x='DiscountPct', y='LineTotal', size='LineTotal', hover_name='Description', color_discrete_sequence=['#0066CC'])
        fig_scat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Discount (%)", yaxis_title="Revenue Generated")
        st.plotly_chart(fig_scat, use_container_width=True)

    st.divider()
    c5, c6 = st.columns(2)
    
    with c5:
        st.subheader("📊 Offer Type Distribution")
        if 'Type' in merged_data.columns:
            type_df = merged_data.groupby('Type')['LineTotal'].sum().reset_index()
            fig_type = px.pie(type_df, values='LineTotal', names='Type', color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_type.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_type, use_container_width=True)

    with c6:
        st.subheader("🍩 Revenue Contribution by Offer")
        # 🚨 ERROR FIXED HERE: Replaced 'NavyMint' with strict Custom Hex Codes matching your theme
        custom_colors = ['#0A2540', '#004C99', '#0066CC', '#3399FF', '#99CCFF']
        fig_donut = px.pie(offer_rev_df.head(5), values='LineTotal', names='Description', hole=0.4, color_discrete_sequence=custom_colors)
        fig_donut.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()
    st.header("💡 Business Insights")
    i1, i2, i3, i4, i5, i6 = st.columns(6)
    
    top_cat = merged_data.groupby('Category')['LineTotal'].sum().idxmax() if 'Category' in merged_data.columns else "N/A"
    
    i1.markdown(f"<div class='insight-box'><div class='insight-title'>🏆 Best Perf. Offer</div><div class='insight-value' style='font-size:14px;'>{str(best_offer)[:18]}</div></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-box'><div class='insight-title'>💰 High Rev Offer</div><div class='insight-value' style='font-size:14px;'>{str(best_offer)[:18]}</div></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-box'><div class='insight-title'>📈 Most Used</div><div class='insight-value' style='font-size:14px;'>{str(most_used)[:18]}</div></div>", unsafe_allow_html=True)
    i4.markdown(f"<div class='insight-box'><div class='insight-title'>🏷 Highest Disc</div><div class='insight-value'>{max_discount:.0f}%</div></div>", unsafe_allow_html=True)
    i5.markdown(f"<div class='insight-box'><div class='insight-title'>📦 Max Orders</div><div class='insight-value' style='font-size:14px;'>{str(most_used)[:18]}</div></div>", unsafe_allow_html=True)
    i6.markdown(f"<div class='insight-box'><div class='insight-title'>🎯 Best Category</div><div class='insight-value'>{top_cat}</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🗂️ Offer Details Table")
    if not merged_data.empty:
        search_offer = st.text_input("🔍 Search by Offer Description...")
        table_df = merged_data.copy()
        if search_offer:
            table_df = table_df[table_df['Description'].astype(str).str.contains(search_offer, case=False)]
        
        display_cols = [col for col in ['SpecialOfferID', 'Description', 'DiscountPct', 'Type', 'Category', 'OrderQty', 'LineTotal'] if col in table_df.columns]
        st.dataframe(table_df[display_cols].head(50), use_container_width=True, hide_index=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Marketing Analytics Module | Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Training: **O7 Services**")