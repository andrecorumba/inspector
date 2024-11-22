import streamlit as st
import requests
from page_status import check_status

API_HOST = "fastapi"
API_PORT = "8000"

def fetch_api_data(endpoint: str):
    """
    Fetch data from the API.

    Args:
        endpoint (str): The API endpoint URL.

    Returns:
        dict: The JSON response from the API or an error message.
    """
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch data from {endpoint}: {e}")
        return {}

def app():
    """
    Render the Response page of the AI model.

    This page displays completed analyses and allows users to review responses, 
    view related metadata, and submit evaluations.
    """
    st.title("AI Model Responses")
    st.write("⚠️ Only completed analyses are displayed here. Track the status of your analysis in the status menu.")

    # Fetch status dataframe
    df = check_status()
    if not df.empty:
        df = df[df['Result'] == '✅']
        total_response = df["Identifier"].to_list()
        total_response = [identifier.replace('status', 'response') for identifier in total_response]

        if total_response:
            rag_redis_key = st.selectbox(
                label='Select a key or enter the number to view the response', 
                options=total_response
            )
            
            # Display AI responses and metadata
            st.markdown("## Model Response")
            response_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/{rag_redis_key}')
            st.write(response_data)

            st.markdown("## Tokens")
            tokens_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/use/{rag_redis_key}')
            st.json(tokens_data, expanded=False)

            st.markdown("## Context")
            context_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/context/{rag_redis_key}')
            st.json(context_data, expanded=False)

            st.markdown("## Files Used")
            files_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/files/{rag_redis_key}')
            st.json(files_data, expanded=False)

            st.markdown("## Detailed Prompt")
            prompt_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/messages/{rag_redis_key}')
            st.json(prompt_data, expanded=False)

            st.markdown("## Detailed Response")
            details_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/detail/{rag_redis_key}')
            st.json(details_data, expanded=False)

            st.markdown("## Response Evaluation")
            evaluation_data = fetch_api_data(f'http://{API_HOST}:{API_PORT}/response/evaluation/{rag_redis_key}')
            st.json(evaluation_data, expanded=False)

            if evaluation_data.get("evaluation") == 0:
                evaluation_score = st.slider(
                    label="Evaluate the Model Response:", 
                    min_value=0, 
                    max_value=5, 
                    step=1, 
                    help="0 - Not Evaluated, 1 - Nonsensical, 2 - Very Incomplete, 3 - Incomplete, 4 - Acceptable, 5 - Complete",
                    key="evaluation_slider"
                )
                observation = st.text_area(
                    label="What would be the expected response? (Required for ratings 1 to 3)", 
                    key="evaluation_observation",
                )
                if st.button("Submit Evaluation"):
                    if evaluation_score in [1, 2, 3] and not observation.strip():
                        st.error("Observation is required for evaluations rated 1 to 3.")
                    else:
                        url_post = f'http://{API_HOST}:{API_PORT}/response/evaluation/{rag_redis_key}'
                        params = {
                            "evaluation": int(evaluation_score),
                            "observation": observation
                        }
                        try:
                            evaluation_post = requests.post(url_post, json=params)
                            evaluation_post.raise_for_status()
                            st.success("Evaluation Submitted Successfully!")
                        except requests.RequestException as e:
                            st.error(f"Failed to submit evaluation: {e}")
        else:
            st.warning(f"No keys found for the user: {st.session_state.get('user', 'unknown')}")

    else:
        st.info("No completed analyses available.")