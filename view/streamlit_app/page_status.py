import streamlit as st
import requests
import pandas as pd
from model.config_schema import API_HOST, API_PORT


def app():
    """Render the Status page for analysis."""
    st.title('Analysis Status')
    st.write("""
             Displays the processing status of the last five analyses.
             Check "Show all" to display all tasks or click "Refresh" to update the status.
             """)
    df = check_status()
    if not df.empty:
        st.button(label="Refresh", key="button_refresh")
        st.checkbox("Show all", key="check_all")

        if st.session_state["button_refresh"]:   
            if st.session_state["check_all"]:
                st.dataframe(data=df, hide_index=True)
            else:
                st.dataframe(data=df.head(5), hide_index=True)
    else:
        st.warning(f"No tasks found for the user: {st.session_state["user"]}")


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