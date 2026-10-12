import numpy as np

INF = float("inf")
KINDS = ("ОБЫЧ", "БИН", "ТРОП")

def prepare(A, kind, zero_diag=False):
    A = np.asarray(A)
    if kind == "ОБЫЧ":
        return A.astype(np.int64)
    if kind == "БИН":
        return (A != 0)
    C = np.where(A != 0, A, INF).astype(float)
    if zero_diag:
        np.fill_diagonal(C, 0.0)
    return C

def identity(n, kind):
    if kind == "ОБЫЧ":
        return np.eye(n, dtype=np.int64)
    if kind == "БИН":
        return np.eye(n, dtype=bool)
    E = np.full((n, n), INF)
    return E

def mul_naive(A, B, kind):
    n = len(A)
    if kind == "ТРОП":
        C = [[INF] * n for _ in range(n)]
    else:
        C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if kind == "ОБЫЧ":
                    C[i][j] = C[i][j] + A[i][k] * B[k][j]
                elif kind == "БИН":
                    C[i][j] = C[i][j] or (A[i][k] + B[k][j])
                else:
                    C[i][j] = min(C[i][j], A[i][k] + B[k, j])
    return np.array(C, dtype={"ОБЫЧ": np.int64, "БИН": bool, "ТРОП": float}[kind])

def mul_fast(A, B, kind):
    if kind == "ОБЫЧ":
        return A @ B
    if kind == "БИН":
        return(A.astype(np.float32) @ B.astype(np.float32)) > 0
    n = A.shape[0]
    C = np.full((n, n), INF)
    for k in range(n):
        np.minimum(C, A[:, k:k + 1] + B[k:k + 1, :], out=C)
    return C

def power_linear(A, p, kind, mul=mul_fast):
    C = A
    R = identity(len(A), kind)
    while p > 0:
        R = mul(R, C, kind)
        p -= 1
    return R

def power_binary(A, p, kind, mul=mul_fast):
    C = A
    R = identity(len(A), kind)
    while p > 0:
        if p % 2 == 1:
            R = mul(R, C, kind)
        p //= 2
        if p > 0:
            C = mul(C, C, kind)
    return R
