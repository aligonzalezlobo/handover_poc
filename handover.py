import streamlit as st
import pandas as pd

def load_data(file_path):
    """
    Load the dataset from the given file path.
    """
    return pd.read_csv(file_path)

def main():
    # Load the dataset
    data = load_data("final_data.csv")

    # Set page configuration
    st.set_page_config(
        page_title="CLIENTCO - Clients Analytics, Sales Team Tool",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Increase the maximum number of elements allowed to be styled
    pd.set_option("styler.render.max_elements", 5989816)

    # Create sidebar navigation for tabs
    tab = st.sidebar.radio("Navigation", ["Home Page", "Client Ranking", "Client Deep-dive"])

    if tab == "Home Page":
        # Add your content for the home page
        st.title("Welcome to Sales Team Tool CLIENTCO")
        st.write("blabla ")

    elif tab == "Client Ranking":
        # Create columns for layout
        t1, t2 = st.columns((0.07, 0.5))

        # Add logo image to the first column
        with t1:
            logo_image = "images/index.png"
            st.image(logo_image, width=120)

        # Add title to the second column
        with t2:
            st.title("CLIENTCO - Clients Analytics Tool")

        # Add sentence asking to choose branch
        st.write("Choose your branch:")

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
            'importance_score':'Importance Score',
            'proba_churn': 'Probability of Churn',
            'tot_sales_net': 'Total Net Sales',
            'avg_freq_orders': 'Frequency Orders',
            'lag_day_last': 'Days since Last Order',
            'nb_ret': 'Number Returns',
            'quali_relation' : 'Relationship Quality',
            'pct_online': 'Pct sales online',
            'pct_store': 'Pct sales in store',
            'pct_phone': 'Pct sales over the phone',
            'pct_visits': 'Pct sales during visits',
            'pct_other': 'Pct sales other',
            'client_type' : 'client_type'
        }

        # Apply column renaming and selection
        filtered_data = filtered_data.rename(columns=display_columns)[display_columns.values()]


        # Round 'Frequency Orders' to two decimal places
        filtered_data['Frequency Orders'] = filtered_data['Frequency Orders'].round(2)

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
        sort_by = st.selectbox("Sort by", ["", "Importance Score", "Probability of Churn", "Total Net Sales"])
        if sort_by:
            if sort_by == "Importance Score":
                filtered_data = filtered_data.sort_values(by="Importance Score", ascending=False)
            elif sort_by == "Probability of Churn":
                filtered_data = filtered_data.sort_values(by="Probability of Churn", ascending=False)
            elif sort_by == "Total Net Sales":
                filtered_data = filtered_data.sort_values(by="Total Net Sales", ascending=False)

        # Display filtered data without index
        st.write("Clients of the selected branch:")
        st.write(filtered_data)

    # ... (the rest of your code before the elif statement)


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

                    # Client Type mapping
                    client_type_mapping = {
                        'recurrent_client': 'Recurrent Client',
                        'occasional_client': 'Occasional Client',
                        'new_client': 'New Client'
                    }
                    client_data['client_type'] = client_type_mapping.get(client_data['client_type'], client_data['client_type'])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Importance Score", value="{:.2f}".format(client_data['importance_score']))
                    with col2:
                        st.metric("Probability of Churn", value="{:.2%}".format(client_data['proba_churn']))
                    with col3:
                        st.metric("Total Net Sales", value="${:,.2f}".format(client_data['tot_sales_net']))

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

                else:
                    st.error("Client ID not found in the dataset.")
            except ValueError:
                st.error("Client ID must be a number.")



if __name__ == "__main__":
    main()
