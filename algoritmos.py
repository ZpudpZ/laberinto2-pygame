def dfs(laberinto, inicio, meta):
    stack = [inicio]
    caminos = {inicio: []}
    while stack:
        nodo = stack.pop()
        if nodo == meta:
            return caminos[nodo]
        for vecino in obtener_vecinos(laberinto, nodo):
            if vecino not in caminos:
                caminos[vecino] = caminos[nodo] + [vecino]
                stack.append(vecino)
    return []

def bfs(laberinto, inicio, meta):
    queue = [inicio]
    caminos = {inicio: []}
    while queue:
        nodo = queue.pop(0)
        if nodo == meta:
            return caminos[nodo]
        for vecino in obtener_vecinos(laberinto, nodo):
            if vecino not in caminos:
                caminos[vecino] = caminos[nodo] + [vecino]
                queue.append(vecino)
    return []

def obtener_vecinos(laberinto, nodo):
    x, y = nodo
    vecinos = []
    if x > 0 and laberinto[y][x - 1] != '1':
        vecinos.append((x - 1, y))
    if x < len(laberinto[0]) - 1 and laberinto[y][x + 1] != '1':
        vecinos.append((x + 1, y))
    if y > 0 and laberinto[y - 1][x] != '1':
        vecinos.append((x, y - 1))
    if y < len(laberinto) - 1 and laberinto[y + 1][x] != '1':
        vecinos.append((x, y + 1))
    return vecinos


import heapq


def greedy(laberinto, inicio, meta):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    filas, columnas = len(laberinto), len(laberinto[0])
    abiertas = []
    heapq.heappush(abiertas, (0, inicio))
    caminos = {inicio: []}
    while abiertas:
        _, actual = heapq.heappop(abiertas)

        if actual == meta:
            return caminos[actual]

        for vecino in obtener_vecinos(laberinto, actual):
            if vecino not in caminos:
                coste = heuristica(vecino, meta)
                heapq.heappush(abiertas, (coste, vecino))
                caminos[vecino] = caminos[actual] + [vecino]

    return []


def a_star(laberinto, inicio, meta):
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    filas, columnas = len(laberinto), len(laberinto[0])
    abiertas = []
    heapq.heappush(abiertas, (0 + heuristica(inicio, meta), inicio))
    costos = {inicio: 0}
    caminos = {inicio: []}

    while abiertas:
        _, actual = heapq.heappop(abiertas)

        if actual == meta:
            return caminos[actual]

        for vecino in obtener_vecinos(laberinto, actual):
            nuevo_coste = costos[actual] + 1  # Cada paso tiene un coste de 1
            if vecino not in costos or nuevo_coste < costos[vecino]:
                costos[vecino] = nuevo_coste
                heur = heuristica(vecino, meta)
                heapq.heappush(abiertas, (nuevo_coste + heur, vecino))
                caminos[vecino] = caminos[actual] + [vecino]

    return []
