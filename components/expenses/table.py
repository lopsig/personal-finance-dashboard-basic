import streamlit as st
import pandas as pd


CATEGORIES = [
    "Comida",
    "Transporte",
    "Agua",
    "Luz",
    "Educación",
    "Entretenimiento",
    "Tarjeta de Credito",
    "Otros"
]


def expense_table(df: pd.DataFrame):

    table_df = df.copy()

    # Columna para marcar registros a eliminar
    table_df["delete"] = False

    edited_df = st.data_editor(
        table_df,
        use_container_width=True,
        hide_index=True,
        disabled=["id"],
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                width="small"
            ),

            "date": st.column_config.DateColumn(
                "Fecha"
            ),

            "category": st.column_config.SelectboxColumn(
                "Categoría",
                options=CATEGORIES
            ),

            "amount": st.column_config.NumberColumn(
                "Monto",
                format="$ %.2f"
            ),

            "description": st.column_config.TextColumn(
                "Descripción"
            ),

            "delete": st.column_config.CheckboxColumn(
                "🗑️ Eliminar",
                default=False
            ),
        }
    )

    return edited_df