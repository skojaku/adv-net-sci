# Preparation: Neural Networks and Deep Learning Prerequisites

## Required Knowledge from Previous Modules

Before studying Graph Neural Networks, ensure you understand:
- **From M01-M08**: Network representations, linear algebra, optimization, and embedding concepts
- **From M08**: Matrix decomposition techniques and dimensionality reduction principles

## Neural Network Fundamentals

### Basic Architecture Components

#### Perceptron and Multi-Layer Networks
- **Perceptron**: $y = \sigma(w^T x + b)$ where $\sigma$ is an activation function
- **Multi-layer**: Composition of linear transformations and nonlinear activations
- **Universal approximation**: Neural networks can approximate arbitrary functions

#### Activation Functions
Essential nonlinear functions:
- **ReLU**: $\text{ReLU}(x) = \max(0, x)$ - most common, helps with gradient flow
- **Sigmoid**: $\sigma(x) = \frac{1}{1 + e^{-x}}$ - outputs in (0,1) range
- **Tanh**: $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$ - outputs in (-1,1) range
- **Softmax**: $\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}$ - for probability distributions

### Forward and Backward Propagation

#### Forward Pass
Computing network output:
- **Layer computation**: $h^{(l+1)} = \sigma(W^{(l)} h^{(l)} + b^{(l)})$
- **Composition**: Output is function composition through all layers
- **Vectorization**: Efficient batch processing

#### Backpropagation
Computing gradients for optimization:
- **Chain rule**: $\frac{\partial L}{\partial W^{(l)}} = \frac{\partial L}{\partial h^{(l+1)}} \frac{\partial h^{(l+1)}}{\partial W^{(l)}}$
- **Gradient flow**: How gradients propagate backward through layers
- **Vanishing gradients**: Challenge in deep networks

## Optimization for Neural Networks

### Loss Functions
Different objectives for different tasks:
- **Mean Squared Error**: $\text{MSE} = \frac{1}{n}\sum_i (y_i - \hat{y}_i)^2$ for regression
- **Cross-entropy**: $\text{CE} = -\sum_i y_i \log(\hat{y}_i)$ for classification
- **Custom losses**: Task-specific objectives for graph problems

### Gradient-Based Optimization
Advanced optimization techniques:
- **SGD with momentum**: $v_t = \gamma v_{t-1} + \alpha \nabla_\theta L$
- **Adam optimizer**: Adaptive learning rates with momentum
- **Learning rate scheduling**: Decreasing rates over time
- **Batch normalization**: Normalizing layer inputs for stable training

### Regularization Techniques
Preventing overfitting:
- **L1/L2 regularization**: Adding penalty terms to loss function
- **Dropout**: Randomly setting some neurons to zero during training
- **Early stopping**: Stopping training when validation loss stops improving

## Representation Learning

### Feature Learning vs. Feature Engineering
- **Manual features**: Hand-crafted features based on domain knowledge
- **Learned features**: Features discovered automatically by neural networks
- **End-to-end learning**: Learning features jointly with final task

### Embedding Spaces
Understanding learned representations:
- **Distributed representations**: Dense vectors vs. one-hot encodings
- **Semantic similarity**: Similar inputs have similar representations
- **Linear relationships**: Arithmetic in embedding space (e.g., king - man + woman ≈ queen)

## Convolutional Neural Networks (CNNs)

### Convolution Operation
Foundation for understanding graph convolutions:
- **Local connectivity**: Neurons connect to local regions of input
- **Parameter sharing**: Same filters applied across different positions
- **Translation invariance**: Feature detection regardless of position

### Pooling Operations
Dimensionality reduction and invariance:
- **Max pooling**: Taking maximum value in local regions
- **Average pooling**: Taking average value in local regions
- **Global pooling**: Reducing to single value per feature map

## Attention Mechanisms

### Basic Attention
Computing weighted combinations:
- **Query-key-value**: $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$
- **Self-attention**: When queries, keys, and values come from same source
- **Multi-head attention**: Multiple attention mechanisms in parallel

### Applications to Graphs
- **Node attention**: Weighting importance of different neighbors
- **Graph-level attention**: Weighting importance of different nodes
- **Dynamic weights**: Learned attention weights vs. fixed graph structure

## Deep Learning for Irregular Data

### Challenges with Graph Data
- **Variable size**: Graphs have different numbers of nodes and edges
- **No natural ordering**: Nodes don't have canonical ordering like pixels
- **Irregular structure**: Unlike grids or sequences

### Permutation Invariance
Essential property for graph neural networks:
- **Node permutation**: Network output shouldn't change if nodes are reordered
- **Symmetric functions**: Functions that respect permutation invariance
- **Aggregation operations**: Sum, max, mean preserve invariance

These deep learning foundations provide the necessary background for understanding how Graph Neural Networks adapt neural network concepts to work with the irregular structure of graphs and networks.