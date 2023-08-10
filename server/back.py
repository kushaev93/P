import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
from get_5min_data import get_5min_data_from_yfinance_and_save


app = Flask(__name__)
CORS(app)  # Разрешить запросы CORS на все маршруты
@app.route('/spx_data')
def get_spx_data():
    current_date = datetime.now()
    
    # Загрузка данных
    spx_data = yf.download('^GSPC', start="2023-01-01", end=current_date.strftime("%Y-%m-%d"))
    
    # Создание списков для хранения данных свечей и индикатора
    candle_data = []
    indicator_data = []

    for index, row in spx_data.iterrows():
        # Данные свечи
        candle_info = {
            'x': int(index.timestamp() * 1000),
            'y': [row['Open'], row['High'], row['Low'], row['Close']]
        }
        candle_data.append(candle_info)
        
        # Данные индикатора
        indicator_value = 1 if abs(row['Open'] - row['Close']) > 10 else 0
        indicator_info = {
            'timestamp': int(index.timestamp() * 1000),
            'value': indicator_value
        }
        indicator_data.append(indicator_info)

    # Отправка данных свечи и индикатора как JSON объекта
    return jsonify(candles=candle_data, indicator=indicator_data)


# @app.route('/spx_data')
# def get_spx_data():
#     # Получение текущей даты
#     current_date = datetime.now()
    
#     # Загрузка данных с помощью yfinance для индекса S&P 500 (spx)
#     spx_data = yf.download('^GSPC', start="2023-01-01", end=current_date.strftime("%Y-%m-%d"))
    
#     # Создание списка для хранения данных свечей в формате, соответствующем вашему ожиданию
#     candle_data = []
#     for index, row in spx_data.iterrows():
#         candle_info = {
#             'x': int(index.timestamp() * 1000),  # Преобразование даты в миллисекунды
#             'y': [row['Open'], row['High'], row['Low'], row['Close']]
#         }
#         candle_data.append(candle_info)

#     # Преобразование списка данных свечей в формат JSON
#     return jsonify(data=candle_data)

get_5min_data_from_yfinance_and_save()

def get_data_by_date(target_date, limit=78):
    file_path = 'spx_data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    result_data = []
    target_datetime = datetime.strptime(target_date, '%d %m %Y')
    start_time = target_datetime.replace(hour=22, minute=30)
    end_time = start_time + timedelta(days=1, hours=4, minutes=55)

    count = 0 
    
    for point in data:
        x_datetime_str = point['x']
        x_datetime = datetime.strptime(point['x'], '%d %m %Y %H:%M')
        if start_time <= x_datetime <= end_time:
            result_data.append(point)
            count += 1
            if count >= limit:
                break  # Прекращаем поиск, если достигнуто ограничение

    return result_data
@app.route('/5min', methods=['POST'])

def receive_data():
    # Получаем данные из запроса
    data = request.json

    # Извлекаем строку даты из объекта, полученного от клиента
    x_date_str = data

    # Получаем данные из файла по указанной дате
    data_by_date = get_data_by_date(x_date_str)

    # Выводим данные по указанной дате в консоль сервера
    print("Print", data_by_date)

    # Отправляем данные по указанной дате в формате JSON клиенту
    return jsonify(data=data_by_date)
    return jsonify(200)

def get_5min_data():
    try:
        # Получаем данные от клиента
        client_data = request.data.decode('utf-8')
        
        # Выводим данные от клиента в консоль
        print("Данные от клиента:", client_data)
    # Возвращаем успешный ответ клиенту с кодом 200
        return jsonify(success=True), 200
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Возвращаем ошибку клиенту с кодом 500
        return 'Ошибка сервера', 500

if __name__ == "__main__":
    app.run(port=8000)