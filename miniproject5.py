import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

df1 = pd.read_csv(r"C:\Users\Пользователь\Desktop\Аналитик данных 1\[SW.BAND] 2 МОДУЛЬ PYTHON\[SW.BAND] Данные для Минипроектов\5_transaction_data.csv", encoding='windows-1251')
df2 = pd.read_csv(r"C:\Users\Пользователь\Desktop\Аналитик данных 1\[SW.BAND] 2 МОДУЛЬ PYTHON\[SW.BAND] Данные для Минипроектов\5_transaction_data_updated.csv", encoding='windows-1251')

# Переводим в datetime
df1['date1'] = pd.to_datetime(df1["date"], dayfirst=True, errors="coerce")
df2['date2'] = pd.to_datetime(df2["date"], dayfirst=True, errors="coerce")

# Переводим в числовой формат (timestamp в секундах)
df1["date_num1"] = df1["date1"].astype("int64") // 10**9
df2["date_num2"] = df2["date2"].astype("int64") // 10**9

#print(df1['transaction'].unique()) 'cancelled' 'successfull' 'error'

print("Размер таблицы:", df1.shape)
print("\nТипы переменных:\n", df1.dtypes)
print("\nЧисло пропущенных значений:\n", df1.isna().sum())
print("\nОписательная статистика:\n", df1.describe(include="all"))

cancelled_count = (df1['transaction'] == 'cancelled').sum()
successfull_count = (df1['transaction'] == 'successfull').sum()
error_count = (df1['transaction'] == 'error').sum()
print('В столбце transaction параметр cancelled встречается:', cancelled_count, 'раз.')
print('В столбце transaction параметр successfull встречается:', successfull_count, 'раз.')
print('В столбце transaction параметр error встречается:', error_count, 'раз.')

# Визуализация barplot
ax = sns.countplot(x="transaction", data=df1, color="skyblue")  # вместо palette

# подписи на столбиках
for p in ax.patches:
    ax.annotate(p.get_height(),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom')
plt.title("Распределение транзакций")
plt.xlabel("Тип транзакции")
plt.ylabel("Количество")
plt.show()

# Фильтруем только успешные транзакции
successful = df1[df1['transaction'] == 'successfull']

# Считаем число успешных транзакций на пользователя
user_success_counts = successful['name'].value_counts()
print(user_success_counts.head())

# строим гистограмму распределения числа успешных транзакций
plt.figure(figsize=(10,6))
plt.hist(user_success_counts, bins=20, color='skyblue', edgecolor='black')
plt.title("Распределение числа успешных транзакций на пользователя")
plt.xlabel("Количество успешных транзакций")
plt.ylabel("Число пользователей")
plt.show()


user_vs_minute_pivot = df2.pivot_table(index='minute', columns='name', values='transaction', aggfunc='count', fill_value=0, )
user_vs_minute_pivot = user_vs_minute_pivot.reset_index() # так сказать растягиваем столбцы, чтобы все выглядело красиво и name не висело сверху
user_vs_minute_pivot = user_vs_minute_pivot.fillna(0) # заполняем нулями пропущенные значения
print(user_vs_minute_pivot)


plt.figure(figsize=(10,6))
sns.histplot(df2["minute"], bins=60, color="orange", edgecolor="black")
plt.title("Распределение minute из исходных данных")
plt.xlabel("minute")
plt.ylabel("Количество транзакций")
plt.show()




df2["true_minute"] = df2["date2"].dt.hour * 60 + df2["date2"].dt.minute # Это даёт количество минут от начала суток (0–1439).


plt.figure(figsize=(10,6))
sns.histplot(df2["true_minute"], bins=1440, color="green", edgecolor="black")
plt.title("Распределение true_minute (исправленные данные)")
plt.xlabel("true_minute")
plt.ylabel("Количество транзакций")
plt.show()

print(df2[["date2", "minute", "true_minute"]].head(10))






































