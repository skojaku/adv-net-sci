# Module 09: Graph Neural Networks - Coding Implementation

## Basic GNN Concepts and Setup

### Environment Setup
```python
# Required libraries for GNN implementation
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv, GATConv, SAGEConv
import numpy as np
import matplotlib.pyplot as plt

# Check if CUDA is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
```

### Creating Graph Data Objects
```python
def create_graph_data(edge_list, node_features=None, node_labels=None):
    """Create PyTorch Geometric Data object from edge list"""
    
    # Convert edge list to tensor
    edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
    
    # Create node features (identity matrix if not provided)
    num_nodes = int(edge_index.max().item() + 1)
    if node_features is None:
        x = torch.eye(num_nodes, dtype=torch.float)
    else:
        x = torch.tensor(node_features, dtype=torch.float)
    
    # Create labels if provided
    if node_labels is not None:
        y = torch.tensor(node_labels, dtype=torch.long)
    else:
        y = None
    
    data = Data(x=x, edge_index=edge_index, y=y)
    return data

# Example: Create data from Zachary's Karate Club
import igraph
g = igraph.Graph.Famous('Zachary')
edges = g.get_edgelist()

# Create simple node features (degree, clustering coefficient)
degrees = g.degree()
clustering = g.transitivity_local_undirected()
clustering = [c if not np.isnan(c) else 0.0 for c in clustering]  # Handle NaN
node_features = [[deg, clust] for deg, clust in zip(degrees, clustering)]

# Create synthetic labels (split into two communities)
node_labels = [0 if i < 17 else 1 for i in range(g.vcount())]

data = create_graph_data(edges, node_features, node_labels)
print(f"Graph: {data.num_nodes} nodes, {data.num_edges} edges")
print(f"Node features shape: {data.x.shape}")
```

## Basic GNN Architectures

### Graph Convolutional Network (GCN)
```python
class SimpleGCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleGCN, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # First GCN layer
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Second GCN layer
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)

# Create and initialize model
model = SimpleGCN(input_dim=2, hidden_dim=16, output_dim=2)
print(model)
```

### Graph Attention Network (GAT)
```python
class SimpleGAT(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, heads=8):
        super(SimpleGAT, self).__init__()
        self.conv1 = GATConv(input_dim, hidden_dim, heads=heads, dropout=0.6)
        self.conv2 = GATConv(hidden_dim * heads, output_dim, heads=1, dropout=0.6)
        self.dropout = nn.Dropout(0.6)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # First GAT layer
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = self.dropout(x)
        
        # Second GAT layer
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)

gat_model = SimpleGAT(input_dim=2, hidden_dim=8, output_dim=2)
```

### GraphSAGE
```python
class SimpleGraphSAGE(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleGraphSAGE, self).__init__()
        self.conv1 = SAGEConv(input_dim, hidden_dim)
        self.conv2 = SAGEConv(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)

sage_model = SimpleGraphSAGE(input_dim=2, hidden_dim=16, output_dim=2)
```

## Training and Evaluation

### Node Classification Training
```python
def train_node_classification(model, data, train_mask, val_mask, epochs=200):
    """Train GNN for node classification"""
    
    model = model.to(device)
    data = data.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    criterion = nn.NLLLoss()
    
    model.train()
    train_losses = []
    val_accuracies = []
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data)
        
        # Compute loss on training nodes
        loss = criterion(out[train_mask], data.y[train_mask])
        loss.backward()
        optimizer.step()
        
        train_losses.append(loss.item())
        
        # Evaluate on validation set
        if epoch % 10 == 0:
            model.eval()
            with torch.no_grad():
                pred = model(data).argmax(dim=1)
                val_acc = (pred[val_mask] == data.y[val_mask]).float().mean()
                val_accuracies.append(val_acc.item())
                print(f'Epoch {epoch:03d}, Loss: {loss:.4f}, Val Acc: {val_acc:.4f}')
            model.train()
    
    return train_losses, val_accuracies

# Create train/val splits
num_nodes = data.num_nodes
train_mask = torch.zeros(num_nodes, dtype=torch.bool)
val_mask = torch.zeros(num_nodes, dtype=torch.bool)
test_mask = torch.zeros(num_nodes, dtype=torch.bool)

# Split nodes
indices = np.random.permutation(num_nodes)
train_mask[indices[:int(0.6 * num_nodes)]] = True
val_mask[indices[int(0.6 * num_nodes):int(0.8 * num_nodes)]] = True
test_mask[indices[int(0.8 * num_nodes):]] = True

# Train models
print("Training GCN...")
gcn_losses, gcn_val_accs = train_node_classification(model, data, train_mask, val_mask)

print("\nTraining GAT...")
gat_losses, gat_val_accs = train_node_classification(gat_model, data, train_mask, val_mask)
```

