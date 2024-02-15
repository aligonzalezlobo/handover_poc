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
    data = load_data("final_data2.csv")
    time_data = load_data("top_client_data.csv")

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
        # Create an empty space, pushing the content to the bottom
        for _ in range(100):  # You can adjust the range number to push the logo down as needed
            st.empty()

        # Center the image by using column width or specifying the width in pixels
        logo_image2 = "images/image2.png"  # Replace with your image path
        st.image(logo_image2, use_column_width=True)


    if tab == "Home Page":

        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image1.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.title("Welcome to Sales Team Tool - CLIENTCO")

        intro_text = """
        This is a churn prevention tool designed to empower sales teams with insights and analytics to proactively identify and address potential customer churn. The application provides sales professionals with the means to forecast which customers are at risk of churning, highlight those whose retention is critical, and strategize on salvaging sales figures by winning back certain customers. The tool features several tabs, each offering unique functionalities:

        - **Client Ranking**: This tab offers a fundamental analysis of customers, ranking them based on various metrics such as churn probability (as determined by our Machine Learning model), total sales return (the total amount spent by the customer on our products), and a priority metric. The priority metric is a formula that uses weighted averages to prioritize some customers over others, based on their potential impact on the business.

        - **Clients Deep-Dive**: This section provides an in-depth analysis of individual customer metrics that are vital for sales teams to understand before making informed decisions. It allows for a detailed examination of the factors influencing customer behavior and churn risk.

        - **Finance Tool**: A practical tool that enables sales teams to input client data and project potential sales recovery based on historical sales performance. This feature assists in financial planning and setting realistic targets for customer retention and sales recovery efforts.

        Sales teams can explore and familiarize themselves with these tabs to make better-informed decisions quickly and efficiently.
        """
        
        st.write(intro_text)

    elif tab == "AI Client Ranking":
        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.35))

        # Add logo image to the first column
        with t1:
            logo_image = "images/image3.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.title("CLIENTCO - Clients Analytics Tool - AI Powered Client Ranking")

        st.write("This tab offers a fundamental analysis of customers, ranking them based on various metrics such as churn probability (as determined by our Machine Learning model), total sales return (the total amount spent by the customer on our products), and a priority metric. The priority metric is a formula that uses weighted averages to prioritize some customers over others, based on their potential impact on the business.")

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
            'client_type' : 'client_type'
        }

        # Apply column renaming and selection
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

        # Display filtered data without index
        st.write("Clients of the selected branch:")
        st.write(filtered_data)



    elif tab == "Client Deep-dive":
        st.header("Client Deep-dive Analysis")
        st.write("Choose your branch:")

        branches = ['All'] + sorted(data['branch_id'].unique().tolist())
        selected_branch = st.selectbox("Select Branch", branches, index=0)

        if selected_branch != "All":
            data = data[data['branch_id'] == selected_branch]

        client_id = st.text_input("Enter Client ID:")

        if client_id:
            try:
                client_id = int(client_id)
                client_data = data[data['client_id'] == client_id]

                if not client_data.empty:
                    client_data = client_data.iloc[0]

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

                    # Preferred Way of Contact table
                    st.subheader("Preferred Way of Contact")
                    contact_data = {
                        'Pct Sales Online': "{:.2f}".format(client_data['pct_online']),
                        'Pct Sales In Store': "{:.2f}".format(client_data['pct_store']),
                        'Pct Sales Over the Phone': "{:.2f}".format(client_data['pct_phone']),
                        'Pct Sales During Visits': "{:.2f}".format(client_data['pct_visits']),
                        'Pct Sales Other': "{:.2f}".format(client_data['pct_other'])
                    }
                    st.table(pd.DataFrame(contact_data, index=[0]))

                    # Plot time series data
                    st.subheader("Time Series Data")
                    client_time_data = time_data[time_data['client_id'] == client_id]
                    if not client_time_data.empty:
                        fig = px.line(client_time_data, x='date_order', y='sales_net', title=f'Time Series: Sales Net Over Time (Client ID: {client_id})')
                        st.plotly_chart(fig)
                    else:
                        st.warning("No time series data available for this client.")
                else:
                    st.error("Client ID not found in the dataset.")
            except ValueError:
                st.error("Client ID must be a number.")
        
    elif tab == "Financial Tool":
        st.header("Financial Tool")



if __name__ == "__main__":
    main()
