import networkx as nx
import plotly.graph_objects as go

def createGraph(commander_dict, connectionLimit=1):
    # Initialize the graph
    G = nx.Graph()
    F = nx.Graph()

    card_to_commanders = {}

    commanders = list(commander_dict.keys())

    # Add nodes and edges
    for commander, cards in commander_dict.items():
        # Failsafe for commander with no cards
        if cards == None:
            commander_dict[commander] = []
            cards = []
        # Add the commander node
        G.add_node(commander)
        
        # map each card to each commander they ahve
        for card in cards:
            if card not in card_to_commanders:
                card_to_commanders[card] = []
            card_to_commanders[card].append(commander)
            
    # Add edges between commanders that share a card and calculate shared card percentage
    for i in range(len(commander_dict)):

        if i % 50 == 0:
            print("Linking commanders: {0} / {1} complete".format(i, len(commander_dict)))

        for j in range(i + 1, len(commander_dict)):
            commander_a = commanders[i]
            commander_b = commanders[j]
                
           # Count shared cards
            shared_cards = len(set(commander_dict[commander_a]).intersection(commander_dict[commander_b]))
            total_cards = len(set(commander_dict[commander_a]).union(commander_dict[commander_b]))
            
            # add an edge if they share cards
            if shared_cards >= connectionLimit:
                # weightCalc = shared_cards / total_cards / connectionLimit

                # weightCalc = (shared_cards - connectionLimit) / (total_cards - connectionLimit)
                # weightCalc = (shared_cards - connectionLimit) / (total_cards - connectionLimit)

                weightCalc = (((1 + shared_cards - connectionLimit)  / total_cards))
                edgeCalc = (((1 + shared_cards - connectionLimit)  / total_cards) ** 1.5) / 2
                G.add_edge(commander_a, commander_b, weight=weightCalc) # edge weight is the % of cards shared, can use exponents if I feel like it
                F.add_edge(commander_a, commander_b, weight=edgeCalc) # Use this for the edge width (DISPLAY ONLY)
    # Create the layout for nodes, varying spring strength by edge weight
    # Different layouts to take for a spin
    # NOTE: upping the iteration count helps a lot
    pos = nx.spring_layout(G, seed=42, weight='weight', scale=10, k=0.15, iterations=200) # "standard" is .15
    # pos = nx.forceatlas2_layout(G, scaling_ratio=.00025, seed=42, max_iter=300) # this at c=30 rules
    # pos = nx.kamada_kawai_layout(G, weight='weight', scale=2) # I like it at a=40

    # iterations of at least 200 help a lot, same with upping the scale
    # cool settings:    
    # spring, iter=500+, scale=100, c=28 (a little messy but neat)
    # force, iter=500+, scale=0.0001, ~c=30

    edge_x = []
    edge_y = []
    edge_widths = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        edge_width = F[u][v]['weight'] * 10
        edge_widths.append(edge_width)
        edge_widths.append(None) # filler to make my later loop clean
        edge_widths.append(None) # filler to make my later loop clean

    # edges are [x0, x1, None] so loop every three values
    edge_trace_list = []
    for i in range(0, len(edge_x), 3):
        edge_trace_list.append( go.Scatter(
                                x=[edge_x[i], edge_x[i + 1]],
                                y=[edge_y[i], edge_y[i + 1]],
                                line=dict(width=edge_widths[i] / 10,color='#888'),
                                # line=dict(width=0.05,color='#888'),
                                hoverinfo='none',
                                mode='lines'))

    node_x = []
    node_y = []
    node_text = []
    node_adjacencies = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append('{0}: {1} connections'.format(node, len(list(G.neighbors(node)))))
        adjacencies = len(list(G.neighbors(node)))
        node_adjacencies.append(adjacencies)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=4, # 10
            colorbar=dict(
                thickness=15,
                title=dict(
                text='Node Connections',
                side='right'
                ),
                xanchor='left',
            ),
            line_width=1))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=edge_trace_list + [node_trace],
                layout=go.Layout(
                    title=dict(
                        text="Commander Similarity Data<br> min shared = {0}".format(connectionLimit),
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()