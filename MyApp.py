# C:\Users\User>cd C:\Users\User\Documents\IDE_Git
# C:\Users\User\Documents\IDE_Git>streamlit run MyApp.py
 
#   You can now view your Streamlit app in your browser.

#   Local URL: http://localhost:8501
#   Network URL: http://192.168.34.146:8501



  
# РАЗВОРАЧИВАЕМ СТРИМЛИТ-
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Aналитический центр",
    layout="wide"
)


st.header('Aналитический центр - Сводный департамент')
st.subheader('Комплексная модель автоматизированного поиска рисков нарушений')
st.write('(переход от выборочных проверок к сплошному автоматизированному контролю федерального бюджета)') 
st.write('Источником информации для анализа являются - открытые данные')

#st.write('Доступ ограничен')
password = st.text_input('Для доступа введите пароль:', type='password')
if password != 'Inna':
    st.write('НЕТ ДОСТУПА')
else:
    
    # df = pd.read_excel('https://github.com/MyAudit/MA/raw/master/!%202023%2010%2001%20faip_sravnenie_k%202023%2010%2025_1.xlsx')
    df = pd.read_excel('https://github.com/MyAudit/km/raw/master/2023_10_01_faip_sravnenie_k_2023_10_25_1.xlsx')
    df['ГРБС(общее)'] = [('0' + str(i)) if len(str(i)) == 2 else str(i) for i in df['ГРБС(общее)']]
    
    st.subheader('Анализ ФАИП на 01.10.2023')
    
    # ЗАКОМЕНТИРОВАН 1Й ВАРИАНТ - РАБОТАЕТ
    
    # st.write(df)
    
    

    # def convert_df_dep_svod(df):
    #     #return df.to_csv().encode('utf-8') # - оригинал кода - дает краказябры
    #     #return df.to_excel()#.encode('utf-8') - тест - не срабатывает
    #     #return df.to_csv().encode('Windows-1251') # - данные на русском, но в строчку через запятую таблицу не показывает
    #     #return df.to_csv(sep=';',encoding='utf-8') # - таблица есть но с кракозябрами
    #     return df.to_csv(sep=';').encode('Windows-1251')
        
            
    # csv = convert_df_dep_svod(df)
    # st.download_button(
    #     label="Скачать как csv",
    #     data=csv,
    #     file_name=('Анализ ФАИП на 01.10.2023.csv'),
    #     mime='text/csv',
    #     )
    
    
    
    # НИЖЕ 2Й ВАРИАНТ - С ФИЛЬТРАМИ
    
    # https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
    
    # Раздел кода 1. Размещение виджетов Streamlit
    # filter_dataframe Функция вводит и выводит одно и то же - фрейм данных pandas. 
    # В рамках функции мы сначала спрашиваем пользователя, не хочет ли он отфильтровать фрейм данных с помощью флажка modify.
    # Мы также добавили комментарии и подсказки по вводу в верхней части функции, чтобы сделать код более удобоваримым:
    
    def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a UI on top of a dataframe to let viewers filter columns

        Args:
            df (pd.DataFrame): Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
        """
        modify = st.checkbox("Добавить фильтры")

        if not modify:
            return df 
        
        
        # Раздел кода 2. Подготовка входного фрейма данных к фильтрации  
        # Для подготовки фрейма данных для вашего приложения необходимо выполнить несколько шагов. 
        # Для первых трех вам необходимо:
        # 1) Создайте копию фрейма данных pandas, чтобы пользовательский ввод не изменил базовые данные.
        # 2) Попытайтесь преобразовать столбцы строк в datetimes с помощью pd.to_datetime().
        # 3) Локализуйте свои столбцы datetime с помощью .tz_localize(). Средство выбора даты Streamlit (которое вы будете использовать позже!) возвращает даты без часового пояса, поэтому вам нужно выполнить этот шаг, чтобы сравнить их:
        
        df = df.copy()

        # Try to convert datetimes into a standard format (datetime, no timezone)
        for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass

            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)
                
        # Теперь, когда ваши данные представлены в лучшем формате, вам необходимо:
        # 1) Настройте контейнер с st.container для ваших виджетов фильтрации.
        # 2) Используйтеst.multiselect, чтобы позволить пользователю выбирать столбцы:   
        
        modification_container = st.container()
        
        with modification_container:
            to_filter_columns = st.multiselect("Отфильтруйте таблицу по", df.columns)
        
            # Перебирайте каждый столбец и разбирайтесь с каждым в зависимости от его типа. 
            # Затем вы напишете условия для каждого из них!
            # Добавьте отступ и стрелку для улучшения эстетики, когда пользователи выбирают много столбцов. 
            
            for column in to_filter_columns:
                left, right = st.columns((1, 20))
                left.write("↳")
                
                # Все ваши данные находятся в правильном формате. 
                # Вы гарантировали, что ваш исходный набор данных останется нетронутым, 
                # и подготовили цикл для просмотра всех ваших столбцов. Теперь начинается самое интересное!

                # Раздел кода 3. Написание условий для разных типов столбцов
                
                # В этой функции вам нужно будет проверить наличие трех типов данных pandas 
                # — категориальных, числовых и datetime 
                # — затем обработать остальные, как если бы они были строками. 
                # Это предположение, которое нам подходит. 
                # Ваша ситуация может отличаться, поэтому не стесняйтесь добавлять свои собственные условия в этот список.
                # 
                # Для каждого из них создайте виджет Streamlit, соответствующий вашему типу, 
                # затем отфильтруйте ваши данные на основе этого виджета. 
                # В конце этого цикла вам нужно будет вернуть весь отфильтрованный фрейм данных.

                # Давайте рассмотрим их один за другим.

                # Категориальные типы
                # Проверьте наличие категориальных типов с помощью is_categorical_dtype функции. 
                # Часто пользователи не приводят свои данные к этому типу, 
                # поэтому предположим, что все, имеющее менее 10 уникальных значений, действует как категориальный dtype. 
                # В качестве бонуса, он будет отлично работать с логическими столбцами (которые имеют только значения True или False!).

                # Теперь создайте виджет с несколькими вариантами выбора с возможными значениями и используйте его для фильтрации вашего фрейма данных:
                
                # Treat columns with < 10 unique values as categorical
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )
                    df = df[df[column].isin(user_cat_input)]
                
                # Числовые типы

                # Числовые типы довольно просты. 
                # Вы можете получить минимум и максимум из самого набора данных, 
                # затем предположить, что шаговая функция равна 1% от диапазона, 
                # и соответствующим образом отфильтровать данные:
                
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"Values for {column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                
                # Типы Datetime

                # Тип datetime dtype почти такой же, как у двух других. 
                # Вы получаете пользовательский ввод с помощью st.date_input функции. 
                # Как только пользователь введет две даты, вы сможете отфильтровать свой набор данных: 
                
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Values for {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                                            
                # Другие типы

                # Нам нравится преобразовывать другие dtypes в строку, а затем позволять пользователю искать в них подстроки. 
                # Это может не сработать для вашего варианта использования, но для нас это работает достаточно хорошо:
                
                else:
                    user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]
        return df        
    # Сведите все это воедино
    # Хотите посмотреть, как выглядит код в действии? 
    # Продолжайте и протестируйте его на наборе данных palmerpenguins (данные смотрите в этом репозитории GitHub) 
    # или на ваших собственных данных!

    # Мы создали пример приложения с использованием кода (ознакомьтесь с ним ниже):        
    
    st.dataframe(filter_dataframe(df))
    
    def convert_df_dep_svod(df):
        #return df.to_csv().encode('utf-8') # - оригинал кода - дает краказябры
        #return df.to_excel()#.encode('utf-8') - тест - не срабатывает
        #return df.to_csv().encode('Windows-1251') # - данные на русском, но в строчку через запятую таблицу не показывает
        #return df.to_csv(sep=';',encoding='utf-8') # - таблица есть но с кракозябрами
        return df.to_csv(sep=';').encode('Windows-1251')
        
            
    csv = convert_df_dep_svod(df)
    st.download_button(
        label="Скачать как csv",
        data=csv,
        file_name=('Анализ ФАИП на 01.10.2023.csv'),
        mime='text/csv',
        )        
            
    
    
    #st.write(df)
    
    

    # def convert_df_dep_svod1(df_itog):
    #     #return df.to_csv().encode('utf-8') # - оригинал кода - дает краказябры
    #     #return df.to_excel()#.encode('utf-8') - тест - не срабатывает
    #     #return df.to_csv().encode('Windows-1251') # - данные на русском, но в строчку через запятую таблицу не показывает
    #     #return df.to_csv(sep=';',encoding='utf-8') # - таблица есть но с кракозябрами
    #     return df_itog.to_csv(sep=';').encode('Windows-1251')
        
            
    # csv = convert_df_dep_svod1(df_itog)
    # st.download_button(
    #     label="Скачать как csv (фильтр)",
    #     data=csv,
    #     file_name=('Анализ ФАИП на 01.10.2023 (фильтр).csv'),
    #     mime='text/csv',
    #     )



    
    
    
    
# print(df.dtypes)


