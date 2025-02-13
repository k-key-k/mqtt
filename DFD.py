from graphviz import Digraph

dfd = Digraph('DFD', format='png')
dfd.attr(rankdir='LR', size='30')
dfd.attr('node', fontsize='60')
dfd.attr('edge', fontsize='45')

dfd.node('User', 'Пользователь', shape='rectangle')

dfd.node('GUI', 'GUI (Ввод/Вывод)', shape='circle')
dfd.node('NN1', 'Нейросеть №1', shape='circle')
dfd.node('NN2', 'Нейросеть №2', shape='circle')
dfd.node('Fuzz', 'Фаззификатор', shape='circle')
dfd.node('ES', 'Экспертная система\n(scikit-fuzzy)', shape='circle')
dfd.node('Defuzz', 'Дефаззификатор', shape='circle')
dfd.node('Aggregator', 'Агрегатор данных', shape='circle')

dfd.node('DB', 'База данных (SQLite)', shape='cylinder')

dfd.edge('User', 'GUI', label='Ввод данных')
dfd.edge('GUI', 'NN1', label='Исходные данные')
dfd.edge('NN1', 'NN2', label='Характеристики полимеров')
dfd.edge('NN2', 'Fuzz', label='Коэффициент уверенности')
dfd.edge('Fuzz', 'ES', label='Нечеткий ввод')
dfd.edge('ES', 'Defuzz', label='Нечеткий вывод')
dfd.edge('Defuzz', 'Aggregator', label='Качественный анализ')
dfd.edge('Aggregator', 'GUI', label='Результаты')
dfd.edge('Aggregator', 'DB', label='Сохранение данных')
dfd.edge('DB', 'GUI', label='Статус операции')

dfd.attr(dpi='1000')

dfd.render('C:/Users/Admin/PycharmProjects/dfd_expert_system', view=False)
'/mnt/data/dfd_expert_system.png'
