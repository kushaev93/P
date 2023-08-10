import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Загрузка данных о ценах закрытия S&P 500 с помощью yfinance
data = yf.download('^GSPC', start='2023-01-01', end='2023-07-27')

# Вычисление тела свечи и определение цвета (зеленая или красная)
data['Body'] = data['Close'] - data['Open']
data['Color'] = data['Body'].apply(lambda x: 'green' if x > 0 else 'red')

# Создание индикатора (1 - свеча с телом > 10, 0 - свеча с телом <= 10)
data['Indicator'] = data['Body'].apply(lambda x: 1 if abs(x) > 10 else 0)

# Создание столбца 'Body Range'
data['Body Range'] = data['Body'].apply(lambda x: '20-25' if 20 <= abs(x) <= 25 else ('25-30' if 25 < abs(x) <= 30 else ('30-35' if 30 < abs(x) <= 35 else None)))

# Функция-генератор для анализа индикатора 0-1-1-0
def analyze_indicator(data):
    i = 0
    counter = 0
    while i < len(data) - 3:
        if data['Indicator'][i] == 0 and data['Indicator'][i + 1] == 1 and data['Indicator'][i + 2] == 1 and data['Indicator'][i + 3] == 0:
            counter += 1
            i += 4
        else:
            i += 1
    return counter

# Функция-генератор для анализа индикатора 0-1-0
def analyze_indicator_010(data):
    i = 0
    counter = 0
    while i < len(data) - 2:
        if data['Indicator'][i] == 0 and data['Indicator'][i + 1] == 1 and data['Indicator'][i + 2] == 0:
            counter += 1
            i += 3
        else:
            i += 1
    return counter

# Функция-генератор для анализа индикатора 0-1
def analyze_indicator_01(data):
    i = 0
    counter = 0
    while i < len(data) - 1:
        if data['Indicator'][i] == 0 and data['Indicator'][i + 1] == 1:
            counter += 1
            i += 2
        else:
            i += 1
    return counter

# Функция-генератор для анализа индикатора 1-0-1
def analyze_indicator_101(data):
    i = 0
    counter = 0
    while i < len(data) - 2:
        if data['Indicator'][i] == 1 and data['Indicator'][i + 1] == 0 and data['Indicator'][i + 2] == 1:
            counter += 1
            i += 3
        else:
            i += 1
    return counter

# Вызов функций для анализа индикаторов
counter_0110 = analyze_indicator(data)
counter_010 = analyze_indicator_010(data)
counter_01 = analyze_indicator_01(data)
counter_101 = analyze_indicator_101(data)

# Подсчет количества зеленых и красных свечей
green_candles = data[data['Color'] == 'green'].shape[0]
red_candles = data[data['Color'] == 'red'].shape[0]

# Подсчет количества свечей с телом менее 10 пунктов и более 10 пунктов
indicator_0_count = data[data['Indicator'] == 0].shape[0]
indicator_1_count = data[data['Indicator'] == 1].shape[0]

# Подсчет количества свечей с различными значениями тела
body_20_25_count = data[data['Body Range'] == '20-25'].shape[0]
body_25_30_count = data[data['Body Range'] == '25-30'].shape[0]
body_30_35_count = data[data['Body Range'] == '30-35'].shape[0]

# Подсчет общего количества свечей
total_candles = len(data)

# Создание подграфиков с двумя осями y
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

# Добавление свечей на первый подграфик
fig.add_trace(go.Candlestick(x=data.index,
                             open=data['Open'],
                             high=data['High'],
                             low=data['Low'],
                             close=data['Close'],
                             increasing_line_color='green',
                             decreasing_line_color='red',
                             name='Свечи',
                             hovertext=data['Body'].round(2)),
              row=1, col=1)

# Добавление индикатора (линии) на второй подграфик
fig.add_trace(go.Scatter(x=data.index,
                         y=data['Indicator'],
                         mode='lines',
                         line=dict(color='blue', width=1.5),
                         name='Индикатор'),
              row=2, col=1)

# Настройка макета графика
fig.update_layout(title='SPX',
                  xaxis_title='Дата',
                  xaxis_rangeslider_visible=False,
                  xaxis_rangeslider_thickness=0.05,
                  yaxis=dict(showgrid=True, gridcolor='lightgray'),
                  yaxis2=dict(showgrid=True, gridcolor='lightgray'),
                  paper_bgcolor='white',
                  plot_bgcolor='white')

