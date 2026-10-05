"""python3 scripts/verify_dcsbm.py   (standard library only)

Checks every number and identity of the degree-corrected SBM slides (S33 to S38), against src/data/data.ts:
- the degrees of the karate club and of the random network of S06, S07 (S34),
- the maximum-likelihood estimates and the likelihood as a function of c alone, on the 8-node network (S36, S37),
- the identity log L(c) = m * I(c) + const, with I(c) the mutual information of the groups at the two ends of an edge.
"""
import itertools
import math
import re

data = open('src/data/data.ts').read()


def arr(name):
    m = re.search(rf'export const {name} = (\[.*?\]) as const;', data, re.S)
    return eval(m.group(1))


# ---- S34: degrees
def degrees(edges, n):
    d = [0] * n
    for a, b in edges:
        d[a] += 1
        d[b] += 1
    return d


K_DEG = degrees(arr('KARATE_EDGES'), 34)
N_DEG = degrees(arr('NOISE_EDGES'), 34)
assert len(arr('KARATE_EDGES')) == 78 and len(arr('NOISE_EDGES')) == 78
print('karate degrees', sorted(K_DEG, reverse=True)[:6], 'min', min(K_DEG), 'max', max(K_DEG))
print('random degrees', sorted(N_DEG, reverse=True)[:6], 'min', min(N_DEG), 'max', max(N_DEG))

# ---- the 8-node network of S23 to S31
U = arr('SBM_U')
GROUP = [0, 0, 0, 0, 1, 1, 1, 1]
pairs = [(a, b) for a in range(8) for b in range(a + 1, 8)]
edges = [(a, b) for k, (a, b) in enumerate(pairs) if U[k] < (0.9 if GROUP[a] == GROUP[b] else 0.1)]
assert len(edges) == 12
k = degrees(edges, 8)
m = len(edges)


def blocks(c, K):
    M = [[0] * K for _ in range(K)]  # M[r][s] = sum_ij A_ij [c_i = r][c_j = s]: an edge inside a group counts twice
    for a, b in edges:
        M[c[a]][c[b]] += 1
        M[c[b]][c[a]] += 1
    kap = [sum(M[r]) for r in range(K)]
    return M, kap


def dc_loglik_max(c, K):
    """The Poisson log-likelihood at its maximum over theta and omega, computed from the definition (constants dropped, as in
    Karrer and Newman: the factorials of the counts and the 2^(A_ii/2); here all counts are 0 or 1 and there are no self-edges)."""
    M, kap = blocks(c, K)
    theta = [k[i] / kap[c[i]] for i in range(8)]
    omega = [[M[r][s] for s in range(K)] for r in range(K)]
    ll = 0.0
    for i in range(8):
        for j in range(i, 8):
            mean = theta[i] * theta[j] * omega[c[i]][c[j]] * (0.5 if i == j else 1.0)
            a = 1 if (i, j) in edges else 0
            if a:
                ll += a * math.log(mean)
            ll -= mean
    return ll


def c_only(c, K):
    M, kap = blocks(c, K)
    s = sum(M[r][t] * math.log(M[r][t] / (kap[r] * kap[t])) for r in range(K) for t in range(K) if M[r][t] > 0)
    return s


def mutual_info(c, K):
    M, kap = blocks(c, K)
    tot = sum(kap)
    I = 0.0
    for r in range(K):
        for t in range(K):
            if M[r][t] > 0:
                p = M[r][t] / tot
                I += p * math.log(p / ((kap[r] / tot) * (kap[t] / tot)))
    return I


const = sum(x * math.log(x) for x in k) - m
checked = 0
for c in itertools.product([0, 1, 2], repeat=8):
    K = max(c) + 1
    M, kap = blocks(c, K)
    if min(kap) == 0:
        continue
    lhs = dc_loglik_max(c, K)
    rhs = 0.5 * c_only(c, K) + const  # log L(c) = 1/2 sum_rs m_rs log(m_rs / (kappa_r kappa_s)) + const
    assert abs(lhs - rhs) < 1e-9, (c, lhs, rhs)
    # log L(c) = m I(c) + const'
    assert abs(0.5 * c_only(c, K) - (m * mutual_info(c, K) - m * math.log(2 * m))) < 1e-9
    checked += 1
print('checked', checked, 'groupings: log L(c) = 1/2 sum m log(m/(kappa kappa)) + const = m I(c) + const')

M, kap = blocks(GROUP, 2)
print('degrees', k, 'kappa', kap, 'M', M, '2m', 2 * m)
assert M == [[10, 1], [1, 12]] and kap == [11, 13]
theta = [k[i] / kap[GROUP[i]] for i in range(8)]
print('theta-hat', [round(t, 3) for t in theta])
exp_seen = [[kap[r] * kap[t] / (2 * m) for t in range(2)] for r in range(2)]
print('seen', M, 'from degrees alone', [[round(x, 2) for x in row] for row in exp_seen])
print('I(true split) =', round(mutual_info(GROUP, 2), 4), ' log L(c) - const =', round(0.5 * c_only(GROUP, 2), 4))
best = max((c for c in itertools.product([0, 1], repeat=8) if 0 < sum(c) < 8), key=lambda c: c_only(c, 2))
print('best two-group split by the degree-corrected log L:', best, 'true split:', tuple(GROUP))
print('ok')
