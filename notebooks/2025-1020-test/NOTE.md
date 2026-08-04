# Hyperbolic Word2Vec Implementation

## Concept Overview

This project implements a Word2Vec-style embedding model that projects words into a hyperbolic space instead of the traditional Euclidean space. The motivation for using hyperbolic geometry is that it naturally captures hierarchical structures in data, which are common in language (e.g., taxonomies, semantic hierarchies).

## Architecture

### Traditional Word2Vec
- Input layer: One-hot encoded word vectors
- Hidden layer: Dense embedding layer (e.g., 100-300 dimensions)
- Output layer: Softmax over vocabulary (Skip-gram) or context prediction (CBOW)
- Geometry: Euclidean space

### Hyperbolic Word2Vec (This Implementation)
- **Input layer**: One-hot encoded word vectors (vocabulary size)
- **Embedding layer**: Projects to Euclidean intermediate representation
- **Hyperbolic projection layer**: Maps to 2-3D hyperbolic space (hyperboloid model)
- **Geometry**: Poincaré ball or hyperboloid model of hyperbolic geometry
- **Distance metric**: Hyperbolic distance instead of Euclidean

## Why Hyperbolic Space?

1. **Hierarchical structure**: Hyperbolic space expands exponentially, allowing it to embed tree-like hierarchies with low distortion
2. **Efficient representation**: Can represent hierarchical relationships in lower dimensions (2-3D) compared to Euclidean space
3. **Linguistic structure**: Language has inherent hierarchical structure (hypernymy, meronymy, etc.)

## Mathematical Framework

### Hyperboloid Model
The hyperboloid model represents hyperbolic space as:
```
H^n = {x ∈ R^{n+1} : ⟨x, x⟩_L = -1, x_0 > 0}
```
where ⟨·,·⟩_L is the Minkowski inner product.

### Distance Metric
The hyperbolic distance between two points x, y on the hyperboloid:
```
d_H(x, y) = arcosh(-⟨x, y⟩_L)
```

### Geoopt Library
We use `geoopt` (Riemannian Optimization in PyTorch) which provides:
- Manifold-aware optimizers
- Hyperbolic layers and operations
- Proper gradient computation on manifolds

## Implementation Details

### Model Architecture

1. **Input Layer**: Word indices (vocabulary size V)
2. **Euclidean Embedding**: Linear layer mapping to intermediate dimension (e.g., 50-100D)
3. **Hyperbolic Projection**: Custom layer using geoopt that:
   - Projects to 2-3D hyperbolic space
   - Uses exponential map to map from tangent space to hyperboloid
   - Maintains points on the manifold during optimization
4. **Output**: Hyperbolic embeddings (2-3D per word)

### Training Objective

We'll use the Skip-gram objective modified for hyperbolic space:
- **Positive pairs**: (target word, context word) should be close in hyperbolic space
- **Negative sampling**: Sample random words that should be far from target
- **Loss function**: Based on hyperbolic distance rather than dot product

### Dataset: Les Misérables

We'll use the text of "Les Misérables" by Victor Hugo as our training corpus:
- Rich vocabulary and hierarchical structure (characters, locations, themes)
- Public domain text available from Project Gutenberg
- Sufficient length for meaningful word embeddings
- Interesting semantic relationships to visualize in 2D/3D

## Project Structure

```
hyperbolic-word2vec/
├── data/
│   └── raw/              # Raw text files (Les Misérables)
├── src/
│   ├── model.py          # Hyperbolic Word2Vec model
│   ├── data.py           # Data loading and preprocessing
│   ├── train.py          # Training script
│   └── utils.py          # Utility functions
├── tests/
│   └── test_model.py     # Unit tests
├── examples/
│   └── demo.py           # Example usage and visualization
├── Snakefile             # Snakemake workflow
├── requirements.txt      # Python dependencies
└── note.md              # This file
```

## Dependencies

- **PyTorch**: Deep learning framework
- **geoopt**: Riemannian optimization and hyperbolic geometry
- **numpy**: Numerical computing
- **matplotlib/plotly**: Visualization of 2D/3D embeddings
- **nltk**: Text preprocessing
- **snakemake**: Workflow management

## Usage Workflow

1. **Data preparation**: Download and preprocess Les Misérables text
2. **Training**: Train hyperbolic Word2Vec model (2-3D embeddings)
3. **Evaluation**: Analyze learned embeddings and hierarchical structure
4. **Visualization**: Plot word embeddings in hyperbolic space

## Expected Outcomes

- 2D or 3D visualization of word embeddings in hyperbolic space
- Clear hierarchical clustering (characters, places, themes)
- Demonstration that hyperbolic geometry can capture semantic relationships efficiently
- Comparison with Euclidean Word2Vec in same dimensionality

## References

- Nickel & Kiela (2017): "Poincaré Embeddings for Learning Hierarchical Representations"
- Tifrea et al. (2019): "Poincaré GloVe: Hyperbolic Word Embeddings"
- Mikolov et al. (2013): "Efficient Estimation of Word Representations in Vector Space" (original Word2Vec)
- Kochurov et al. (2020): "Geoopt: Riemannian Optimization in PyTorch"

## Notes

- Starting with 2D embeddings for easy visualization, can extend to 3D
- Using hyperboloid model (via geoopt) for numerical stability
- Skip-gram architecture chosen for better performance on smaller corpora
- Negative sampling for computational efficiency
