from trains.models import Train


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


def get_graph(queryset):
    graph = {}
    for query in queryset:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    trains_queryset = Train.objects.all()
    graph = get_graph(trains_queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    travel_time = data['travel_time']
    all_ways = dfs_paths(graph, from_city.id, to_city.id)
    if not len(list(all_ways)):
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')

    return context
