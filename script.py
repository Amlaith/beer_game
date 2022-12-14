# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EnmOfDlcAecXRj5LsmwwhzX6okINQMqW
"""

import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os


# Объявления классов агантов
class Agent():
  def __init__(self, prev=None, next=None):
    self.prev = prev
    self.next = next

class Factory(Agent):
  def __init__(self, prev=None):
    super().__init__(prev=prev)

  def turn(self, from_prev):
    return from_prev

class Consumer(Agent):
  def __init__(self, next=None, orders=[4] * 12 + [9] + [5] * 39):
    super().__init__(next=next)
    self.orders = orders
    self.received = []
  
  def play(self):
    for order in self.orders:
      self.received.append(self.next.turn(order))
    return self.received

class Player(Agent):
  def __init__(self, prev=None, next=None, panic=1, name='Anonymous'):
    super().__init__(prev, next)
    self.name = name
    self.panic = panic
    self.stock = 16
    self.deficit = 0
    self.stock_log = [self.stock]
    self.deficit_log = [self.deficit]
    self.balance = [self.stock]

  def __repr__(self):
    return self.name

  # Действия игрока в каждый ход  
  def turn(self, from_prev):
    to_ship = from_prev + self.deficit  # Надо отгрузить
    if to_ship > self.stock: # Если не хватает - дефицит
      self.deficit = to_ship - self.stock
      to_ship = self.stock
    else:
      self.deficit = 0
    self.deficit_log.append(self.deficit)
    self.stock = self.stock - to_ship  # Запасы
    self.stock_log.append(self.stock)
    self.balance.append(2 * self.deficit + self.stock)  # Стоимость
    
    # Заказываем больше нужного
    to_next = int(from_prev * self.panic)
    if to_next > self.stock:
      self.stock = self.stock + self.next.turn(to_next - self.stock)
    else:
      self.next.turn(0)  

    return to_ship


# Заголовок
st.write('# Beer Game')


# Иллюстрации процесса игры
path = os.path.dirname(__file__)
st.image(path+'/media/order_flow.png')
st.image(path+'/media/goods_flow.png')


# Параметры игры
players = {
    'Петя': 1.5,
    'Коля': 1.5,
    'Таня': 1.5,
    'Света': 1.5,
}

cols = st.columns(len(players))
for i, name in enumerate(players.keys()):
  players[name] = cols[i].slider(f'**{name}** ожидает, что объем каждого следующего заказа составит столько от объема предыдущего заказа: ', .5, 3., 1.5, .1)

orders_blueprint = [4] * 12 + [9] + [4] * 39
orders = [0] * 52
with st.expander('Посмотреть заказы потребителя:'):
  qs = st.columns(4)
  for i, q in enumerate(qs):
    q.write(f'{i+1}-й квартал')
  for i in range(52):
    orders[i] = qs[i // 13].number_input(f'Неделя {i+1}:', 0, 100, orders_blueprint[i])


# Создание агентов
chain = [Player(panic=panic_level, name=name) for name, panic_level in players.items()]
consumer = Consumer(next=chain[0], orders=orders)
factory = Factory(prev=chain[3])
chain[0].prev = consumer
chain[0].next = chain[1]
chain[1].prev = chain[0]
chain[1].next = chain[2]
chain[2].prev = chain[1]
chain[2].next = chain[3]
chain[3].prev = chain[2]
chain[3].next = factory


# Старт игры
consumer.play();


# Итоговый график
fig, ax = plt.subplots()
for player in chain:
  ax = plt.plot(player.balance, label=player)
leg = plt.legend()
plt.ylabel('Штраф')
plt.xlabel('Неделя')
plt.title('Размер штрафа')
st.pyplot(fig)

# График склада
fig, ax = plt.subplots()
for player in chain:
  ax = plt.plot(player.stock_log, label=player)
leg = plt.legend()
plt.ylabel('Наличие')
plt.xlabel('Неделя')
plt.title('Наличие на складе')
st.pyplot(fig)

# График дефицита
fig, ax = plt.subplots()
for player in chain:
  ax = plt.plot(player.deficit_log, label=player)
leg = plt.legend()
plt.ylabel('Дефицит')
plt.xlabel('Неделя')
plt.title('Размер дефицита')
st.pyplot(fig)


# Показать исходный код всего скрипта
with st.expander('Посмотреть код:'):
  with open("script.py", encoding='utf-8') as f:
      lines_to_display = f.read()
  st.code(lines_to_display, "python")

