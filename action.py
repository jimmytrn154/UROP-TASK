import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# Load dataset
with open('edinburgh_knn2rest.json', 'r') as file:
    data = json.load(file)

# Step 1: Extract keywords and associate them with restaurant candidates
restaurant_to_keywords = defaultdict(set)
for user_id, user_data in data.items():
    keywords = user_data.get('kw', [])
    candidates = user_data.get('candidate', [])
    
    for candidate, keyword in zip(candidates, keywords):
        restaurant_to_keywords[candidate].add(keyword)

# Step 2: Map restaurant names for readability
restaurant_labels = {rest: f'Restaurant {i+1}' for i, rest in enumerate(restaurant_to_keywords.keys())}

# Step 3: Filter specific keywords
selected_keywords = {'sushi', 'milk', 'pizza'}
filtered_edges = []
for restaurant, keywords in restaurant_to_keywords.items():
    readable_restaurant = restaurant_labels[restaurant]
    for keyword in keywords:
        if keyword in selected_keywords:
            filtered_edges.append((keyword, readable_restaurant))

# Step 4: Initialize a bipartite graph
B = nx.Graph()

# Add nodes and edges only for the filtered keywords
B.add_nodes_from([edge[0] for edge in filtered_edges], bipartite=0)  # Keyword nodes
B.add_nodes_from([edge[1] for edge in filtered_edges], bipartite=1)  # Restaurant nodes
B.add_edges_from(filtered_edges)

# Step 5: Visualize the filtered graph
plt.figure(figsize=(12, 8))

# Using spring layout for spacing
pos = nx.spring_layout(B, seed=42)

# Draw restaurant and keyword nodes with distinct colors
restaurant_nodes = [node for node in B.nodes if node in restaurant_labels.values()]
keyword_nodes = [node for node in B.nodes if node not in restaurant_labels.values()]

nx.draw_networkx_nodes(B, pos, nodelist=restaurant_nodes, node_color="lightgreen", node_size=500, label="Restaurants")
nx.draw_networkx_nodes(B, pos, nodelist=keyword_nodes, node_color="lightblue", node_size=400, label="Keywords")

# Draw edges
nx.draw_networkx_edges(B, pos, width=1.2)

# Draw labels for both restaurants and keywords
nx.draw_networkx_labels(B, pos, font_size=10)

plt.title('Keyword-Restaurant Relationships for Selected Keywords')
plt.legend(loc="upper right")
plt.show()
