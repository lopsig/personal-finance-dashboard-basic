import streamlit as st
import pandas as pd

from database import *

def expense_table(df: pd.DataFrame):

    st.divider()

    st.subheader("📋 Historial de Gastos")

    st.data_editor(
        df,
        use_container_width=True,
        hide_index=True
    )