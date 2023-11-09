# Importamos las bibliotecas necesarias
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_cors import CORS
import networkx as nx
import json

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)
# Habilitamos CORS para la aplicación
CORS(app)

# Creamos un gráfico aleatorio y establecemos el nodo seleccionado inicialmente en 0
G = nx.random_regular_graph(6, 36)

selected_node = 0
Planetas = []
# Ruta de inicio que renderiza la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar un nodo al gráfico
@app.route('/add_node')
def add_node():
    # Obtenemos el ID del nuevo nodo
    node_id = len(G)
    # Agregamos el nuevo nodo al gráfico con su descripción
    G.add_node(node_id, description=descripciones[node_id])
    # Conectamos el nuevo nodo a los primeros 6 nodos existentes
    for other_node_id in range(max(0, node_id - 6), node_id):
        G.add_edge(node_id, other_node_id)
    # Devolvemos los datos del gráfico en formato JSON
    return jsonify(nx.node_link_data(G))

# Ruta para eliminar un nodo del gráfico
# Ruta para eliminar un nodo del gráfico


@app.route('/remove_node')
def remove_node():
    # Aquí deberías tener la lógica para eliminar un nodo de tu grafo
    # Por ejemplo:
    if len(G.nodes) > 0:
        G.remove_node(list(G.nodes)[-1])  # Elimina el último nodo

    # Obtenemos los datos del gráfico
    data = nx.node_link_data(G)
    # Devolvemos los datos en formato JSON
    return jsonify(data)


# Ruta para seleccionar un nodo
@app.route('/select_node/<int:node_id>')
def select_node(node_id):
    global selected_node

    # Verifica si el nodo existe en el gráfico
    if node_id not in G:
        return jsonify({'error': 'Node not found'}), 404

    # Establece el nuevo nodo seleccionado
    selected_node = node_id

    # Obtiene los nodos adyacentes al nodo seleccionado
    adjacent_nodes = list(G.adj[node_id])

    # Prepara los datos para devolver
    data = nx.node_link_data(G)
    data['adjacent_nodes'] = adjacent_nodes

    # Devuelve los datos en formato JSON
    return jsonify(data)


# Ruta para obtener los datos del gráfico
@app.route('/graph_data')
def graph_data():
    # Obtenemos los datos del gráfico
    data = nx.node_link_data(G)
    # Devolvemos los datos en formato JSON
    return jsonify(data)

# Punto de entrada principal de la aplicación
if __name__ == "__main__":
    app.run(debug=True)