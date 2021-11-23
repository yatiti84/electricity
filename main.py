import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_weather = pd.read_csv('weather_loc_clean.csv', header=0)

columns = df_weather.columns
print(columns)
# len(columns)
df_elec = pd.read_csv('electirc.csv', header=0)
df_elec = df_elec.iloc[:len(columns), :]
index = {}
for i in range(len(columns)):
    index[i] = columns[i]
df_elec.rename(index=index)

temperature = []
#  當日全台主要測站均溫
for col in columns:
    mean = df_weather[col].mean()
    temperature.append(mean)
# 將溫度和電力資料合併
se = pd.Series(temperature, index=columns, name='全台日均溫')
df_elec['全台日均溫'] = se.values
# 拿取資料
X = np.reshape(list(df_elec['全台日均溫']), (len(df_elec['全台日均溫']), 1))
y_industry = np.reshape(list(df_elec['工業用電(百萬度)']), (len(df_elec['工業用電(百萬度)']), 1))
y_life = np.reshape(list(df_elec['民生用電(百萬度)']), (len(df_elec['民生用電(百萬度)']), 1))

# 訓練資料 測試資料
from sklearn.model_selection import train_test_split

X_train, X_test, y_train_industry, y_test_industry = train_test_split(X, y_industry,
                                                                      test_size=0.2, random_state=0)
X_train, X_test, y_train_life, y_test_life = train_test_split(X, y_life, test_size=0.2, random_state=0)

# 線性回歸模型
from sklearn.linear_model import LinearRegression


def linearReg(X_train, y_train, X_test):
    lm = LinearRegression()

    return lm.fit(X_train, y_train)


# 績效評估
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def predictPerformance(X_test, y_test, lm):
    y_predict = lm.predict(X_test)
    r2Score = r2_score(y_test, y_predict)
    mse = mean_squared_error(y_test, y_predict)
    rmse = np.sqrt(mean_squared_error(y_test, y_predict))
    mae = mean_absolute_error(y_test, y_predict)
    coef = lm.coef_[0]
    print('r2_score：', r2Score)
    print('MSE：', mse)
    print('RMSE：', rmse)
    print('MAE：', mae)
    print('coef：', coef)
    print('===================================')
    return y_predict


y_predict_industry = predictPerformance(X_test, y_test_industry, linearReg(X_train, y_train_industry, X_test))
y_predict_life = predictPerformance(X_test, y_test_life, linearReg(X_train, y_train_life, X_test))
# 視覺化
plt.scatter(X, y_industry, color='black')
plt.plot(X_test, y_predict_industry, color='red', linewidth=3)
plt.scatter(X, y_life, color='blue')
plt.plot(X_test, y_predict_life, color='red', linewidth=3)
