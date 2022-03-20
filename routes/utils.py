from trains.models import Train


# Поиск всех возможных маршрутов из пункта А в пункт В
def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


# Создание графа, словарь со связями городов
def get_graph(queryset):
    graph = {}
    for query in queryset:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
    return graph


# Функция по поиску нужного пользователю маршрута
def get_routes(request, form) -> dict:
    context = {'form': form}
    trains_queryset = Train.objects.all()
    graph = get_graph(trains_queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travel_time = data['travel_time']
    # Все возможные маршруты из города(from_city) в город(to_city) которые задаются пользователем в форме поиска
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    # Если таких маршрутов нет, т.е. список с маршрутами пуст
    if not len(all_ways):
        raise ValueError('Маршрута, удовлетворяющего условиям, не существует')
    # По маршруту из пункта А в пункт B можно задать список городов через которые хочет проехать пользователь,
    # в cities - список этих городов, далее проверка, встречаются ли эти города по пути из пункта А в пункт В
    # маршрут состоит из id городов, соберем все возможные маршруты и отберем лишь те, в которых есть все города
    # из переменной cities, т.е. такие маршруты которые удовлетворяют заданному списку cities.
    if cities:
        # генератор на основе списка городов которые необходимо проехать
        through_city = [city.id for city in cities]
        # в переменную right_ways будем заносить удовлетворяющие поиску маршруты
        right_ways = []
        # все существующие маршруты, в них будем искать маршруты, в которых есть города, которые хочет
        # проехать пользователь, проходимся циклом по всем маршрутам
        for route in all_ways:
            # функция all() вернет нам или True т.е. все города из списка cities есть в маршруте, а значит
            # такой маршрут подходит, или False - не подходит.
            if all(city in route for city in through_city):
                # если маршрут найден, вносим его в список
                right_ways.append(route)
        # Если список пуст, т.е. таких маршрутов не нашлось
        if not right_ways:
            raise ValueError('Маршрут через эти города невозможен')
    # если не нужно проезжать через какие-либо города
    else:
        right_ways = all_ways

    # В форме поиска также можно задать желаемое время в пути. Далее пишем логику по поиску маршрута,
    # время в пути которого будет меньше или равно времени, которых задал пользователь в форме
    # Итоговая переменная с подходящим маршрутом
    appropriate_route = []
    # в all_trains ключом будет список городов from_city, to_city в которые и из которых ходят поезда,
    # а значением будет список поездов, которые эти города проходят
    all_trains = {}
    # Проходим циклом по trains_queryset(Train.objects.all()), создаём словарь с составным ключом
    # составной ключ это кортеж из городов(from -> to), а значение это поезда
    for query in trains_queryset:
        all_trains.setdefault((query.from_city_id, query.to_city_id), [])
        all_trains[(query.from_city_id, query.to_city_id)].append(query)
    # проходимся по ранее отобранным маршрутам, с проверками по городам
    for route in right_ways:
        routes_data = {}
        routes_data['trains'] = []
        # в total_time запишем сумму времени всех отрезков маршрута
        total_time = 0
        # проходимся в цикле по route. В route хранится список состоящий из id городов, первый и последний
        # элемент списка это пункт А и В, между ними города которые хочет проехать пользователь, если таковые есть.
        # Задача в том, чтобы вытаскивать в цикле каждую пару городов и суммировать время в переменную total_time
        for city_pair in range(len(route) - 1):
            # Вытаскиваем первую пару городов в маршруте
            pair = all_trains[(route[city_pair], route[city_pair + 1])]
            # pair это список, состоящий из пары городов, через индексирование вытаскиваем эту пару и
            # берём нужный атрибут т.е. travel_time
            pair_instanse = pair[0]
            # Накапливаем время в переменной total_time
            total_time += pair_instanse.travel_time
        routes_data['total_time'] = total_time
        # если маршрут подходит по времени
        if total_time <= travel_time:
            # вносим его в список подходящих маршрутов
            appropriate_route.append(routes_data)
    # если ни один маршрут не подходит по времени
    if not appropriate_route:
        raise ValueError('Время в пути больше заданного')

    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context
