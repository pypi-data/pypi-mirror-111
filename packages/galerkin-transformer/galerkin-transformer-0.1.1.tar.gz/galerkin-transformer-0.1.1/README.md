# Fourier Transformer and Galerkin Transformer: Attention without softmax
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Pytorch 1.8](https://img.shields.io/badge/pytorch-1.9-blue.svg)](https://pytorch.org/)
[![arXiv](https://img.shields.io/badge/arXiv-2105.14995-b31b1b.svg)](https://arxiv.org/abs/2105.14995)

# Introduction
The new attention operator is `(QK^T)V` or `Q(K^TV)`, whichever doing matmul gets the layer normalization, i.e., `Q, K` get layer normalized in the local attention, as for `K, V` in the global attention. No softmax, no layer normalization is applied afterward. This is called a scale-preserving simple attention. The feature extractor is a simple FFN or an interpolation-based CNN, the decoder is the spectral convolution re-implemented using only real parameters from the best operator learner to-date Fourier Neural Operator (FNO) in [*Li et al 2020*](https://github.com/zongyi-li/fourier_neural_operator) if the target is smooth, or just a pointwise FFN if otherwise. The resulting network is extremely powerful in learning PDE-related operators (energy decay, inverse coefficient identification).


Even though everyone is transformer'ing, the mathematics behind the attention mechanism is not well understood. We have also shown that the Galerkin-type attention (just a linear attention with softmax removed) is nothing but having an approximation capacity on par with a Petrov-Galerkin projection under a Hilbertian setup. We use a method commonly known as ''mixed method'' in the finite element analysis community that is used to solve fluid/electromagnetics problems. Unlike finite element methods, in an attention-based operator learner the approximation is not discretization-tied, in that:
1. the dimensions of the approximation spaces are not tied to the geometry as in the traditional finite element analysis (or finite difference, spectral methods, radial basis, etc);
2. the approximation spaces are being dynamically updated by the nonlinear universal approximator due to the presence of the positional encodings in the latent representations.

For details please refer to: [https://arxiv.org/abs/2105.14995](https://arxiv.org/abs/2105.14995)
```bibtex
@Misc{Cao:2021transformer,
  author        = {Shuhao Cao},
  title         = {Choose a Transformer: Fourier or Galerkin},
  year          = {2021},
  archiveprefix = {arXiv},
  eprint        = {2105.14995},
  primaryclass  = {cs.CL},
  url           = {https://arxiv.org/abs/2105.14995},
}
```
