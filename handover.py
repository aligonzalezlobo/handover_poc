import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    """
    Load the dataset from the given file path.
    """
    return pd.read_csv(file_path)

def main():
    # Load the dataset
    data = load_data("final_data5.csv")
    time_data = load_data("top_client_data.csv")
    financial_data = load_data("financial_tool.csv")

    # Set page configuration
    st.set_page_config(
        page_title="CLIENTCO - Clients Analytics, Sales Team Tool",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Increase the maximum number of elements allowed to be styled
    pd.set_option("styler.render.max_elements", 5989816)

    # Create sidebar navigation for tabs
    tab = st.sidebar.radio("Navigation", ["Home Page", "AI Client Ranking", "Client Deep-dive","Financial Tool"])

    # At the bottom of the sidebar
    with st.sidebar:
        for _ in range(100): 
            st.empty()
        logo_image2 = "images/image2.png"
        st.image(logo_image2, use_column_width=True)


    if tab == "Home Page":

        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image4.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.write("\n")
            st.title("Welcome to Sales Team Tool - CLIENTCO")
        
        st.write("\n")

        intro_text = """
        This is a churn prevention tool designed to empower sales teams with insights and analytics to proactively identify and address potential customer churn. The application provides sales professionals with the means to forecast which customers are at risk of churning, highlight those whose retention is critical, and strategize on salvaging sales figures by winning back certain customers. The tool features several tabs, each offering unique functionalities:

        - **AI Client Ranking**: This tab offers a fundamental analysis of customers, ranking them based on various metrics such as churn probability (as determined by our Machine Learning model), total sales return (the total amount spent by the customer on our products), and a priority metric. The priority metric is computed using a weighted average between different metrics to prioritize some customers over others, based on their potential impact on the business.

        - **Clients Deep-Dive**: This section provides an in-depth analysis of individual customer metrics that are vital for sales teams to understand customer's profiles in order to make informed decisions. It allows for a detailed examination of the factors influencing client's behavior and churn risk.

        - **Finance Tool**: A practical tool that enables sales teams to input client data an available budget to project potential sales recovery based on historical sales performance. This feature assists in financial planning and setting realistic targets for customer retention and sales recovery efforts.

        Sales teams can explore and familiarize themselves with these tabs to make better-informed decisions quickly and efficiently.
        """
        
        st.write(intro_text)

        st.write("\n") 
        st.write("\n")

        st.subheader("**CLIENTCO over the last two years**")

        # Calculate basic statistics
        total_clients = data['client_id'].nunique()
        total_sales = data['nb_orders'].sum()
        sales_net_revenue = data['tot_sales_net'].sum()
        number_branches = data['branch_id'].nunique()

        # Display basic statistics
        st.markdown(f"""
        <style>
            .metric-box {{
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
            }}
            .metric-header {{
                font-size: 16px;
                margin-bottom: 5px;
            }}
            .blue-box {{
                border-color: blue;
            }}
            .red-box {{
                border-color: red;
            }}
            .green-box {{
                border-color: green;
            }}
            .purple-box {{
                border-color: purple;
            }}
        </style>
        <div class="metric-box blue-box">
            <div class="metric-header" style="color: blue;">Total Clients</div>
            <h2>{total_clients}</h2>
        </div>
        <div class="metric-box red-box">
            <div class="metric-header" style="color: red;">Total Sales</div>
            <h2>{total_sales}</h2>
        </div>
        <div class="metric-box green-box">
            <div class="metric-header" style="color: green;">Net Revenue</div>
            <h2>${sales_net_revenue:,.2f}</h2>
        </div>
        <div class="metric-box purple-box">
            <div class="metric-header" style="color: purple;">Total Branches</div>
            <h2>{number_branches}</h2>
        </div>
        """, unsafe_allow_html=True)
    

    elif tab == "AI Client Ranking":
        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image3.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.title("CLIENTCO - AI Powered Client Ranking")
            st.subheader("Clients Analytics Tool")
        
        st.write("\n")

        st.write("This tab offers a fundamental analysis of customers, ranking them based on various metrics such as churn probability (as determined by our Machine Learning model), total sales return (the total amount spent by the customer on our products), and a priority metric. The priority metric is a formula that uses weighted averages to prioritize some customers over others, based on their potential impact on the business.")

        st.write("\n")

        # Get unique branches from the dataset
        branches = ['All'] + data['branch_id'].unique().tolist()

        # Create selectbox for branch selection
        selected_branch = st.selectbox("Select Branch", branches, index=0)  # Set "All" as default option

        # Filter data based on selected branch
        if selected_branch == "All":
            filtered_data = data
        else:
            filtered_data = data[data['branch_id'] == selected_branch]

        # Rename and select columns
        display_columns = {
            'client_id': 'Client ID',
            'branch_id': 'Branch ID',
            'priority_score':'Priority Score',
            'churn_probability': 'Probability of Churn',
            'tot_sales_net': 'Total Net Sales',
            'avg_freq_orders': 'Frequency Orders',
            'lag_day_last': 'Days since Last Order',
            'pref_cont_method': 'Preferred Way of Contact',
            'client_type' : 'client_type'
        }

        filtered_data = filtered_data.rename(columns=display_columns)[display_columns.values()]

        filtered_data['Frequency Orders'] = filtered_data['Frequency Orders'].round(2)

        filtered_data['Priority Score'] = filtered_data['Priority Score'].round(2)

        filtered_data['Total Net Sales'] = filtered_data['Total Net Sales'].round(2)

        filtered_data['Probability of Churn'] = filtered_data['Probability of Churn']*100

        filtered_data['Probability of Churn'] = filtered_data['Probability of Churn'].round(2)

        # Filter clients based on type
        client_types = ['Recurrent', 'Occasional', 'New']
        selected_client_types = st.multiselect('Filter by Client Type', client_types, default=client_types)

        # Map client type to the respective value
        type_mapping = {
            'Recurrent': 'recurrent_client',
            'Occasional': 'occasional_client',
            'New': 'new_client'
        }

        # Filter data based on selected client types
        filtered_data = filtered_data[filtered_data['client_type'].isin([type_mapping[type_] for type_ in selected_client_types])]

        # Remove the 'client_type' column from the displayed data
        filtered_data = filtered_data.drop(columns=['client_type'])

        # Sort data by 'Probability of Churn' and 'Total Sales Net'
        sort_by = st.selectbox("Sort by", ["", "Priority Score", "Probability of Churn", "Total Net Sales"])
        if sort_by:
            if sort_by == "Priority Score":
                filtered_data = filtered_data.sort_values(by="Priority Score", ascending=False)
            elif sort_by == "Probability of Churn":
                filtered_data = filtered_data.sort_values(by="Probability of Churn", ascending=False)
            elif sort_by == "Total Net Sales":
                filtered_data = filtered_data.sort_values(by="Total Net Sales", ascending=False)

        # Display filtered data
        st.write("Clients of the selected branch:")
        st.write(filtered_data)

        st.write("\n")
        st.write("\n")

        # After displaying the filtered data table
        st.subheader("Functionalities explanations:")

        st.markdown("""
        - **Branch Filter**: Filter that allows the filtering by branch. Each sales manager can focus on their specific branch or on the company as a whole.
        - **Customer Filter**: Clients are segmented into three different buckets: new customers (did their first order in the last month), occasional customers (did 2 or less orders), recurrent buyers (rest of the clients, considered as loyal clients).
        - **Sort By Filter**: Possibility to sort clients based on their churn probability, amount of sales net revenue, priority score.
        """)

    elif tab == "Client Deep-dive":
        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image5.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.write("\n")
            st.title("Client Deep-dive Analysis")
        
        st.write("\n")

        st.write("This tab provides an in-depth analysis of individual customer metrics that are vital for sales teams to understand customer's profiles in order to make informed decisions. It allows for a detailed examination of the factors influencing client's behavior and churn risk.")

        st.write("\n")


        branches = ['All'] + sorted(data['branch_id'].unique().tolist())
        selected_branch = st.selectbox("Select Branch", branches, index=0)

        if selected_branch != "All":
            data = data[data['branch_id'] == selected_branch]

        client_id = st.text_input("Enter Client ID:")

        st.write("\n")

        if client_id:
            try:
                client_id = int(client_id)
                client_data = data[data['client_id'] == client_id]

                if not client_data.empty:
                    client_data = client_data.iloc[0]

                    # Calculate and display the three principal metrics in boxes
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                            <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                                <h4 style="color: #4CAF50;">Priority Score</h4>
                                <h3>{client_data['priority_score']:.2f}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div style="border: 2px solid #f44336; padding: 10px; border-radius: 5px;">
                                <h4 style="color: #f44336;">Churn Probability</h4>
                                <h3>{client_data['churn_probability']*100:.2f}%</h3>
                            </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                            <div style="border: 2px solid #2196F3; padding: 10px; border-radius: 5px;">
                                <h4 style="color: #2196F3;">Total Net Sales</h4>
                                <h3>${client_data['tot_sales_net']:,.2f}</h3>
                            </div>
                        """, unsafe_allow_html=True)

                    st.write("\n")
                    st.write("\n")

                    # Display metrics as before

                    # Detailed Analytics
                    st.subheader("Detailed Analytics")
                    detailed_data = {
                        'Frequency Orders': "{:.2f}".format(client_data['avg_freq_orders']),
                        'Days since Last Order': "{:.2f}".format(client_data['lag_day_last']),
                        'Number Returns': "{:.2f}".format(client_data['nb_ret']),
                        'Relationship Quality': client_data['quali_relation'],
                        'Client Type': client_data['client_type']
                    }
                    st.table(pd.DataFrame(detailed_data, index=[0]))

                    st.write("\n")
                    st.write("\n")

                    # Preferred Way of Contact table
                    st.subheader("Ways of Contact")
                    contact_data = {
                        'Pct Sales Online': "{:.2f}".format(client_data['pct_online']),
                        'Pct Sales In Store': "{:.2f}".format(client_data['pct_store']),
                        'Pct Sales Over the Phone': "{:.2f}".format(client_data['pct_phone']),
                        'Pct Sales During Visits': "{:.2f}".format(client_data['pct_visits']),
                        'Pct Sales Other': "{:.2f}".format(client_data['pct_other'])
                    }
                    st.table(pd.DataFrame(contact_data, index=[0]))

                    st.write("\n")
                    st.write("\n")

                    # Plot time series data
                    st.subheader("Time Series Data: Sales Net Over Time")
                    client_time_data = time_data[time_data['client_id'] == client_id]
                    if not client_time_data.empty:
                        fig = px.line(
                            client_time_data, 
                            x='date_order', 
                            y='sales_net', 
                            title=f'Time Series: Sales Net Over Time (Client ID: {client_id})',
                            labels={'date_order': 'Date Order', 'sales_net': 'Total Net Sales'} 
                        )

                        st.plotly_chart(fig)
                    else:
                        st.warning("No time series data available for this client.")
                else:
                    st.error("Client ID not found in the dataset.")
            except ValueError:
                st.error("Client ID must be a number.")
        
        st.write("")

        st.subheader("Functionalities explanations:")

        st.markdown("""
        - **Branch Filter**: Filter that allows the filtering by branch. Each sales manager can focus on their specific branch or on the company as a whole.
        - **Customer Filter**: Input the number of the client we want to do a deep-dive on.
        """)
        
    elif tab == "Financial Tool":

        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image6.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.write("\n")
            st.title("Financial Tool")
        
        st.write("\n")

        st.write("This tab provides enables sales teams to input client data an available budget to project potential sales recovery based on historical sales performance. This feature assists in financial planning and setting realistic targets for customer retention and sales recovery efforts.")

        st.write("\n")

        # Rename and select columns

        display_columns = {
            'client_id': 'Client ID',
            'branch_id': 'Branch ID',
            'priority_score':'Priority Score',
            'churn_probability': 'Probability of Churn',
            'tot_sales_net': 'Total Net Sales',
            'tot_client_cost': 'Total Client Cost',
            'return_client':'Total Client Return',
            'pref_cont_method':'Contact',
            'cost':'Cost'
        }

        # Apply column renaming and selection
        financial_data = financial_data.rename(columns=display_columns)[display_columns.values()]

        financial_data = financial_data[financial_data['Contact'].isin(['Phone', 'Visit'])]

        # Add input for available budget
        available_budget = st.number_input("Available Budget:", min_value=0.0, format='%f')

        # Add a selectbox for the sorting criteria
        sorting_criterion = st.selectbox("Sort by", ["Priority Score", "Total Client Return"], index=0)

        # Sort the data by the selected criterion in descending order
        financial_data_sorted = financial_data.sort_values(by=sorting_criterion, ascending=False)

        # Initialize a list to keep track of selected clients and a running total of the cost
        selected_clients = []
        total_cost = 0

        # Loop through sorted clients and select them until the budget is reached
        for _, row in financial_data_sorted.iterrows():
            if total_cost + row['Cost'] <= available_budget:
                selected_clients.append(row['Client ID'])
                total_cost += row['Cost']
            else:
                break  # Stop if we reach or exceed the budget

        # Calculate total return from selected clients
        total_return = financial_data_sorted[financial_data_sorted['Client ID'].isin(selected_clients)]['Total Client Return'].sum()

        # Display the total number of clients and total return in two columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div style="border: 2px solid #2196F3; border-radius: 5px; padding: 10px;">
                    <h4 style="color: #2196F3;">Total number of clients:</h4>
                    <h3 style="color: #2196F3;">{len(selected_clients)}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="border: 2px solid #2196F3; border-radius: 5px; padding: 10px;">
                    <h4 style="color: #2196F3;">Expected clients back:</h4>
                    <h3 style="color: #2196F3;">{round(len(selected_clients)*0.85)}</h3>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style="border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; margin-bottom: 20px;">
                    <h4 style="color: #4CAF50;">Expected total return (1y):</h4>
                    <h3 style="color: #4CAF50;">${(total_return/2)*0.85:,.2f}</h3>
                </div>
            """, unsafe_allow_html=True)

        # Check if there are any selected clients and display them

        if selected_clients:  # Check if there are any selected clients
            selected_data = financial_data_sorted[financial_data_sorted['Client ID'].isin(selected_clients)]

            # Display the DataFrame without the index
            st.dataframe(selected_data.reset_index(drop=True))
    
        # After displaying the filtered data table
        st.subheader("Functionalities explanations:")

        st.markdown("""
        - **Available Budget**: Input of the available budget we have to reach to clients.
        - **Sort By Filter**: Filter that allows to sort use the budget prioritising clients by their priority rate or by their total return.
        """)



if __name__ == "__main__":
    main()
