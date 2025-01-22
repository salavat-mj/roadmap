import streamlit as st
import pandas as pd

# Пример данных о продуктах
PRODUCTS = {
    "Кабачок": {"Белки": 0.6, "Жиры": 0.3, "Углеводы": 4.6, "Калории": 24},
    "Томат (помидор)": {"Белки": 1.1, "Жиры": 0.2, "Углеводы": 3.7, "Калории": 20},
    "Капуста брокколи": {"Белки": 3, "Жиры": 0.4, "Углеводы": 5.2, "Калории": 28},
    "Шампиньоны свежие": {"Белки": 4.3, "Жиры": 1, "Углеводы": 0.1, "Калории": 27},
    "Сыр Адыгейский": {"Белки": 18.5, "Жиры": 14, "Углеводы": 0, "Калории": 240},
    "Перец сладкий красный": {"Белки": 1.3, "Жиры": 0, "Углеводы": 5.3, "Калории": 27},
    "Лук репчатый": {"Белки": 1.4, "Жиры": 0, "Углеводы": 9.6, "Калории": 42},
}

# Заголовок
st.title("Калькулятор продуктов")

# Инициализация состояния для хранения данных таблицы
if "data" not in st.session_state:
    st.session_state.data = []

# Функция добавления строки
def add_row():
    st.session_state.data.append({"Продукт": "", "Вес": 0, "Белки": 0, "Жиры": 0, "Углеводы": 0, "Калории": 0})

# Кнопка добавления продукта
if st.button("Добавить продукт"):
    add_row()

# Разделитель
divider = "<hr style='border: 0.2px solid #d7dee5;' />"
st.markdown(divider, unsafe_allow_html=True)

col_size = [1.3, 6, 2, 2, 2, 2, 2]
# Таблица данных
updated_data = []  # Для хранения данных после обработки цикла
for i, row in enumerate(st.session_state.data):
    col1, col2, col3, col4, col5, col6, col7 = st.columns(col_size)

    # Кнопка удаления строки (выровненная по нижнему краю)
    with col1:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("❌", key=f"remove_{i}"):
            continue  # Пропускаем добавление этой строки в updated_data

    # Выпадающий список с продуктами
    with col2:
        product = st.selectbox("Продукт", [""] + list(PRODUCTS.keys()), key=f"product_{i}")
        row["Продукт"] = product

    # Поле ввода веса
    with col3:
        weight = st.number_input("Вес, гр", min_value=0, value=row["Вес"], step=1, key=f"weight_{i}")
        row["Вес"] = weight

    # Поля для Белков, Жиров, Углеводов и Калорий
    if product:
        nutrients = PRODUCTS[product]
        row["Белки"] = nutrients["Белки"] * weight / 100
        row["Жиры"] = nutrients["Жиры"] * weight / 100
        row["Углеводы"] = nutrients["Углеводы"] * weight / 100
        row["Калории"] = nutrients["Калории"] * weight / 100

    with col4:
        st.text("Белки")
        st.write(round(row["Белки"], 2))
    with col5:
        st.text("Жиры")
        st.write(round(row["Жиры"], 2))
    with col6:
        st.text("Углеводы")
        st.write(round(row["Углеводы"], 2))
    with col7:
        st.text("Калории")
        st.write(round(row["Калории"], 2))

    # Если строка не была удалена, добавляем её в обновленные данные
    updated_data.append(row)

# Обновляем состояние с данными
st.session_state.data = updated_data

# Преобразование данных в DataFrame для расчетов
df = pd.DataFrame(st.session_state.data)

# Итоговые значения
if not df.empty:
    # Разделитель перед "Итого"
    st.markdown(divider, unsafe_allow_html=True)

    total = df[["Вес", "Белки", "Жиры", "Углеводы", "Калории"]].sum()
    col1, col2, col3, col4, col5, col6, col7 = st.columns(col_size)

    with col1:
        st.text("")
    with col2:
        st.text("Итого")
    with col3:
        st.write(total["Вес"])
    with col4:
        st.write(round(total["Белки"], 2))
    with col5:
        st.write(round(total["Жиры"], 2))
    with col6:
        st.write(round(total["Углеводы"], 2))
    with col7:
        st.write(round(total["Калории"], 2))

    # Значения на 100 грамм
    per_100g = (total / total["Вес"] * 100).fillna(0)
    col1, col2, col3, col4, col5, col6, col7 = st.columns(col_size)

    with col1:
        st.text("")
    with col2:
        st.text("На 100 г")
    with col3:
        st.write(round(per_100g["Вес"], 2))
    with col4:
        st.write(round(per_100g["Белки"], 2))
    with col5:
        st.write(round(per_100g["Жиры"], 2))
    with col6:
        st.write(round(per_100g["Углеводы"], 2))
    with col7:
        st.write(round(per_100g["Калории"], 2))
