# CSPy: Python API for CaratheodoryPruning.jl

For documentation of Julia package and methods, see the [docs](https://fbelik.github.io/CaratheodoryPruning.jl/dev/).

## Install from GitHub

```bash
pip install "git+https://github.com/fbelik/CSPy.git"
```

This API provides the following methods that interface the Julia package using the interface [juliacall](https://juliapy.github.io/PythonCall.jl/dev/juliacall/). The goal is to allow the user to pass in `np.array` which will be converted to Julia array types and python functions which are converted to Julia functions.

- `caratheodory_pruning(V, w_in, progress=False)` interfaces to the Julia method `caratheodory_pruning(V, w_in, progress=false)` and performs pruning with respect to the `MxN` Vandermonde matrix `V` and the `M`-vector of weights, `w_in`. Slightly different than the Julia code, returns a 3-tuple, `w`, `inds`, and `err` such that `w` is a `len(inds)` numpy array with the pruned, nonzero, weights, `inds` corresponds to the indices chosen, and `err` is the error in pruning.
- `on_demand_matrix(N, M, vecfun, by="cols", vandermonde=False)` interfaces to the Julia method `OnDemandMatrix(N, M, vecfun, by=:cols)`. The additional flag `vandermonde` is required if the entries of the on-demand matrix are stored as `VandermondeVector`'s.
- `on_demand_vector(M, elemfun)` interfaces to the Julia method `OnDemandVector(N, M, elemfun)`.
- `vandermonde_vector(vec, pt)` interfaces to the Julia method `VandermondeVector(vec, pt)`; assumes that both `vec` and `pt` can be converted to Julia vector types.

In order to interface with Julia methods properly, it defines methods for converting between Python and Julia functions:
- `juliavecfun(pyfun)` converts a function in Python, `pyfun(i)` to a Julia function by reindexing and calling `pyconvert` with `pyfun -> (i-> pyconvert(Float64, pyfun(i-1)))`
- `juliavanderfun(pyfun)` converts a function in Python, `pyfun(i)` to a Julia function by reindexing and calling `pyconvert` with `pyfun -> (i-> pyconvert(VandermondeVector, pyfun(i-1)))`

For now, all types are converted to `Float64` in Julia, so underlying Python arrays should not be complex valued. 

## Initialization behavior

`import CSPy` is now side-effect free and does not install Julia packages automatically.
If `CaratheodoryPruning` is not available in your Julia environment, call:

```python
import CSPy
CSPy.initialize(auto_install=True)
```

You can also enable this once via environment variable:

```bash
export CSPY_AUTO_INSTALL_JULIA=1
```
