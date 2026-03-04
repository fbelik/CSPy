import importlib
import os

import numpy as np

jl = None
_julia_ready = False
_csp = None
_juliavecfun = None
_juliavanderfun = None


def _get_jl():
    global jl
    if jl is None:
        jl = importlib.import_module("juliacall").Main
    return jl


def initialize(auto_install=None):
    """Initialize Julia bindings for CaratheodoryPruning.

    By default, the package does not auto-install Julia dependencies on import.
    Set `auto_install=True` (or CSPY_AUTO_INSTALL_JULIA=1) to allow installation.
    """
    global _julia_ready, _csp, _juliavecfun, _juliavanderfun

    if _julia_ready:
        return _csp

    if auto_install is None:
        auto_install = os.getenv("CSPY_AUTO_INSTALL_JULIA", "").lower() in {"1", "true", "yes"}

    _jl = _get_jl()
    _jl.seval("import Pkg")

    try:
        _jl.seval("using CaratheodoryPruning")
    except Exception as exc:
        if not auto_install:
            raise ImportError(
                "Julia package 'CaratheodoryPruning' is not available. "
                "Run CSPy.initialize(auto_install=True) once, or set "
                "CSPY_AUTO_INSTALL_JULIA=1 before import."
            ) from exc
        _jl.seval('Pkg.add("CaratheodoryPruning")')
        _jl.seval("using CaratheodoryPruning")

    _csp = _jl.seval("CaratheodoryPruning")
    _juliavecfun = _jl.seval("pyfun -> (i -> pyconvert(Float64, pyfun(i - 1)))")
    _juliavanderfun = _jl.seval(
        "pyfun -> (i -> pyconvert(CaratheodoryPruning.VandermondeVector, pyfun(i - 1)))"
    )
    _julia_ready = True
    return _csp


def _require_csp():
    return initialize()


def caratheodory_pruning(V, w_in, progress=False):
    csp = _require_csp()
    w, inds, err = csp.caratheodory_pruning(V, w_in, progress=progress)
    # Convert to Python indexing and compact weight vector.
    w = np.array([w[i - 1] for i in inds])
    inds = inds.to_numpy() - 1
    return w, inds, err


def on_demand_matrix(N, M, vecfun, by="cols", vandermonde=False):
    csp = _require_csp()
    if vandermonde:
        jlfun = _juliavanderfun(vecfun)
    else:
        jlfun = _juliavecfun(vecfun)
    _jl = _get_jl()
    by = _jl.Symbol(by)
    return csp.OnDemandMatrix(N, M, jlfun, by=by, T=_jl.seval("Float64"))


def on_demand_vector(M, elemfun):
    csp = _require_csp()
    jlfun = _juliavecfun(elemfun)
    return csp.OnDemandVector(M, jlfun)


def vandermonde_vector(vec, pt):
    csp = _require_csp()
    _jl = _get_jl()
    return csp.VandermondeVector(_jl.Array(vec), _jl.Array(pt))


__all__ = [
    "initialize",
    "caratheodory_pruning",
    "on_demand_matrix",
    "on_demand_vector",
    "vandermonde_vector",
]
