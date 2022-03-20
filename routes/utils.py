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
    return context
