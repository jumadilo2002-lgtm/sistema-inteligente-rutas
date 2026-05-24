import csv
import heapq
from collections import defaultdict



# CARGA DE LA BASE DE CONOCIMIENTO

def load_knowledge_base(file_path: str):

    graph = defaultdict(dict)

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                origin = row["origin"]
                destination = row["destination"]
                cost = int(row["cost"])
                route_name = row["route_name"]

                # Regla lógica almacenada en el grafo
                graph[origin][destination] = {
                    "cost": cost,
                    "route": route_name,
                }

        return dict(graph)

    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

    except Exception as e:
        raise RuntimeError(f"Error procesando la base de conocimiento: {e}")



# OBTENER TODOS LOS NODOS

def get_all_nodes(graph):
    """
    Obtiene todos los nodos del grafo,
    incluyendo los que solo aparecen como destino.
    """

    nodes = set(graph.keys())

    for neighbors in graph.values():
        nodes.update(neighbors.keys())

    return nodes



# ALGORITMO A*

def a_star_search(graph, start, goal, heuristics):
    """
    Ejecuta el algoritmo A* para encontrar
    la ruta óptima de menor costo.
    """

    all_nodes = get_all_nodes(graph)

    # Validación de nodos
    if start not in all_nodes or goal not in all_nodes:
        raise ValueError("El nodo inicial o el nodo destino no existen.")

    # Cola de prioridad:
    # (f_cost, g_cost, nodo_actual, camino, rutas_usadas)
    open_set = []

    heapq.heappush(
        open_set,
        (
            heuristics.get(start, 0),
            0,
            start,
            [start],
            [],
        ),
    )

    # Costos mínimos encontrados
    g_costs = {node: float("inf") for node in all_nodes}
    g_costs[start] = 0

    while open_set:

        f_cost, current_g, current_node, path, routes = heapq.heappop(open_set)

        # Si llegamos al destino
        if current_node == goal:
            return path, routes, current_g

        # Explorar vecinos
        for neighbor, data in graph.get(current_node, {}).items():

            travel_cost = data["cost"]
            route_name = data["route"]

            tentative_g = current_g + travel_cost

            # Si encontramos un mejor camino
            if tentative_g < g_costs.get(neighbor, float("inf")):

                g_costs[neighbor] = tentative_g

                # Heurística estimada
                h_cost = heuristics.get(neighbor, 0)

                # Fórmula A*
                new_f_cost = tentative_g + h_cost

                # Actualizar camino
                new_path = list(path)
                new_path.append(neighbor)

                # Guardar rutas utilizadas
                new_routes = list(routes)
                new_routes.append(route_name)

                heapq.heappush(
                    open_set,
                    (
                        new_f_cost,
                        tentative_g,
                        neighbor,
                        new_path,
                        new_routes,
                    ),
                )

    # No existe ruta posible
    return None, None, float("inf")



# PROGRAMA PRINCIPAL

if __name__ == "__main__":

    print("=" * 60)
    print(" SISTEMA INTELIGENTE DE RUTAS DE TRANSPORTE ")
    print("=" * 60)

  
    # 1. Cargar base de conocimiento

    csv_file = "transit_routes.csv"

    transit_graph = load_knowledge_base(csv_file)


    # 2. Heurísticas

    # Estimación aproximada en minutos
    # hasta el nodo objetivo: Mirolindo
    heuristics = {
        "Centro": 30,
        "Estadio": 25,
        "Terminal": 20,
        "UCC": 10,
        "Mirolindo": 0,
        "Hospital": 22,
        "Salado": 18,
        "UniversidadTolima": 12,
        "Aeropuerto": 8,
    }

    # 3. Entrada del usuario

    start_node = input("\nIngrese el punto de inicio: ").strip().title()

    goal_node = input("Ingrese el destino: ").strip().title()

    # 4. Ejecutar búsqueda
   
    try:

        path, routes, total_cost = a_star_search(
            transit_graph,
            start_node,
            goal_node,
            heuristics,
        )

    
        # 5. Mostrar resultados

        if path:

            print("\nRUTA ÓPTIMA ENCONTRADA")
            print("-" * 60)

            # Mostrar nodos
            print("Trayecto:")
            print(" -> ".join(path))

            print("\nRutas utilizadas:")

            for i in range(len(routes)):
                print(f"{path[i]} -> {path[i + 1]}" f" usando {routes[i]}")

            print(f"\nCosto total: {total_cost} minutos")

        else:
            print("No se encontró una ruta válida " "según las reglas actuales.")

    except ValueError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nError inesperado: {e}")
