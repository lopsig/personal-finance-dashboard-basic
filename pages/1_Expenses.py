import streamlit as st
import pandas as pd
import plotly.express as px

from database import *

create_tables()

st.title("💸 Gastos")

# ---------- FORM----------

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

# ---------- HISTORIAL ----------

expenses = get_expenses()

if expenses:

    df = pd.DataFrame(
        expenses,
        columns=[
            "ID",
            "Fecha",
            "Categoría",
            "Monto",
            "Descripción"
        ]
    )

    total_expenses = df["Monto"].sum()
    number_of_expenses = df["Monto"].count()
    average_expenses = df["Monto"].mean()

    # ---------- GRAFICO ----------

    st.divider()

    st.subheader(
        "📊 Gastos por categoría"
    )

    expenses_by_category = (
        df.groupby("Categoría")["Monto"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        expenses_by_category,
        names="Categoría",
        values="Monto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------- METRICAS ----------

    st.divider()
    st.subheader(
        "📋 Historial de Gastos"
    )


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


    # df = df.drop(
    #     columns=["ID"]
    # )



    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    st.subheader("🗑️ Eliminar gasto")

    expense_options = {
        f"{row['Fecha']} | {row['Categoría']} | ${row['Monto']:.2f}":
            row["ID"]
        for _, row in df.iterrows()
    }

    selected_expense = st.selectbox(
        "Seleccione un gasto",
        options=list(expense_options.keys())
    )

    if st.button("Eliminar gasto"):

        expense_id = expense_options[selected_expense]

        delete_expense(expense_id)

        st.success(
            "Gasto eliminado correctamente"
        )

        st.rerun()