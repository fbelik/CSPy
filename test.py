import CSPy
import numpy as np

M = 100000              # Number of MC samples
p = 4                  # Maximal polynomial degree
N = int((p+1)*(p+2)/2) # Size of multi-index set (total-degree in 2D)

def vecfun(i):
    # Generate random point in unit circle
    pt = 2 * np.random.rand(2) - 1
    while sum(np.power(pt,2)) > 1:
        pt = 2 * np.random.rand(2) - 1
    # Evaluate basis on point
    vec = np.zeros(N)
    ct = 0
    for i in range(p+1):
        for j in range(p-i+1):
            vec[ct] = pt[0]**i + pt[1]**j
            ct += 1
    # Return vector storing the basis evaluation and point used
    return CSPy.vandermonde_vector(vec, pt)

# Vandermonde matrix
V = CSPy.on_demand_matrix(M, N, vecfun, by="rows", vandermonde=True)
# Input weight vector
wfun = lambda i: np.pi / M
w_in = CSPy.on_demand_vector(M, wfun)
# Pruning
w, inds, err = CSPy.caratheodory_pruning(V, w_in, progress=True)

# Evaluates the pruned quadrature rule on a function f(x)
def quadrule(f):
    res = 0.0
    for i in range(len(inds)):
        # Correct for python 0 indexing
        pt = V.vecs[inds[i]+1].pt
        wt = w[i]
        res += wt * f(pt)
    return res


approx = quadrule(lambda x: (x[0]**2 + x[1]**2))
exact = np.pi / 2
relerr = 100 * abs((approx - exact) / (exact))
print("Exact integration of f(x,y)=x^2+y^2 is pi/6 = {:.5f}".format(exact))
print("Approximate integration of f(x,y)=x^2+y^2 = {:.5f}".format(approx))
print("Relative error for f(x,y)=x^2+y^2 is {:.5f}%".format(relerr))

# Collect points used
xs = np.zeros(N)
ys = np.zeros(N)
for i in range(len(inds)):
    # Correct for python 0 indexing
    pt = V.vecs[inds[i]+1].pt
    xs[i] = pt[0]
    ys[i] = pt[1]

# Visualize the pruned rule
import matplotlib.pyplot as plt
plt.scatter(xs, ys, c=w)
plt.colorbar()
xplt = np.linspace(-1,1,101)
plt.plot(xplt, np.sqrt(1 - np.power(xplt,2)), color="black", linestyle="--")
plt.plot(xplt, -1 * np.sqrt(1 - np.power(xplt,2)), color="black", linestyle="--")
plt.show()