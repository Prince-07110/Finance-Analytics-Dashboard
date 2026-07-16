import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    st.markdown("""
        <style>
        .info-card {
            background-color: #FFFFFF; border-radius: 10px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); border-left: 5px solid #0066CC;
            margin-bottom: 20px; border: 1px solid #EAEAEA;
        }
        .info-title { color: #0A2540; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
        .info-text { color: #7F8C8D; font-size: 14px; }
        
        .tech-box {
            background-color: #F8F9FA; border-radius: 8px; padding: 15px; text-align: center;
            border: 1px solid #E9ECEF; font-weight: 600; color: #0A2540;
            margin-bottom: 15px; transition: transform 0.3s;
        }
        .tech-box:hover { transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        
        .workflow-box {
            background-color: #0A2540; color: #FFFFFF; border-radius: 8px; padding: 15px;
            text-align: center; font-weight: bold; margin: 10px 0;
        }
        .arrow { text-align: center; font-size: 24px; color: #0066CC; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("ℹ️ About Finance Analytics Dashboard")
    st.subheader("Enterprise Business Intelligence Dashboard")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"A professional Business Intelligence dashboard built using the Microsoft AdventureWorks dataset. | 📅 {c_date} | ⏰ {c_time}")

    st.divider()
    st.header("📋 Project Overview")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='info-card'><div class='info-title'>Project Name</div><div class='info-text'>Finance Analytics Dashboard</div></div>", unsafe_allow_html=True)
    c2.markdown("<div class='info-card'><div class='info-title'>Project Type</div><div class='info-text'>Business Intelligence Dashboard</div></div>", unsafe_allow_html=True)
    c3.markdown("<div class='info-card'><div class='info-title'>Domain</div><div class='info-text'>Data Analytics & Visualization</div></div>", unsafe_allow_html=True)
    
    c4, c5 = st.columns([1, 2])
    c4.markdown("<div class='info-card'><div class='info-title'>Dataset Used</div><div class='info-text'>Microsoft AdventureWorks DB</div></div>", unsafe_allow_html=True)
    c5.markdown("<div class='info-card'><div class='info-title'>Primary Objective</div><div class='info-text'>Transform raw enterprise data into meaningful business insights using interactive, data-driven dashboards to aid executive decision making.</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🎯 Project Objectives")
    obj1, obj2, obj3, obj4 = st.columns(4)
    obj1.markdown("<div class='tech-box'>💰 Analyze Company Revenue</div>", unsafe_allow_html=True)
    obj2.markdown("<div class='tech-box'>👨 Monitor Employee Performance</div>", unsafe_allow_html=True)
    obj3.markdown("<div class='tech-box'>📈 Analyze Sales Trends</div>", unsafe_allow_html=True)
    obj4.markdown("<div class='tech-box'>📢 Evaluate Marketing Campaigns</div>", unsafe_allow_html=True)
    
    obj5, obj6, obj7, obj8 = st.columns(4)
    obj5.markdown("<div class='tech-box'>📦 Analyze Product Performance</div>", unsafe_allow_html=True)
    obj6.markdown("<div class='tech-box'>🌍 Compare Territory Performance</div>", unsafe_allow_html=True)
    obj7.markdown("<div class='tech-box'>👥 Understand Customer Behaviour</div>", unsafe_allow_html=True)
    obj8.markdown("<div class='tech-box'>🏢 Build Enterprise BI Dashboard</div>", unsafe_allow_html=True)

    st.divider()
    st.header("💻 Technology Stack")
    t1, t2, t3, t4 = st.columns(4)
    t1.markdown("<div class='tech-box'>🐍 Python</div>", unsafe_allow_html=True)
    t2.markdown("<div class='tech-box'>👑 Streamlit</div>", unsafe_allow_html=True)
    t3.markdown("<div class='tech-box'>🐼 Pandas</div>", unsafe_allow_html=True)
    t4.markdown("<div class='tech-box'>🔢 NumPy</div>", unsafe_allow_html=True)
    
    t5, t6, t7, t8 = st.columns(4)
    t5.markdown("<div class='tech-box'>📊 Plotly</div>", unsafe_allow_html=True)
    t6.markdown("<div class='tech-box'>📉 Matplotlib</div>", unsafe_allow_html=True)
    t7.markdown("<div class='tech-box'>📗 OpenPyXL</div>", unsafe_allow_html=True)
    t8.markdown("<div class='tech-box'>🗄️ AdventureWorks DB</div>", unsafe_allow_html=True)

    st.divider()
    st.header("🧩 Project Modules")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.write("🏠 **Home Dashboard**")
        st.write("👨 **Employee Analytics**")
    with m2:
        st.write("💰 **Finance Analytics**")
        st.write("📈 **Sales Analytics**")
    with m3:
        st.write("📢 **Marketing Analytics**")
        st.write("📦 **Product Analytics**")
    with m4:
        st.write("🌍 **Territory Analytics**")
        st.write("👥 **Customer Analytics**")

    st.divider()
    st.header("🗂️ Dataset Information")
    dataset_info = pd.DataFrame({
        "Dataset Name": ["SalesOrderHeader", "SalesOrderDetail", "Employee", "Product", "Customer", "SalesTerritory"],
        "Category": ["Sales", "Sales", "HR", "Production", "Sales", "Sales"],
        "Purpose": ["Order Dates, Revenue, Taxes", "Quantities, Line Totals", "Staff Demographics, Jobs", "Inventory, Costs, Pricing", "Client Purchase IDs", "Regional Performance"],
        "Rows": ["31,465", "121,317", "290", "504", "19,820", "10"],
        "Columns": ["26", "11", "16", "25", "7", "10"]
    })
    st.dataframe(dataset_info, use_container_width=True, hide_index=True)

    st.divider()
    st.header("✨ Project Features")
    f1, f2, f3, f4, f5 = st.columns(5)
    f1.markdown("<div class='tech-box'>⚙️ Interactive UI</div>", unsafe_allow_html=True)
    f2.markdown("<div class='tech-box'>📱 Responsive Layout</div>", unsafe_allow_html=True)
    f3.markdown("<div class='tech-box'>🔍 Dynamic Filters</div>", unsafe_allow_html=True)
    f4.markdown("<div class='tech-box'>📊 Interactive Charts</div>", unsafe_allow_html=True)
    f5.markdown("<div class='tech-box'>💡 Business Insights</div>", unsafe_allow_html=True)

    st.divider()
    st.header("🔄 Project Workflow")
    w1, w2, w3 = st.columns([1, 2, 1])
    with w2:
        st.markdown("<div class='workflow-box'>🗄️ AdventureWorks Dataset</div>", unsafe_allow_html=True)
        st.markdown("<div class='arrow'>⬇</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>🧹 Data Cleaning & Preprocessing</div>", unsafe_allow_html=True)
        st.markdown("<div class='arrow'>⬇</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>⚙️ Data Analysis & Logic Building</div>", unsafe_allow_html=True)
        st.markdown("<div class='arrow'>⬇</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>📊 Interactive Dashboard UI</div>", unsafe_allow_html=True)
        st.markdown("<div class='arrow'>⬇</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>💡 Actionable Business Insights</div>", unsafe_allow_html=True)

    st.divider()
    st.header("🚀 Future Scope")
    fs1, fs2 = st.columns(2)
    with fs1:
        st.write("✅ **Artificial Intelligence Integration**")
        st.write("✅ **Machine Learning Predictions**")
        st.write("✅ **Sales & Revenue Forecasting**")
        st.write("✅ **Employee Attrition Prediction**")
    with fs2:
        st.write("✅ **Customer Segmentation using ML**")
        st.write("✅ **Interactive Geospatial Maps**")
        st.write("✅ **Real-Time Database Integration**")
        st.write("✅ **Cloud Deployment (AWS/Azure)**")

    st.divider()
    st.header("👨‍💻 Developer Information")
    d1, d2, d3, d4 = st.columns(4)
    d1.markdown("<div class='info-card'><div class='info-title'>Developer Name</div><div class='info-text'>Prince</div></div>", unsafe_allow_html=True)
    d2.markdown("<div class='info-card'><div class='info-title'>Department</div><div class='info-text'>Electronics & Comm. Engineering</div></div>", unsafe_allow_html=True)
    d3.markdown("<div class='info-card'><div class='info-title'>College</div><div class='info-text'>Lyallpur Khalsa College Technical Campus</div></div>", unsafe_allow_html=True)
    d4.markdown("<div class='info-card'><div class='info-title'>Industrial Training</div><div class='info-text'>O7 Services</div></div>", unsafe_allow_html=True)

    st.divider()
    st.success("🎉 **Acknowledgement:** This project was developed as part of industrial training to demonstrate practical knowledge of Business Intelligence, Data Analytics, and Enterprise Dashboard Development using the Microsoft AdventureWorks dataset.")

    st.markdown("<hr style='margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: #0A2540; color: white; padding: 20px; border-radius: 10px; text-align: center;'>
            <h4 style='margin: 0; color: #FFFFFF;'>Finance Analytics Dashboard (Version 1.0)</h4>
            <p style='margin: 5px 0 0 0; color: #7F8C8D; font-size: 0.9rem;'>Developed by <b>Prince</b> | Lyallpur Khalsa College Technical Campus | Training at O7 Services</p>
            <p style='margin: 5px 0 0 0; color: #7F8C8D; font-size: 0.8rem;'>© 2026 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)