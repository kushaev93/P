import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Загрузка данных о ценах закрытия S&P 500 с yfinance
data = yf.download('^GSPC', start='2023-01-01', end='2023-07-25')

# Вычисление тела свечи и определение цвета (зелёная или красная)
data['Body'] = data['Close'] - data['Open']
data['Color'] = data['Body'].apply(lambda x: 'green' if x > 0 else 'red')

# Создание индикатора (1 - свеча с телом > 10, 0 - свеча с телом <= 10)
data['Indicator'] = data['Body'].apply(lambda x: 1 if abs(x) > 10 else 0)

# Создание счетчиков для свечей с различными значениями тела
data['Body Range'] = data['Body'].apply(lambda x: '20-25' if 20 <= abs(x) <= 25 else ('25-30' if 25 < abs(x) <= 30 else ('30-35' if 30 < abs(x) <= 35 else None)))

# Подсчет количества красных и зеленых свечей
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
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

# Добавление свечей на первый подграфик
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='green',  # Задаем цвет для зеленых свечей
                decreasing_line_color='red',    # Задаем цвет для красных свечей
                name='Свечи',
                hovertext=data['Body'].round(2)), row=1, col=1)

# Добавление индикатора (линии) на второй подграфик
fig.add_trace(go.Scatter(x=data.index,
               y=data['Indicator'],
               mode='lines',
               line=dict(color='blue', width=1.5),  # Изменяем цвет и толщину линии индикатора
               name='Индикатор'), row=2, col=1)

# Настройка макета графика
fig.update_layout(title='SPX',
                  xaxis_title='Дата',
                  xaxis_rangeslider_visible=False,
                  xaxis_rangeslider_thickness=0.05,   # Уменьшаем толщину ползунка для масштабирования
                  yaxis=dict(showgrid=True, gridcolor='lightgray'),  # Добавляем сетку на оси y
                  yaxis2=dict(showgrid=True, gridcolor='lightgray'),  # Добавляем сетку на оси y2 (индикатор)
                  paper_bgcolor='white',  # Изменяем цвет фона
                  plot_bgcolor='white',   # Изменяем цвет области графика
)

# Настройка оси y2 для второго подграфика (индикатор)
fig.update_yaxes(title='Индикатор', range=[-0.5, 1.5], showgrid=True, zeroline=False, showline=False, side='right', row=2, col=1)

# Добавление аннотаций с количеством красных и зеленых свечей
fig.add_annotation(text=f"Красных свечей: {red_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=1.1,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="red"))

fig.add_annotation(text=f"Зелёных свечей: {green_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=1.05,   # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="green"))

# Добавление аннотаций с количеством свечей с телом менее 10 пунктов и более 10 пунктов
fig.add_annotation(text=f"Индикатор 0: {indicator_0_count}",
                   xref="paper", yref="y2",
                   x=0.98, y=0.3,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Индикатор 1: {indicator_1_count}",
                   xref="paper", yref="y2",
                   x=0.98, y=0.2,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Добавление аннотаций с количеством свечей с различными значениями тела
fig.add_annotation(text=f"Тело 20-25: {body_20_25_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.95,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Тело 25-30: {body_25_30_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.9,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

fig.add_annotation(text=f"Тело 30-35: {body_30_35_count}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.85,    # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Добавление аннотации с общим количеством свечей
fig.add_annotation(text=f"Общее количество свечей: {total_candles}",
                   xref="paper", yref="paper",
                   x=0.98, y=0.8,   # Позиция аннотации
                   showarrow=False,
                   font=dict(size=12, color="black"))

# Создание подписи с датой и ценой закрытия при наведении курсора
fig.add_trace(go.Scatter(x=[], y=[],
               mode='lines',
               line=dict(dash='dash', color='gray', width=1),
               name='Пунктирная линия',
               hoverinfo='text',
               hovertext='Дата: %{x|%Y-%m-%d}<br>Цена закрытия: %{y:.2f}<br>Тело свечи: %{text}'), row=1, col=1)

fig.update_layout(hovermode='x unified')

# Обновление подписи с датой и ценой закрытия при наведении курсора
def update_annotation(trace, points, selector):
    x_coord = points.xs[0]
    y_coord = data.loc[x_coord, 'Close']
    body_value = data.loc[x_coord, 'Body']
    fig.update_traces(x=[x_coord, x_coord], y=[data['Low'].min(), data['High'].max()], selector=dict(name='Пунктирная линия'))
    fig.update_annotations(text=f"Дата: {x_coord.strftime('%Y-%m-%d')}<br>Цена закрытия: {y_coord:.2f}<br>Тело свечи: {body_value:.2f}",
                           xref="x", yref="y",
                           x=x_coord, y=y_coord,
                           showarrow=False,
                           font=dict(size=10, color="black"))

fig.data[0].on_hover(update_annotation)

# Отображение графика
fig.show()
