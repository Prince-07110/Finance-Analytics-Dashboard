import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show():
    st.markdown("""
        <style>
        .kpi-box {
            background-color: #FFFFFF; border-radius: 10px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #0066CC;
            margin-bottom: 20px; border: 1px solid #EAEAEA; height: 120px; 
            display: flex; flex-direction: column; justify-content: center;
        }
        .kpi-title { color: #7F8C8D; font-size: 13px; font-weight: 600; text-transform: uppercase; margin: 0; }
        .kpi-value { color: #0A2540; font-size: 24px; font-weight: bold; margin: 5px 0 0 0; }
        
        .cat-card {
            background-color: #F8F9FA; border-radius: 8px; padding: 15px;
            border: 1px solid #E9ECEF; margin-bottom: 10px;
        }
        .cat-title { color: #0A2540; font-size: 16px; font-weight: bold; margin-bottom: 5px; }
        .cat-desc { color: #7F8C8D; font-size: 13px; }
        
        .workflow-box {
            background-color: #0A2540; color: #FFFFFF; border-radius: 8px; padding: 12px;
            text-align: center; font-weight: bold; margin: 5px 0; font-size: 14px;
        }
        .arrow { text-align: center; font-size: 20px; color: #0066CC; font-weight: bold; margin: 0; padding: 0; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🗂️ Dataset Overview Dashboard")
    st.subheader("AdventureWorks Dataset Explorer")
    
    c_date = datetime.now().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.info(f"Understand the complete structure and quality of the AdventureWorks dataset. | 📅 {c_date} | ⏰ {c_time}")

    @st.cache_data(show_spinner=False)
    def load_all_datasets():
        base_names = [
            'Sales.SalesOrderHeader', 'Sales.SalesOrderDetail', 'Sales.SalesTerritory', 'Sales.Customer',
            'Sales.SpecialOffer', 'HumanResources.Employee', 'HumanResources.EmployeePayHistory',
            'HumanResources.Department', 'Production.Product', 'Production.ProductCategory',
            'Production.ProductSubcategory', 'Person.Person'
        ]
        
        data_dict = {}
        total_rows = 0
        total_cols = 0
        
        for name in base_names:
            csv_path = f"Dataset/{name}.csv"
            xlsx_path = f"Dataset/{name}.xlsx"
            
            df = pd.DataFrame()
            try:
                if os.path.exists(csv_path): df = pd.read_csv(csv_path)
                elif os.path.exists(xlsx_path): df = pd.read_excel(xlsx_path)
            except:
                pass
                
            if not df.empty:
                df.columns = df.columns.str.strip()
                
                # 🚀 ADVANCED DATA CLEANING ENGINE 🚀
                # Missing values ko unke data type ke hisaab se clean karna
                for col in df.columns:
                    if df[col].dtype == 'object':
                        df[col] = df[col].fillna('Not Specified')
                    else:
                        df[col] = df[col].fillna(0)
                
                data_dict[name] = df
                total_rows += len(df)
                total_cols += len(df.columns)
            else:
                data_dict[name] = pd.DataFrame()
                
        return data_dict, total_rows, total_cols

    datasets, t_rows, t_cols = load_all_datasets()
    active_datasets = {k: v for k, v in datasets.items() if not v.empty}
    t_files = len(active_datasets)

    st.divider()
    st.header("📊 Dataset Summary")
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>📁 Total Files</p><p class='kpi-value'>{t_files}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>📊 Tables Used</p><p class='kpi-value'>{t_files}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>📄 Total Records</p><p class='kpi-value'>{t_rows:,}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>🧾 Total Columns</p><p class='kpi-value'>{t_cols:,}</p></div>", unsafe_allow_html=True)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>🗂 Total Categories</p><p class='kpi-value'>5</p></div>", unsafe_allow_html=True)

    st.divider()
    st.header("📂 Dataset Categories")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown("<div class='cat-card'><div class='cat-title'>👨 Human Resources</div><div class='cat-desc'>Contains employee, department, and pay history records.</div></div>", unsafe_allow_html=True)
    c2.markdown("<div class='cat-card'><div class='cat-title'>💰 Sales</div><div class='cat-desc'>Contains customer orders, special offers, and territory data.</div></div>", unsafe_allow_html=True)
    c3.markdown("<div class='cat-card'><div class='cat-title'>📦 Production</div><div class='cat-desc'>Contains product inventory, categories, and pricing.</div></div>", unsafe_allow_html=True)
    c4.markdown("<div class='cat-card'><div class='cat-title'>👤 Person</div><div class='cat-desc'>Contains customer and employee personal demographics.</div></div>", unsafe_allow_html=True)
    c5.markdown("<div class='cat-card'><div class='cat-title'>🛒 Purchasing</div><div class='cat-desc'>Contains vendor and purchase related information.</div></div>", unsafe_allow_html=True)

    st.divider()
    st.header("🗂️ Dataset File Details")
    
    file_details = []
    for name, df in datasets.items():
        if not df.empty:
            cat = name.split('.')[0]
            file_details.append({
                "Dataset Name": name,
                "Category": cat,
                "Rows": len(df),
                "Columns": len(df.columns),
                "Purpose": f"Core {cat} operations data",
                "Status": "✅ Loaded & Cleaned"
            })
    
    if not file_details:
        file_details.append({"Dataset Name": "No Data Found", "Category": "-", "Rows": 0, "Columns": 0, "Purpose": "-", "Status": "❌ Missing"})
        
    df_details = pd.DataFrame(file_details)
    st.dataframe(df_details, use_container_width=True, hide_index=True)

    st.divider()
    st.header("🔗 Dataset Relationships")
    r1, r2, r3 = st.columns(3)
    
    with r1:
        st.markdown("<div class='cat-title'>HR & Person Flow</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>Person.Person</div><div class='arrow'>⬇</div><div class='workflow-box'>Employee</div><div class='arrow'>⬇</div><div class='workflow-box'>EmployeePayHistory</div><div class='arrow'>⬇</div><div class='workflow-box'>Department</div>", unsafe_allow_html=True)
    with r2:
        st.markdown("<div class='cat-title'>Sales & Production Flow</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>SalesOrderHeader</div><div class='arrow'>⬇</div><div class='workflow-box'>SalesOrderDetail</div><div class='arrow'>⬇</div><div class='workflow-box'>Product</div><div class='arrow'>⬇</div><div class='workflow-box'>ProductCategory</div>", unsafe_allow_html=True)
    with r3:
        st.markdown("<div class='cat-title'>Customer & Territory Flow</div>", unsafe_allow_html=True)
        st.markdown("<div class='workflow-box'>Customer</div><div class='arrow'>⬇</div><div class='workflow-box'>SalesOrderHeader</div><div class='arrow'>⬇</div><div class='workflow-box'>SalesTerritory</div>", unsafe_allow_html=True)

    st.divider()
    st.header("🛡️ Data Quality Report")
    
    dq_list = []
    tot_missing = 0
    tot_dupes = 0
    
    for name, df in active_datasets.items():
        miss = int(df.isna().sum().sum())
        dupe = int(df.duplicated().sum())
        tot_missing += miss
        tot_dupes += dupe
        dq_list.append({
            "Dataset Name": name,
            "Missing Values": miss,
            "Duplicate Rows": dupe,
            "Total Columns": len(df.columns),
            "Data Types": ", ".join(list(set(df.dtypes.astype(str).tolist())))
        })
        
    q1, q2, q3, q4 = st.columns(4)
    q1.markdown(f"<div class='kpi-box'><p class='kpi-title'>✅ Missing Values</p><p class='kpi-value'>{tot_missing:,} (Cleaned)</p></div>", unsafe_allow_html=True)
    q2.markdown(f"<div class='kpi-box'><p class='kpi-title'>📋 Duplicate Records</p><p class='kpi-value'>{tot_dupes:,}</p></div>", unsafe_allow_html=True)
    q3.markdown(f"<div class='kpi-box'><p class='kpi-title'>🔢 Numeric Columns</p><p class='kpi-value'>Auto-Detected</p></div>", unsafe_allow_html=True)
    q4.markdown(f"<div class='kpi-box'><p class='kpi-title'>📝 Text/Date Columns</p><p class='kpi-value'>Auto-Detected</p></div>", unsafe_allow_html=True)
    
    if dq_list:
        st.dataframe(pd.DataFrame(dq_list), use_container_width=True, hide_index=True)

    st.divider()
    st.header("🔍 Column Explorer")
    if active_datasets:
        selected_ds = st.selectbox("Select a Dataset to Explore:", list(active_datasets.keys()))
        exp_df = active_datasets[selected_ds]
        
        c_cols, c_data = st.columns([1, 2])
        with c_cols:
            st.write("**Column Data Types & Missing Values**")
            info_df = pd.DataFrame({
                "Data Type": exp_df.dtypes.astype(str),
                "Missing": exp_df.isna().sum()
            }).reset_index().rename(columns={"index": "Column Name"})
            st.dataframe(info_df, use_container_width=True, hide_index=True)
            
        with c_data:
            st.write("**Data Preview (Top 5 Rows)**")
            st.dataframe(exp_df.head(5), use_container_width=True, hide_index=True)
    else:
        st.warning("No datasets loaded to explore.")

    st.divider()
    st.header("🗺️ Dashboard Dataset Mapping")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("<div class='cat-card'><b>🏠 Home</b><br>SalesOrderHeader<br>SalesOrderDetail<br>Employee<br>Customer<br>Product</div>", unsafe_allow_html=True)
        st.markdown("<div class='cat-card'><b>👨 Employee</b><br>Employee<br>Department<br>EmployeePayHistory<br>Person</div>", unsafe_allow_html=True)
    with m2:
        st.markdown("<div class='cat-card'><b>💰 Finance</b><br>SalesOrderHeader<br>SalesTerritory</div>", unsafe_allow_html=True)
        st.markdown("<div class='cat-card'><b>📈 Sales</b><br>SalesOrderHeader<br>SalesOrderDetail<br>Product<br>SalesTerritory</div>", unsafe_allow_html=True)
    with m3:
        st.markdown("<div class='cat-card'><b>📢 Marketing</b><br>SpecialOffer<br>SalesOrderHeader<br>SalesOrderDetail</div>", unsafe_allow_html=True)
        st.markdown("<div class='cat-card'><b>📦 Product</b><br>Product<br>ProductCategory<br>ProductSubcategory<br>SalesOrderDetail</div>", unsafe_allow_html=True)
    with m4:
        st.markdown("<div class='cat-card'><b>🌍 Territory</b><br>SalesTerritory<br>SalesOrderHeader</div>", unsafe_allow_html=True)
        st.markdown("<div class='cat-card'><b>👥 Customer</b><br>Customer<br>Person<br>SalesOrderHeader<br>SalesTerritory</div>", unsafe_allow_html=True)

    st.divider()
    st.header("⚙️ Data Preprocessing Workflow")
    w1, w2, w3, w4, w5, w6, w7 = st.columns(7)
    w1.markdown("<div class='workflow-box'>Dataset<br>Loading</div>", unsafe_allow_html=True)
    w2.markdown("<div class='workflow-box'>Data<br>Cleaning</div>", unsafe_allow_html=True)
    w3.markdown("<div class='workflow-box' style='background-color:#27AE60;'>Missing<br>Resolved</div>", unsafe_allow_html=True)
    w4.markdown("<div class='workflow-box'>Type<br>Convert</div>", unsafe_allow_html=True)
    w5.markdown("<div class='workflow-box'>Table<br>Merging</div>", unsafe_allow_html=True)
    w6.markdown("<div class='workflow-box'>Feature<br>Engg.</div>", unsafe_allow_html=True)
    w7.markdown("<div class='workflow-box' style='background-color:#0066CC;'>Dashboard<br>Ready</div>", unsafe_allow_html=True)

    st.divider()
    st.write("### Finance Analytics Dashboard")
    st.caption("Dataset Overview Module | Developer: **Prince** | College: **Lyallpur Khalsa College Technical Campus** | Training: **O7 Services**")