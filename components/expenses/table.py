#from database import *

import streamlit as st
import pandas as pd


def expense_table(df: pd.DataFrame):

    table_df = df.copy()

    # Columna para seleccionar registros a eliminar
    table_df["delete"] = False

    edited_df = st.data_editor(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                disabled=True,
                width="small"
            ),

            "date": st.column_config.DateColumn(
                "Fecha"
            ),

            "category": st.column_config.SelectboxColumn(
                "Categoría",
                options=[
                    "Comida",
                    "Transporte",
                    "Agua",
                    "Luz",
                    "Educación",
                    "Entretenimiento",
                    "Tarjeta de Credito",
                    "Otros"
                ]
            ),

            "amount": st.column_config.NumberColumn(
                "Monto",
                format="$ %.2f"
            ),

            "description": st.column_config.TextColumn(
                "Descripción"
            ),

            "delete": st.column_config.CheckboxColumn(
                "🗑️"
            )
        },

        disabled=["id"]
    )

    st.write(table_df.columns)
    return edited_df