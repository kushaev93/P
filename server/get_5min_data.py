import yfinance as yf
import datetime as dt
import json
import pandas as pd

def convert_timestamp_to_datetime(timestamp):
    date = dt.datetime.fromtimestamp(timestamp // 1000)  # Преобразование миллисекунд в секунды
    formatted_date = date.strftime('%d %m %Y %H:%M')
    return formatted_date

def get_5min_data_from_yfinance_and_save():
    try:
        # Получаем текущую дату
        end_date = dt.datetime.now().strftime('%Y-%m-%d')

        # Создаем объект Ticker для индекса SPX
        spx_ticker = yf.Ticker('^GSPC')

        # Получаем начало года
        start_date = dt.datetime(dt.datetime.now().year, 1, 1).strftime('%Y-%m-%d')

        # Загружаем исторические данные для 5-минутных интервалов
        spx_data = None
        chunk_size = 40  # Задайте размер куска, например, 60 дней
        for i in range(0, 365, chunk_size):
            start_chunk = dt.datetime(dt.datetime.now().year, 1, 1) + dt.timedelta(days=i)
            end_chunk = start_chunk + dt.timedelta(days=chunk_size)
            spx_chunk = spx_ticker.history(start=start_chunk, end=end_chunk, interval='5m')
            if spx_data is None:
                spx_data = spx_chunk
            else:
                spx_data = pd.concat([spx_data, spx_chunk])

        # Преобразуем данные о свечах в формат списка, как ожидается клиентом
        candle_data = []
        for index, row in spx_data.iterrows():
            candle_info = {
                'x': convert_timestamp_to_datetime(index.timestamp() * 1000),  # Преобразование даты в нужный формат
                'y': [row['Open'], row['High'], row['Low'], row['Close']]
            }
            candle_data.append(candle_info)

        # Сохраняем данные в файл 'spx_data.json' в формате JSON
        with open('spx_data.json', 'w') as file:
            json.dump(candle_data, file)

        print("Данные 5-минутного графика с начала года сохранены в файл 'spx_data.json'.")

    except Exception as e:
        print(f"Не удалось загрузить данные: {e}")