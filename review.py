import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def parsing():
    from cianparser import CianParser
    '''Парсинг данных для анализа'''
    locations = tuple('Москва', 'Балашиха', 'Лобня', 'Солнечногорск')
    for loc in locations:
        parser = CianParser(loc)
        parser.get_flats(deal_type="sale", rooms=1, with_saving_csv=True, with_extra_data=True, additional_settings={"start_page":1, "end_page":54})
# Парсинг данных


# Чистка данных

df = pd.read_csv('cian_data.csv', delimiter=';', encoding='utf-8').drop_duplicates()
pd.set_option('display.max_columns', None)

print(df.head())

print('\n', '-' * 10, '\nДанные до обработки\n')
df.info()   # вывожу информацию о датасете до обработки
print('Количество строк до обработки:', df.shape[0])

df = df[df['year_of_construction'].fillna(-1).astype(int) <= 2024]  # удаляю строки с годом больше 2024

df['living_meters'] = df['living_meters'].replace('м²', '', regex=True).replace(r'\xa0', '', regex=True).str.replace(',', '.').astype(float)    # убираю лишние знаки и меняю тип данных
df['kitchen_meters'] = df['kitchen_meters'].replace('м²', '', regex=True).replace(r'\xa0', '', regex=True).str.replace(',', '.').astype(float)

df['underground'] = df['underground'].fillna(-1)
df['floor'] = df['floor'].fillna(-1).astype(int)    # заполняю пропущенными значениями -1 и меняю тип данных на целые числа
df['floors_count'] = df['floors_count'].fillna(-1).astype(int)
df['rooms_count'] = df['rooms_count'].fillna(-1).astype(int)
df['year_of_construction'] = df['year_of_construction'].fillna(-1).astype(int)

df.drop(['phone', 'house_material_type', 'object_type', 'finish_type', 'heating_type', 'deal_type', 'accommodation_type'], axis=1, inplace=True)
df = df[df['price'].notna()]    # удалю строки с пропущенными значениями
df['price'] = round(df['price']).astype(int)
df['price_per_sqm'] = round(df['price'] / df['total_meters']).astype(int)   # создаю и вычисляю цену за кв. метр

print('\n', '-' * 10, '\nДанные после обработки\n')
df.info()   # вывожу информацию о датасете после обработки
print('Количество строк после обработки:', df.shape[0])

# Сохраняю обработанный датасет
df.to_csv('cian_data_mod.csv', sep=';', encoding='utf-8', index=False)

# Конец чистки данных



# Графики

# Построение матрицы корреляции
correlation_matrix = df[['price_per_sqm', 'total_meters', 'floor', 'floors_count', 'rooms_count', 'living_meters', 'kitchen_meters', 'year_of_construction']].corr()

# Визуализация корреляционной матрицы
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", annot_kws={"size": 10})
plt.xticks(rotation=70, fontsize=10)
plt.title("Корреляция между переменными")

# Влияние этажа на цену за квадратный метр
plt.figure(figsize=(20, 10))
sns.barplot(x="floor", y="price_per_sqm", data=df)
plt.title("Зависимость цены за кв.м от этажа")
plt.xlabel("Этаж")
plt.ylabel("Цена за кв.м")

# Влияние этажности здания на цену за квадратный метр
plt.figure(figsize=(20, 10))
sns.barplot(x="floors_count", y="price_per_sqm", data=df)
plt.title("Зависимость цены за кв.м от общего количества этажей в здании")
plt.xlabel("Этажность здания")
plt.ylabel("Цена за кв.м")

# Влияние количества комнат на цену за квадратный метр
plt.figure(figsize=(20, 10))
sns.barplot(x="rooms_count", y="price_per_sqm", data=df)
plt.title("Зависимость цены за кв.м от количества комнат")
plt.xlabel("Количество комнат")
plt.ylabel("Цена за кв.м")
plt.show()
