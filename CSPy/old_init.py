import juliacall
jl = juliacall.Main
jl.seval("import Pkg")

def _load_julia_package(name="CaratheodoryPruning"):
    try:
        jl.seval("using {0}".format(name))
    except:
        jl.seval("Pkg.add(\"{0}\")".format(name))
        jl.seval("using {0}".format(name))
    return jl.seval("{0}".format(name))

csp = _load_julia_package("CaratheodoryPruning")
import numpy as np

def caratheodory_pruning(V, w_in, progress=False):
    w, inds, err = csp.caratheodory_pruning(V, w_in, progress=progress)
    # Account for 1-indexing
    w = np.array([w[i-1] for i in inds])
    inds = inds.to_numpy() - 1
    return w, inds, err

juliavecfun = jl.seval("pyfun -> (i-> pyconvert(Float64, pyfun(i-1)))")
juliavanderfun = jl.seval("pyfun -> (i-> pyconvert(VandermondeVector, pyfun(i-1)))")

def on_demand_matrix(N, M, vecfun, by="cols", vandermonde=False):
    # Pass vecfun into julia
    if vandermonde:
        jlfun = juliavanderfun(vecfun)
    else:
        jlfun = juliavecfun(vecfun)
    by = jl.Symbol(by)
    return csp.OnDemandMatrix(N, M, jlfun, by=by, T=jl.seval("Float64"))

def on_demand_vector(M, elemfun):
    # Pass vecfun into julia
    jlfun = juliavecfun(elemfun)
    return csp.OnDemandVector(M, jlfun)

def vandermonde_vector(vec, pt):
    return csp.VandermondeVector(jl.Array(vec), jl.Array(pt))