# Настройка оси y2 для второго подграфика (индикатор)
fig.update_yaxes(title='Индикатор', range=[-0.5, 1.5], showgrid=True, zeroline=False, showline=False, side='right', row=2, col=1)

# Добавление аннотаций с количеством красных и зеленых свечей
fig.add_annotation(text=f"Красных свечей: {red_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=1.1,
                   showarrow=False,
                   font=dict(size=12, color="red"))

fig.add_annotation(text=f"Зелёных свечей: {green_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=1.05,
                   showarrow=False,
                   font=dict(size=12, color="green"))

# Добавление аннотаций с количеством свечей с телом менее 10 пунктов и более 10 пунктов
fig.add_annotation(text=f"Индикатор 0: {indicator_0_count}",
                   xref="paper", yref="y2",
                   x=0.98, y=0.3,
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Индикатор 1: {indicator_1_count}",
                   xref="paper", yref="y2",
                   x=0.98, y=0.2,
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Добавление аннотаций с количеством свечей с различными значениями тела
fig.add_annotation(text=f"Тело 20-25: {body_20_25_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.95,
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Тело 25-30: {body_25_30_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.9,
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Тело 30-35: {body_30_35_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.85,
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Добавление аннотации с общим количеством свечей
fig.add_annotation(text=f"Общее количество свечей: {total_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.8,
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Загрузка 5-минутных данных для S&P 500 за последний день (если они доступны)
try:
    data_5min = yf.download('^GSPC', start='2023-07-26', end='2023-07-26', interval='5m')
    data_5min = data_5min.tz_convert(None)  # Удаление информации о временной зоне для совместимости с дневным графиком
except Exception as e:
    print(f"Failed download: {e}")

# Создание подписи с датой и ценой закрытия при наведении курсора на дневную свечу
fig.add_trace(go.Scatter(x=[],
                         y=[],
                         mode='lines',
                         line=dict(dash='dash', color='gray', width=1),
                         name='Пунктирная линия',
                         hoverinfo='text',
                         hovertext='Дата: %{x|%Y-%m-%d}<br>Цена закрытия: %{y:.2f}<br>Тело свечи: %{text}'),
              row=1, col=1)

fig.update_layout(hovermode='x unified')

# Обновление подписи с датой и ценой закрытия при наведении курсора на дневную свечу
def update_annotation(trace, points, selector):
    x_coord = points.xs[0]
    y_coord = data.loc[x_coord, 'Close']
    body_value = data.loc[x_coord, 'Body']

    # Удаление существующих аннотаций
    fig.update_annotations(annotations=[])

    # Отображение аннотаций из DataFrame, если они есть для текущей даты
    current_date_annotations = annotations_df[annotations_df['Date'] == x_coord]['Annotation']
    for i, annotation in enumerate(current_date_annotations):
        fig.add_annotation(text=annotation, x=x_coord, y=0.95 - i * 0.05, showarrow=False, font=dict(size=12, color="black"))

    # Обновление 5-минутного графика в подписи, если данные доступны
    if 'data_5min' in globals():
        fig.update_traces(x=data_5min.index, y=data_5min['Close'], selector=dict(name="Пунктирная линия"))

    return f"Дата: {x_coord.strftime('%Y-%m-%d')}<br>Цена закрытия: {y_coord:.2f}<br>Тело свечи: {body_value:.2f}"

# Установка функции обновления подписи при наведении курсора на дневной график
fig.data[0].on_hover(update_annotation)

# Создание DataFrame для аннотаций
annotations_df = pd.DataFrame({
    'Date': pd.to_datetime(['2023-06-01', '2023-06-02']),
    'Annotation': ['Аннотация для 2023-06-01', 'Аннотация для 2023-06-02']
})

# Добавление аннотаций из DataFrame на график (датафрейм annotations_df должен содержать дату и соответствующую аннотацию)
for i, annotation in annotations_df.iterrows():
    fig.add_annotation(text=annotation['Annotation'], x=annotation['Date'], y=0.95 - i * 0.05, showarrow=False, font=dict(size=12, color="black"))

# Отображение графика
fig.show()
