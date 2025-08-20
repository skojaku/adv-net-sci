# Module 09: Graph Neural Networks - Core Concepts

## What are Graph Neural Networks?

**Graph Neural Networks (GNNs)** are deep learning models designed to work directly with graph-structured data. Unlike traditional neural networks that process regular grids (images) or sequences (text), GNNs handle irregular network structures.

**Key innovation**: Message passing between connected nodes to learn representations that capture both node features and graph topology.

## From Images to Graphs: The Conceptual Bridge

### Traditional CNNs (Convolutional Neural Networks)
- **Regular structure**: Fixed grid (pixels)
- **Local connectivity**: 3×3 or 5×5 kernels
- **Translation invariance**: Same operation everywhere
- **Pooling**: Downsample spatial dimensions

### Graph Convolution Challenge
- **Irregular structure**: Varying node degrees, no spatial ordering
- **Variable neighborhoods**: Different number of neighbors per node
- **No natural ordering**: Nodes don't have canonical positions
- **Permutation invariance**: Output shouldn't depend on node ordering

## Core GNN Concepts

### Message Passing Framework
**Basic idea**: Nodes aggregate information from neighbors to update their representations.

**General steps**:
1. **Message**: Compute messages between connected nodes
2. **Aggregate**: Combine messages from all neighbors  
3. **Update**: Update node representation using aggregated message

### Mathematical Formulation
```
h_v^(l+1) = UPDATE(h_v^(l), AGGREGATE({MESSAGE(h_v^(l), h_u^(l)) : u ∈ N(v)}))
```

Where:
- h_v^(l) = representation of node v at layer l
- N(v) = neighbors of node v
- MESSAGE, AGGREGATE, UPDATE = learnable functions

## Major GNN Architectures

### Graph Convolutional Networks (GCN)
**Simple and effective**: Localized first-order approximation of spectral convolution.

**Layer update**:
```
H^(l+1) = σ(Ã H^(l) W^(l))
```

Where:
- Ã = normalized adjacency matrix with self-loops
- H^(l) = node features at layer l
- W^(l) = learnable weight matrix
- σ = activation function

### GraphSAGE (Sample and Aggregate)
**Inductive learning**: Can handle previously unseen nodes.

**Key features**:
- Sample fixed-size neighborhood
- Various aggregation functions (mean, LSTM, pooling)
- Scalable to large graphs

### Graph Attention Networks (GAT)
**Attention mechanism**: Learns importance weights for neighbors.

**Attention weights**:
```
α_ij = softmax(LeakyReLU(a^T [W h_i || W h_j]))
```

**Benefits**:
- Different importance for different neighbors
- Better handling of heterogeneous neighborhoods
- Interpretable attention weights

### Graph Transformer
**Self-attention on graphs**: Adapts Transformer architecture to graphs.

**Challenges addressed**:
- How to incorporate edge information
- Positional encodings for graphs
- Scalability to large graphs

## Types of GNN Tasks

### Node-Level Tasks
**Node classification**: Predict labels for individual nodes
- **Applications**: User classification, protein function prediction
- **Examples**: Classifying research papers by topic, identifying fraudulent accounts

**Node regression**: Predict continuous values for nodes
- **Applications**: Property prediction, node importance scoring

### Edge-Level Tasks
**Link prediction**: Predict missing or future edges
- **Applications**: Friend recommendation, drug-target interaction
- **Approaches**: Node pair scoring, edge classification

**Edge classification**: Classify relationship types
- **Applications**: Relation extraction, interaction type prediction

### Graph-Level Tasks
**Graph classification**: Predict labels for entire graphs
- **Applications**: Molecular property prediction, social network analysis
- **Challenges**: How to create graph-level representations

**Graph regression**: Predict continuous values for graphs
- **Applications**: Chemical compound properties, network statistics

## Key Technical Components

### Neighborhood Aggregation
**Mean aggregation**: Simple average of neighbor features
**Sum aggregation**: Summation (preserves multiset information)
**Max pooling**: Element-wise maximum
**LSTM aggregation**: Sequential processing of neighbors
**Attention-based**: Weighted combination based on learned attention

### Pooling Operations
**Global pooling**: Graph-level representation from all nodes
**Hierarchical pooling**: Multi-resolution graph representations
**Coarsening approaches**: Progressively merge similar nodes

### Skip Connections and Residuals
**Over-smoothing problem**: Deep GNNs may make all nodes similar
**Solutions**: Skip connections, residual connections, dropout

### Normalization Techniques
**BatchNorm**: Normalize across batch dimension
**LayerNorm**: Normalize across feature dimension  
**GraphNorm**: Graph-specific normalization approaches

## Training and Optimization

### Mini-batch Training
**Full-batch**: Use entire graph (memory intensive)
**Node sampling**: Sample subgraphs for each mini-batch
**Layer sampling**: Sample different neighborhoods per layer
**Subgraph sampling**: Work with graph partitions

### Loss Functions
**Supervised tasks**: Cross-entropy, MSE, ranking losses
**Unsupervised tasks**: Reconstruction, contrastive learning
**Graph-level**: Aggregate node predictions appropriately

### Evaluation Metrics
**Node tasks**: Accuracy, F1-score, AUC
**Edge tasks**: Precision, recall, ranking metrics
**Graph tasks**: Graph-level accuracy, molecular property prediction metrics

## Applications Across Domains

### Social Networks
**User behavior prediction**: Predicting user actions, preferences
**Community detection**: Finding groups and communities
**Influence propagation**: Modeling information spread
**Content recommendation**: Personalized content delivery

### Biological Networks
**Drug discovery**: Predicting drug-target interactions
**Protein folding**: Structural property prediction
**Disease analysis**: Gene-disease association prediction
**Metabolic networks**: Pathway analysis and prediction

### Chemical Informatics
**Molecular property prediction**: Solubility, toxicity, activity
**Drug design**: Generating molecules with desired properties
**Chemical reaction prediction**: Reaction outcome and mechanism
**Materials science**: Crystal property prediction

### Knowledge Graphs
**Knowledge completion**: Predicting missing facts
**Question answering**: Reasoning over structured knowledge
**Semantic search**: Finding related entities and concepts
**Recommendation**: Using knowledge for better recommendations

### Computer Networks
**Network security**: Intrusion detection, anomaly identification
**Traffic optimization**: Routing and load balancing
**Performance prediction**: Network throughput and latency
**Failure detection**: Identifying network problems

## Challenges and Future Directions

### Scalability Issues
**Memory complexity**: Storing large graph structures
**Computational complexity**: Message passing over large neighborhoods
**Distributed training**: Parallel processing across multiple machines

### Theoretical Understanding
**Expressive power**: What can GNNs represent?
**Generalization**: How do GNNs generalize to new graphs?
**Optimization**: Why do GNNs train successfully?

### Dynamic and Temporal Graphs
**Evolving networks**: Handling time-varying graph structure
**Temporal dynamics**: Incorporating time information
**Online learning**: Updating models with streaming graph data

### Robustness and Fairness
**Adversarial attacks**: Robustness to malicious modifications
**Fairness**: Ensuring equitable predictions across groups
**Privacy**: Protecting sensitive information in graph data

### Integration with Other Methods
**Hybrid approaches**: Combining GNNs with other deep learning models
**Multi-modal learning**: Graphs with additional data types
**Transfer learning**: Applying pre-trained GNNs to new domains