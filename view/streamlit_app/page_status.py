import streamlit as st
import requests
import pandas as pd
from model.config_schema import API_HOST, API_PORT

def app():
    """
    Render the Status page for analysis.

    This page shows the status of the last five analyses by default and allows users to view all tasks or refresh the data.
    """
    st.title('Analysis Status')
    st.write("""
        Displays the processing status of the last five analyses.
        Check "Show all" to display all tasks or click "Refresh" to update the status.
    """)

    # Ensure session state for user is initialized
    if 'user' not in st.session_state:
        st.session_state['user'] = 'default_user'

    # Fetch the status DataFrame
    df = check_status()

    if not df.empty:
        # Add refresh and toggle buttons
        refresh = st.button(label="Refresh", key="button_refresh")
        show_all = st.checkbox("Show all", key="check_all")

        # Display the data
        if refresh:
            st.experimental_rerun()  # Refresh the app to fetch updated data

        if show_all:
            st.dataframe(data=df, hide_index=True)
        else:
            st.dataframe(data=df.head(5), hide_index=True)
    else:
        st.warning(f"No tasks found for the user: {st.session_state.get('user', 'unknown')}")


def check_status():
    """
    Fetch the status of analyses for the current user.

    Returns:
        pd.DataFrame: A DataFrame containing analysis IDs, statuses, timestamps, and results.
    """
    user = st.session_state.get('user', 'default_user')
    url = f'http://{API_HOST}:{API_PORT}/status/{user}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTP errors if they occur
        total_response = response.json()

        if total_response:
            df = pd.DataFrame(list(total_response.items()), columns=["Identifier", "Status"])
            df["Timestamp"] = pd.to_datetime(df["Status"].str.extract(r'at (.*)')[0], errors='coerce')
            df["Result"] = df["Status"].apply(
                lambda x: "✅" if "Concluded" in x else ("❌" if "Error" in x else "⏳")
            )
            df = df.sort_values(by="Timestamp", ascending=False)
            return df
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data is found
    except requests.RequestException as e:
        st.error(f"Failed to fetch status data: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of an error