### Model Evaluation
```python
def evaluate_model(model, data, test_mask):
    """Evaluate trained model on test set"""
    model.eval()
    with torch.no_grad():
        pred = model(data).argmax(dim=1)
        test_acc = (pred[test_mask] == data.y[test_mask]).float().mean()
        
        # Compute per-class accuracy
        unique_labels = data.y.unique()
        per_class_acc = {}
        for label in unique_labels:
            mask = (data.y[test_mask] == label)
            if mask.sum() > 0:
                acc = (pred[test_mask][mask] == label).float().mean()
                per_class_acc[label.item()] = acc.item()
    
    return test_acc.item(), per_class_acc

# Evaluate models
gcn_test_acc, gcn_per_class = evaluate_model(model, data, test_mask)
gat_test_acc, gat_per_class = evaluate_model(gat_model, data, test_mask)

print(f"GCN Test Accuracy: {gcn_test_acc:.4f}")
print(f"GAT Test Accuracy: {gat_test_acc:.4f}")
```

## Link Prediction with GNNs

### Link Prediction Model
```python
class LinkPredictionGNN(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(LinkPredictionGNN, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.conv2(x, edge_index)
        
        return x
    
    def decode(self, z, edge_index):
        """Decode node embeddings to edge probabilities"""
        row, col = edge_index
        return (z[row] * z[col]).sum(dim=-1)

def prepare_link_prediction_data(data, test_ratio=0.2):
    """Prepare data for link prediction task"""
    from torch_geometric.utils import negative_sampling, train_test_split_edges
    
    # Split edges into train/test
    data = train_test_split_edges(data, val_ratio=0.1, test_ratio=test_ratio)
    return data

# Prepare link prediction data
lp_data = prepare_link_prediction_data(data)
lp_model = LinkPredictionGNN(input_dim=2, hidden_dim=16)
```

## Graph-Level Tasks

### Graph Classification
```python
class GraphClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GraphClassifier, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.classifier = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        
        # Node-level representations
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.dropout(x)
        
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        
        # Graph-level representation (global mean pooling)
        from torch_geometric.nn import global_mean_pool
        x = global_mean_pool(x, batch)
        
        # Classification
        x = self.classifier(x)
        return F.log_softmax(x, dim=1)

# This would be used with a dataset of multiple graphs
# graph_classifier = GraphClassifier(input_dim=2, hidden_dim=32, output_dim=2)
```

## Visualization and Analysis

### Node Embedding Visualization
```python
def visualize_node_embeddings(model, data, title="Node Embeddings"):
    """Visualize learned node embeddings"""
    model.eval()
    with torch.no_grad():
        # Get embeddings from second-to-last layer
        x, edge_index = data.x, data.edge_index
        x = model.conv1(x, edge_index)
        x = F.relu(x)
        embeddings = x.cpu().numpy()
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(embeddings[:, 0], embeddings[:, 1], 
                         c=data.y.cpu().numpy(), cmap='viridis', s=100, alpha=0.7)
    
    # Add node labels
    for i in range(len(embeddings)):
        plt.annotate(str(i), (embeddings[i, 0], embeddings[i, 1]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.colorbar(scatter)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    return embeddings

# Visualize GCN embeddings
gcn_embeddings = visualize_node_embeddings(model, data, "GCN Node Embeddings")
```

### Attention Visualization (for GAT)
```python
def visualize_attention_weights(gat_model, data):
    """Visualize attention weights from GAT model"""
    gat_model.eval()
    with torch.no_grad():
        x, edge_index = data.x, data.edge_index
        
        # Get attention weights from first layer
        out, attention_weights = gat_model.conv1(x, edge_index, return_attention_weights=True)
        
        # attention_weights is (edge_index, attention_values)
        edge_index_att, att_values = attention_weights
        
        # Visualize as network with edge widths proportional to attention
        import networkx as nx
        
        G = nx.Graph()
        G.add_nodes_from(range(data.num_nodes))
        
        # Add edges with attention weights
        for i, (src, dst) in enumerate(edge_index_att.t().cpu().numpy()):
            weight = att_values[i].mean().item()  # Average over attention heads
            G.add_edge(src, dst, weight=weight)
        
        # Plot
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=data.y.cpu().numpy(), 
                              cmap='viridis', node_size=300)
        
        # Draw edges with varying widths
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=[w*5 for w in weights], alpha=0.6)
        
        plt.title("GAT Attention Weights")
        plt.axis('off')
        
    return attention_weights

# Note: This requires modifications to the GAT model to return attention weights
```

## Performance Comparison
```python
def compare_gnn_architectures():
    """Compare different GNN architectures"""
    models = {
        'GCN': SimpleGCN(2, 16, 2),
        'GAT': SimpleGAT(2, 8, 2),
        'SAGE': SimpleGraphSAGE(2, 16, 2)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        losses, val_accs = train_node_classification(model, data, train_mask, val_mask, epochs=100)
        test_acc, per_class = evaluate_model(model, data, test_mask)
        
        results[name] = {
            'test_accuracy': test_acc,
            'per_class_accuracy': per_class,
            'final_loss': losses[-1]
        }
    
    # Display results
    print("\n" + "="*50)
    print("GNN Architecture Comparison")
    print("="*50)
    
    for name, metrics in results.items():
        print(f"{name:10s}: Test Acc = {metrics['test_accuracy']:.4f}")
    
    return results

comparison_results = compare_gnn_architectures()
```