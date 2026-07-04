from components.expenses.table import expense_table
import streamlit as st
import pandas as pd
import plotly.express as px

from database import *

create_tables()

st.title("💸 Gastos")

# ---------- FORMULARIO ----------

with st.form("expense_form"):

    date = st.date_input("Fecha")

    category = st.selectbox(
        "Categoría",
        [
            "Comida",
            "Transporte",
            "Agua",
            "Luz",
            "Educación",
            "Entretenimiento",
            "Tarjeta de Credito",
            "Otros"
        ]
    )

    amount = st.number_input(
        "Monto",
        min_value=0.0,
        step=0.01
    )

    description = st.text_input(
        "Descripción"
    )

    submitted = st.form_submit_button(
        "Guardar"
    )

    if submitted:

        insert_expense(
            str(date),
            category,
            amount,
            description
        )

        st.success(
            "Gasto guardado correctamente"
        )

        st.rerun()


# ---------- HISTORIAL ----------

expenses = get_expenses()

if expenses:

    df = pd.DataFrame(
        expenses,
        columns=[
            "id",
            "date",
            "category",
            "amount",
            "description"
        ]
    )
    df["date"] = pd.to_datetime(df["date"])

    # ---------- MÉTRICAS ----------

    total_expenses = df["amount"].sum()
    number_of_expenses = df["amount"].count()
    average_expenses = df["amount"].mean()

    # ---------- GRÁFICO ----------

    st.divider()

    st.subheader("📊 Gastos por categoría")

    expenses_by_category = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        expenses_by_category,
        names="category",
        values="amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------- MÉTRICAS ----------

    st.divider()

    st.subheader("📋 Historial de Gastos")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Gastado",
            f"$ {total_expenses:.2f}"
        )

    with col2:
        st.metric(
            "📊 Número de Gastos",
            number_of_expenses
        )

    with col3:
        st.metric(
            "📈 Promedio por Gasto",
            f"$ {average_expenses:.2f}"
        )

    # ---------- TABLA ----------

    edited_df = expense_table(df)


else:

    st.info("Todavía no existen gastos registrados.")