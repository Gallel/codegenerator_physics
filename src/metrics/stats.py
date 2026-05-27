"""Small statistics helpers shared by the tables and plots modules.

Kept dependency-free (stdlib only) so it runs anywhere the rest of the
pipeline runs. The corpus is small (27 problems, 5 samples each), so reporting
uncertainty honestly matters more than usual.
"""
import math


def wilson_interval(successes, n, z=1.96):
    """Wilson score interval for a binomial proportion (95% by default).

    Better than the normal approximation for small n and proportions near 0/1,
    which is exactly our regime (n=27, rates often near 1.0). Returns
    (low, high); for n == 0 returns (0.0, 0.0).
    """
    if n == 0:
        return 0.0, 0.0
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return max(0.0, center - half), min(1.0, center + half)


def mean_ci(values, z=1.96):
    """Mean and a normal-approx 95% CI half-width for a list of numbers.

    Returns (mean, half_width, n). half_width is None when n < 2 (no spread to
    estimate). Used for continuous metrics (CodeBLEU, LCS, CAS) where we report
    the mean across problems.
    """
    vals = [v for v in values if v is not None]
    n = len(vals)
    if n == 0:
        return None, None, 0
    mean = sum(vals) / n
    if n < 2:
        return mean, None, n
    var = sum((v - mean) ** 2 for v in vals) / (n - 1)
    se = math.sqrt(var / n)
    return mean, z * se, n


def spearman(xs, ys):
    """Spearman rank correlation rho between two equal-length sequences.

    We use Spearman (not Pearson) for the Pass@1 vs CodeBLEU scatter because
    Pass@1 is heavily discretized (multiples of 1/n), which violates Pearson's
    assumptions. Returns (rho, n); rho is None if fewer than 3 paired points.
    Ties are handled with average ranks. p-value is intentionally omitted (with
    n<=27 we report rho descriptively and say so in the text).
    """
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 3:
        return None, n

    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0  # average rank, 1-based
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx = ranks([p[0] for p in pairs])
    ry = ranks([p[1] for p in pairs])
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    deny = math.sqrt(sum((b - my) ** 2 for b in ry))
    if denx == 0 or deny == 0:
        return None, n
    return num / (denx * deny), n
