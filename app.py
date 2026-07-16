import streamlit as st
from datetime import datetime

# Import all modules safely
from views import home, employee, finance, sales, marketing, product, territory, customer, dataset, about

st.set_page_config(
    page_title="Finance Analytics Dashboard",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GLOBAL ENTERPRISE THEME (MOBILE COMPATIBLE)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #F4F7F6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Adjusted margin-top from -40px to 10px so it doesn't hide the mobile arrow */
    .top-bar {
        background-color: #0A2540;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .top-title { font-size: 20px; font-weight: bold; margin: 0; }
    .top-subtitle { font-size: 11px; color: #99CCFF; margin: 0; }
    .top-user { font-size: 13px; font-weight: 500; text-align: right;}
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAEAEA;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    
    .sidebar-footer {
        font-size: 12px;
        color: #7F8C8D;
        text-align: center;
        padding-top: 20px;
        border-top: 1px solid #EAEAEA;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # TOP HEADER WITH SAFE SPACING
    c_date = datetime.now().strftime("%b %d, %Y")
    c_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
        <div class="top-bar">
            <div>
                <p class="top-title">💠 Finance Analytics Dashboard</p>
                <p class="top-subtitle">AdventureWorks Business Intelligence System</p>
            </div>
            <div class="top-user">
                <p style="margin:0;">👤 Welcome, <b>Prince</b> 👋</p>
                <p style="margin:0; font-size:11px; color:#99CCFF;">📅 {c_date} | ⏰ {c_time}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
        
    # SIDEBAR
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2936/2936690.png", width=50)
        st.title("Enterprise BI")
        st.caption("Data Intelligence Portal")
        st.divider()
        
        search = st.text_input("🔍 Search Module...", placeholder="e.g. Sales, HR...")
        
        menu_items = {
            "🏠 Home": "Home", 
            "👨‍💼 Employee Analytics": "Employee Analytics", 
            "💰 Finance Analytics": "Finance Analytics", 
            "📈 Sales Analytics": "Sales Analytics", 
            "📢 Marketing Analytics": "Marketing Analytics", 
            "📦 Product Analytics": "Product Analytics", 
            "🌍 Territory Analytics": "Territory Analytics", 
            "👥 Customer Analytics": "Customer Analytics", 
            "🗂️ Dataset Overview": "Dataset Overview", 
            "ℹ️ About Project": "About Project"
        }
        
        if search:
            filtered_menu = {k: v for k, v in menu_items.items() if search.lower() in k.lower()}
        else:
            filtered_menu = menu_items
            
        st.write("**📌 Navigation**")
        
        for display_name, internal_name in filtered_menu.items():
            btn_type = "primary" if st.session_state.current_page == internal_name else "secondary"
            if st.button(display_name, key=internal_name, use_container_width=True, type=btn_type):
                st.session_state.current_page = internal_name
                st.rerun()
                
        st.markdown("""
            <div class="sidebar-footer">
                <b>Version 1.0</b><br>
                Dev: Prince<br>
                LKCTC | O7 Services
            </div>
        """, unsafe_allow_html=True)

    # PAGE ROUTING
    if st.session_state.current_page == "Home":
        home.show()
    elif st.session_state.current_page == "Employee Analytics":
        employee.show()
    elif st.session_state.current_page == "Finance Analytics":
        finance.show()
    elif st.session_state.current_page == "Sales Analytics":
        sales.show()
    elif st.session_state.current_page == "Marketing Analytics":
        marketing.show()
    elif st.session_state.current_page == "Product Analytics":
        product.show()
    elif st.session_state.current_page == "Territory Analytics":
        territory.show()
    elif st.session_state.current_page == "Customer Analytics":
        customer.show()
    elif st.session_state.current_page == "Dataset Overview":
        dataset.show()
    elif st.session_state.current_page == "About Project":
        about.show()
    else:
        st.error("Page not found!")

    # GLOBAL FOOTER
    st.markdown("<hr style='margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #7F8C8D; font-size: 13px; padding-bottom: 20px;'>
            <b>Finance Analytics Dashboard v1.0</b> | Built by Prince<br>
            Lyallpur Khalsa College Technical Campus | Industrial Training at O7 Services<br>
            © 2026 All Rights Reserved
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
