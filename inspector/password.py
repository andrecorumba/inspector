import streamlit as st

usuario = ''

def check_password():
    """
    Retorna `True` se o usuário inseriu o password correto.

    Código original disponível em:
    https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
    """

    def password_entered():
        """Checa se o password inserido é correto."""

        global usuario
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"] == st.secrets["passwords"][st.session_state["username"]]
            ):
            st.session_state["password_correct"] = True
            st.session_state["username"]
            # del st.session_state["password"]  # don't store username + password
            # del st.session_state["username"]
            del st.session_state["password"]  # don't store password
            usuario = st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primeira execução, mostra inputs para usuário.
        st.text_input("Username", 
                      on_change=password_entered, 
                      key="username")
        st.text_input("Password", 
                      type="password", 
                      on_change=password_entered, 
                      key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        # Password nnão está correto, mostra input + error.
        st.text_input("Username", 
                      on_change=password_entered, 
                      key="username")
        st.text_input("Password", 
                      type="password", 
                      on_change=password_entered, key="password"
        )
        st.error("😕 Usuário não conhecido ou password incorreto.")
        return False
    
    else:
        # Password correto.
        return True