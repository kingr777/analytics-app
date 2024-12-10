import streamlit as st
import pandas as pd
from models.user import User
from utils.analysis import DataAnalyzer
from utils.visualization import DataVisualizer

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            user = User()
            success, user_data = user.verify_user(username, password)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with col2:
        if st.button("Register"):
            st.session_state['register'] = True
            st.rerun()

def register_page():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    
    if st.button("Create Account"):
        user = User()
        success, message = user.create_user(username, password, email)
        if success:
            st.success(message)
            st.session_state['register'] = False
            st.rerun()
        else:
            st.error(message)
    
    if st.button("Back to Login"):
        st.session_state['register'] = False
        st.rerun()

def main_dashboard():
    st.set_page_config(layout="wide")
    st.title("Advanced Data Analysis Dashboard")
    
    user = User()
    
    # Sidebar
    with st.sidebar:
        st.title(f"Welcome, {st.session_state['username']}!")
        uploaded_file = st.file_uploader("Upload Data", type=['csv', 'xlsx'])
        
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Initialize analyzers
            analyzer = DataAnalyzer(df)
            visualizer = DataVisualizer(df)
            
            # Data Overview
            st.subheader("Data Overview")
            st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            
            # Analysis Options
            analysis_type = st.selectbox(
                "Select Analysis Type",
                ["Basic Statistics", "Correlation Analysis", "Time Series Analysis", "PCA Analysis"]
            )
            
            if analysis_type == "Basic Statistics":
                col = st.selectbox("Select Column", df.select_dtypes(include=['number']).columns)
                stats = analyzer.basic_stats(col)
                st.write(stats)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(visualizer.create_histogram(col), use_container_width=True)
                with col2:
                    st.plotly_chart(visualizer.create_box_plot(col), use_container_width=True)
            
            elif analysis_type == "Correlation Analysis":
                numeric_cols = df.select_dtypes(include=['number']).columns
                corr_matrix = analyzer.correlation_analysis(numeric_cols)
                st.plotly_chart(visualizer.create_heatmap(corr_matrix), use_container_width=True)
            
            # Visualization Section
            st.subheader("Custom Visualizations")
            viz_type = st.selectbox(
                "Select Visualization",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "3D Scatter"]
            )
            
            # Create visualizations based on selection
            if viz_type == "Bar Chart":
                x_col = st.selectbox("X-axis", df.columns)
                y_col = st.selectbox("Y-axis", df.select_dtypes(include=['number']).columns)
                st.plotly_chart(visualizer.create_bar_chart(x_col, y_col), use_container_width=True)
            
            elif viz_type == "3D Scatter":
                x_col = st.selectbox("X-axis", df.select_dtypes(include=['number']).columns)
                y_col = st.selectbox("Y-axis", df.select_dtypes(include=['number']).columns)
                z_col = st.selectbox("Z-axis", df.select_dtypes(include=['number']).columns)
                color_col = st.selectbox("Color by", [None] + list(df.columns))
                st.plotly_chart(visualizer.create_3d_scatter(x_col, y_col, z_col, color_col), use_container_width=True)
            
            # Save data option
            if st.button("Save Analysis"):
                data_name = st.text_input("Enter a name for this dataset")
                if data_name:
                    user.save_user_data(st.session_state['username'], data_name, df.to_dict())
                    st.success("Data saved successfully!")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'register' not in st.session_state:
        st.session_state['register'] = False
    
    if st.session_state['logged_in']:
        main_dashboard()
    elif st.session_state['register']:
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()