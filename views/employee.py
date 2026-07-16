import streamlit as st
import pandas as pd
import plotly.express as px
import os

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
        </style>
    """, unsafe_allow_html=True)

    st.title("👥 Employee Analytics Dashboard")
    st.subheader("Human Resources Operations & Insights")
    
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

    df_emp = load_smart('HumanResources.Employee')
    df_pay = load_smart('HumanResources.EmployeePayHistory')
    df_dept = load_smart('HumanResources.Department')

    tot_emp = len(df_emp) if not df_emp.empty else 0
    tot_dpt = len(df_dept) if not df_dept.empty else 0
    
    if not df_emp.empty and 'SickLeaveHours' in df_emp.columns and 'VacationHours' in df_emp.columns:
        avg_sick = df_emp['SickLeaveHours'].mean()
        avg_vac = df_emp['VacationHours'].mean()
    else:
        avg_sick = 0.0
        avg_vac = 0.0
        
    avg_sal = float(df_pay['Rate'].mean()) if not df_pay.empty and 'Rate' in df_pay.columns else 0.0

    st.divider()
    st.header("📊 HR Overview")
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(f"<div class='kpi-box'><p class='kpi-title'>👥 Total Employees</p><p class='kpi-value'>{tot_emp:,}</p></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-box'><p class='kpi-title'>🏢 Departments</p><p class='kpi-value'>{tot_dpt:,}</p></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-box'><p class='kpi-title'>💵 Avg Salary Rate</p><p class='kpi-value'>${avg_sal:,.2f}</p></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-box'><p class='kpi-title'>🤒 Avg Sick Leave</p><p class='kpi-value'>{avg_sick:,.0f} Hrs</p></div>", unsafe_allow_html=True)
    k5.markdown(f"<div class='kpi-box'><p class='kpi-title'>✈️ Avg Vacation</p><p class='kpi-value'>{avg_vac:,.0f} Hrs</p></div>", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("👔 Job Title Distribution")
        if not df_emp.empty and 'JobTitle' in df_emp.columns:
            job_counts = df_emp['JobTitle'].value_counts().nlargest(10).reset_index()
            job_counts.columns = ['Job Title', 'Count']
            fig_job = px.bar(job_counts, x='Count', y='Job Title', orientation='h', color_discrete_sequence=['#0066CC'])
            fig_job.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="")
            st.plotly_chart(fig_job, use_container_width=True)

    with c2:
        st.subheader("⚤ Gender Distribution")
        if not df_emp.empty and 'Gender' in df_emp.columns:
            gender_counts = df_emp['Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            fig_gender = px.pie(gender_counts, values='Count', names='Gender', hole=0.5, color_discrete_sequence=['#0A2540', '#0066CC'])
            fig_gender.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gender, use_container_width=True)

    st.divider()
    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("💍 Marital Status")
        if not df_emp.empty and 'MaritalStatus' in df_emp.columns:
            marital_counts = df_emp['MaritalStatus'].value_counts().reset_index()
            marital_counts.columns = ['Status', 'Count']
            fig_marital = px.pie(marital_counts, values='Count', names='Status', color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_marital.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_marital, use_container_width=True)

    with c4:
        st.subheader("💰 Salary Rate Distribution")
        if not df_pay.empty and 'Rate' in df_pay.columns:
            fig_sal = px.histogram(df_pay, x='Rate', nbins=20, color_discrete_sequence=['#0A2540'])
            fig_sal.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Hourly Rate ($)", yaxis_title="Number of Employees")
            st.plotly_chart(fig_sal, use_container_width=True)

    st.divider()
    st.header("🗂️ Employee Directory")
    if not df_emp.empty:
        cols_to_show = [col for col in ['BusinessEntityID', 'JobTitle', 'BirthDate', 'MaritalStatus', 'Gender', 'HireDate', 'VacationHours', 'SickLeaveHours'] if col in df_emp.columns]
        dir_df = df_emp[cols_to_show].copy()
        
        search_emp = st.text_input("🔍 Search by Job Title...")
        if search_emp:
            dir_df = dir_df[dir_df['JobTitle'].str.contains(search_emp, case=False, na=False)]
            
        st.dataframe(dir_df, use_container_width=True, hide_index=True)