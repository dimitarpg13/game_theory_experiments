"""
Random Disclosure Parity Game — Minimax & Bellman Equation Analysis
===================================================================

GAME DEFINITION
───────────────
  Move 1 — Player I selects an integer from {1, 2}.
  Move 2 — The referee tosses a fair coin:
            Heads → Player II is INFORMED of Player I's choice.
            Tails → Player II receives NO information.
  Move 3 — Player II selects an integer from {3, 4}.
  Move 4 — The referee draws an integer from {1, 2, 3} with
            probabilities {0.4, 0.2, 0.4}.

  The sum of the numbers from moves 1, 3, and 4 is computed.
  If the sum is EVEN, Player II pays Player I $1.
  If the sum is ODD,  Player I pays Player II $1.

This is a finite, two-person, zero-sum game with IMPERFECT
INFORMATION (Player II may or may not know Player I's choice)
and CHANCE MOVES (coin toss and referee draw).

Unlike the Addition Game (perfect information), standard minimax
does NOT directly apply to the extensive form.  Instead we:
  • Use expectiminimax for the hypothetical perfect-info version
  • Convert to strategic (normal) form for the true imperfect-info game
  • Solve the resulting matrix game with pure and mixed strategies
  • Derive the analytical solution and the value of information

Run:  python random_disclosure_parity_game_demo.py
"""

from __future__ import annotations
import math
from itertools import product

# ═══════════════════════════════════════════════════════════════
#  PART 1: FORMAL BELLMAN / MINIMAX THEORY
# ═══════════════════════════════════════════════════════════════

SECTION_1 = """
═══════════════════════════════════════════════════════════════════
  PART 1: MINIMAX WITH CHANCE NODES AND IMPERFECT INFORMATION
═══════════════════════════════════════════════════════════════════

  THE EXTENSIVE FORM GAME TREE
  ────────────────────────────
  The game has four moves:

    Level 0 — Player I (MAX):  chooses i ∈ {1, 2}
    Level 1 — Referee (CHANCE): coin toss, P(Heads)=P(Tails)=½
    Level 2 — Player II (MIN):  chooses j ∈ {3, 4}
    Level 3 — Referee (CHANCE): draws r ∈ {1,2,3} with P={0.4,0.2,0.4}
    Terminal — Payoff = +1 if (i+j+r) even, −1 if odd

  INFORMATION SETS
  ────────────────
  Player II has THREE information sets:
    H₁: coin = Heads and PI chose 1  (PII knows i=1)
    H₂: coin = Heads and PI chose 2  (PII knows i=2)
    T:  coin = Tails                  (PII does NOT know i)

  The set T groups two nodes — one where PI chose 1, one where
  PI chose 2 — into a single information set.  PII must pick
  the SAME action at both nodes.

  WHY STANDARD MINIMAX FAILS
  ──────────────────────────
  Standard expectiminimax treats each decision node independently.
  In the perfect-info version, PII always sees i and can match
  parity.  But in the actual game, PII at information set T must
  choose BEFORE knowing i — an information-set constraint that
  tree search alone cannot capture.

  SOLUTION APPROACH
  ─────────────────
  1. Convert to STRATEGIC (normal) FORM:
     - Enumerate all pure strategies for each player
     - Compute expected payoff for every strategy pair
     - Obtain a 2 × 8 payoff matrix

  2. Solve the matrix game via MINIMAX:
     - Pure strategy maximin / minimax bounds
     - Mixed strategy equilibrium (minimax theorem)

  BELLMAN EQUATION WITH CHANCE NODES
  ──────────────────────────────────
  At a MAX node:   V = max_a  V(child_a)
  At a MIN node:   V = min_a  V(child_a)
  At a CHANCE node: V = Σ_ω  P(ω) · V(child_ω)

  These compose naturally in perfect-info games, but require
  the strategic-form detour when information sets are present.
"""


# ═══════════════════════════════════════════════════════════════
#  PART 2: GAME PARAMETERS AND PAYOFF LOGIC
# ═══════════════════════════════════════════════════════════════

PI_ACTIONS = (1, 2)
PII_ACTIONS = (3, 4)
REFEREE_OUTCOMES = ((1, 0.4), (2, 0.2), (3, 0.4))
COIN_PROB = 0.5


def parity_payoff(total: int) -> int:
    """Payoff to Player I: +1 if total is even, −1 if odd."""
    return 1 if total % 2 == 0 else -1


def conditional_payoff(i: int, j: int) -> float:
    """E[payoff to PI | PI chose i, PII chose j], averaged over referee."""
    return sum(p * parity_payoff(i + j + r) for r, p in REFEREE_OUTCOMES)


# ═══════════════════════════════════════════════════════════════
#  PART 3: EXPECTIMINIMAX — PERFECT INFORMATION VERSION
# ═══════════════════════════════════════════════════════════════

class TreeStats:
    def __init__(self):
        self.nodes = 0


def expectiminimax_perfect_info(stats: TreeStats) -> float:
    """
    Expectiminimax on the extensive form assuming perfect information:
    PII always knows PI's choice (even on tails).

    Returns the game value to Player I.
    """
    stats.nodes += 1  # root — PI decision (MAX)
    best_pi = -math.inf

    for i in PI_ACTIONS:
        # Coin toss — CHANCE node
        coin_val = 0.0
        for _, coin_prob in [("H", COIN_PROB), ("T", COIN_PROB)]:
            stats.nodes += 1
            # PII decision — MIN node (perfect info: sees i)
            best_pii = math.inf
            for j in PII_ACTIONS:
                stats.nodes += 1
                # Referee draw — CHANCE node / terminals
                ref_val = 0.0
                for r, p_r in REFEREE_OUTCOMES:
                    stats.nodes += 1
                    ref_val += p_r * parity_payoff(i + j + r)
                best_pii = min(best_pii, ref_val)
            coin_val += coin_prob * best_pii

        best_pi = max(best_pi, coin_val)
    return best_pi


def expectiminimax_perfect_info_ab(
    alpha: float, beta: float, stats: TreeStats
) -> float:
    """Expectiminimax with alpha-beta pruning (perfect info)."""
    stats.nodes += 1
    best_pi = -math.inf

    for i in PI_ACTIONS:
        coin_val = 0.0
        for _, coin_prob in [("H", COIN_PROB), ("T", COIN_PROB)]:
            stats.nodes += 1
            best_pii = math.inf
            for j in PII_ACTIONS:
                stats.nodes += 1
                ref_val = 0.0
                for r, p_r in REFEREE_OUTCOMES:
                    stats.nodes += 1
                    ref_val += p_r * parity_payoff(i + j + r)
                best_pii = min(best_pii, ref_val)
                if best_pii <= alpha:
                    break
            coin_val += coin_prob * best_pii

        best_pi = max(best_pi, coin_val)
        alpha = max(alpha, best_pi)
        if alpha >= beta:
            break
    return best_pi


# ═══════════════════════════════════════════════════════════════
#  PART 4: STRATEGIC FORM (NORMAL FORM) PAYOFF MATRIX
# ═══════════════════════════════════════════════════════════════

SECTION_4 = """
═══════════════════════════════════════════════════════════════════
  PART 4: STRATEGIC (NORMAL) FORM
═══════════════════════════════════════════════════════════════════

  PLAYER I's STRATEGIES
  ─────────────────────
  PI moves first with no prior info.  Strategies: {choose 1, choose 2}.

  PLAYER II's STRATEGIES
  ──────────────────────
  PII has 3 information sets (H₁, H₂, T), 2 actions each → 2³ = 8.
  A strategy is a triple (a_H₁, a_H₂, a_T) ∈ {3,4}³.

  PAYOFF COMPUTATION
  ──────────────────
  For PI choosing i and PII using (a, b, c):

    E[payoff] = ½ · g(i, j_heads) + ½ · g(i, c)

  where j_heads = a if i=1, b if i=2, and

    g(i, j) = E[payoff | i, j] = { −0.6 if i+j is even
                                   { +0.6 if i+j is odd

  THE PARITY STRUCTURE
  ────────────────────
  Player I wants i + j ODD  (different parities → payoff +0.6).
  Player II wants i + j EVEN (same parities     → payoff −0.6).

  When PII is INFORMED: PII can match parity → guaranteed g = −0.6.
  When PII is UNINFORMED: PII cannot see i and must guess.

  This is the core strategic tension of the game.
"""


def enumerate_pii_strategies() -> list[tuple[int, int, int]]:
    """All 8 pure strategies: (action_at_H1, action_at_H2, action_at_T)."""
    return list(product(PII_ACTIONS, PII_ACTIONS, PII_ACTIONS))


def compute_expected_payoff(pi_choice: int, pii_strat: tuple[int, int, int]) -> float:
    """Expected payoff to PI for a strategy pair, integrating over chance."""
    a_h1, a_h2, a_t = pii_strat
    j_heads = a_h1 if pi_choice == 1 else a_h2
    j_tails = a_t
    return COIN_PROB * conditional_payoff(pi_choice, j_heads) + \
           COIN_PROB * conditional_payoff(pi_choice, j_tails)


def build_payoff_matrix():
    """
    Build the 2×8 payoff matrix M[i][j].

    Returns (matrix, pi_strats, pii_strats).
    """
    pii_strats = enumerate_pii_strategies()
    matrix = []
    for i in PI_ACTIONS:
        row = [compute_expected_payoff(i, s) for s in pii_strats]
        matrix.append(row)
    return matrix, list(PI_ACTIONS), pii_strats


# ═══════════════════════════════════════════════════════════════
#  PART 5: MINIMAX ON THE MATRIX GAME
# ═══════════════════════════════════════════════════════════════

def minimax_pure(M: list[list[float]]):
    """
    Pure strategy maximin (PI) and minimax (PII) for a 2-row matrix.

    Returns (maximin_val, maximin_row, minimax_val, minimax_col).
    """
    n_rows, n_cols = len(M), len(M[0])

    row_mins = [min(M[i]) for i in range(n_rows)]
    maximin_row = max(range(n_rows), key=lambda r: row_mins[r])
    maximin_val = row_mins[maximin_row]

    col_maxs = [max(M[i][j] for i in range(n_rows)) for j in range(n_cols)]
    minimax_col = min(range(n_cols), key=lambda c: col_maxs[c])
    minimax_val = col_maxs[minimax_col]

    return maximin_val, maximin_row, minimax_val, minimax_col


def find_dominated(M: list[list[float]], pii_strats: list):
    """
    Find dominated PII strategies (PII is the minimizer).

    Strategy j dominates k if M[:,j] ≤ M[:,k] componentwise with
    at least one strict inequality (lower payoffs to PI = better for PII).

    Returns set of dominated column indices.
    """
    n_cols = len(M[0])
    dominated = set()
    for k in range(n_cols):
        for j in range(n_cols):
            if j == k:
                continue
            if (all(M[i][j] <= M[i][k] for i in range(len(M))) and
                    any(M[i][j] < M[i][k] for i in range(len(M)))):
                dominated.add(k)
                break
    return dominated


def solve_2xn_mixed(M: list[list[float]]):
    """
    Solve a 2×n zero-sum matrix game for optimal mixed strategies.

    For PI (2 rows): find p* = P(row 0) maximizing min_j E_j(p).
    For PII (n cols): find q* minimizing max_i (Mq)_i.

    By LP theory, PII's optimal strategy uses at most 2 columns.

    Returns (p_star, v_star, q_star).
    """
    n_cols = len(M[0])
    slopes = [M[0][j] - M[1][j] for j in range(n_cols)]
    intercepts = [M[1][j] for j in range(n_cols)]

    # --- PI's optimal p ---
    candidates = [0.0, 1.0]
    for j1 in range(n_cols):
        for j2 in range(j1 + 1, n_cols):
            denom = slopes[j1] - slopes[j2]
            if abs(denom) > 1e-12:
                p_int = (intercepts[j2] - intercepts[j1]) / denom
                if -1e-12 <= p_int <= 1 + 1e-12:
                    candidates.append(max(0.0, min(1.0, p_int)))

    best_p, best_v = 0.0, -math.inf
    for p in candidates:
        v = min(intercepts[j] + p * slopes[j] for j in range(n_cols))
        if v > best_v:
            best_v = v
            best_p = p

    # --- PII's optimal q (support ≤ 2 columns) ---
    best_q = [0.0] * n_cols
    best_v_pii = math.inf

    for j1 in range(n_cols):
        # Pure strategy j1
        v_cand = max(M[0][j1], M[1][j1])
        if v_cand < best_v_pii:
            best_v_pii = v_cand
            best_q = [0.0] * n_cols
            best_q[j1] = 1.0

        # Mix j1 with j2
        for j2 in range(j1 + 1, n_cols):
            d1 = M[0][j1] - M[1][j1]
            d2 = M[0][j2] - M[1][j2]
            denom = d2 - d1
            if abs(denom) < 1e-12:
                continue
            t = d2 / denom
            if -1e-12 <= t <= 1 + 1e-12:
                t = max(0.0, min(1.0, t))
                r0 = t * M[0][j1] + (1 - t) * M[0][j2]
                r1 = t * M[1][j1] + (1 - t) * M[1][j2]
                v_cand = max(r0, r1)
                if v_cand < best_v_pii:
                    best_v_pii = v_cand
                    best_q = [0.0] * n_cols
                    best_q[j1] = t
                    best_q[j2] = 1 - t

    return best_p, best_v, best_q


# ═══════════════════════════════════════════════════════════════
#  PART 6: ANALYTICAL SOLUTION & VALUE OF INFORMATION
# ═══════════════════════════════════════════════════════════════

SECTION_6 = """
═══════════════════════════════════════════════════════════════════
  PART 6: ANALYTICAL SOLUTION & VALUE OF INFORMATION
═══════════════════════════════════════════════════════════════════

  THE PARITY MATCHING INSIGHT
  ───────────────────────────
  The payoff g(i,j) depends ONLY on the parity of i + j:

    g(i,j) = −0.6  if i ≡ j (mod 2)   (same parity)
    g(i,j) = +0.6  if i ≢ j (mod 2)   (different parity)

  When INFORMED (heads), PII can always match parity:
    PI=1 → PII plays 3 (odd+odd = even ≡ 0 mod 2, g = −0.6)
    PI=2 → PII plays 4 (even+even = even,          g = −0.6)

  When UNINFORMED (tails), PII cannot see i and plays a fixed
  action or randomises.  The optimal uninformed strategy is to
  play 3 and 4 each with probability ½ — the same "matching
  pennies" logic.

  OPTIMAL BEHAVIORAL STRATEGY FOR PII
  ────────────────────────────────────
    At H₁: play 3  (match PI=1's parity)
    At H₂: play 4  (match PI=2's parity)
    At T:  play 3 with prob ½, 4 with prob ½  (randomise)

  GAME VALUE DERIVATION
  ─────────────────────
  Against this strategy, for any PI choice:

    E[payoff] = ½ · (−0.6)     [heads: PII matches parity]
              + ½ · ½ · (−0.6) [tails: PII guesses right]
              + ½ · ½ · (+0.6) [tails: PII guesses wrong]
              = ½ · (−0.6) + ½ · 0
              = −0.30

  PI is indifferent between choosing 1 or 2 → this is an equilibrium.

  VALUE OF INFORMATION
  ────────────────────
  The game value as a function of the disclosure probability p
  (probability of heads) is:

      v(p) = p · (−0.6) + (1−p) · 0 = −0.6p

  Three benchmarks:
    p = 0   (no disclosure):   v = 0.00   (fair game)
    p = 0.5 (fair coin):       v = −0.30  (PII has slight advantage)
    p = 1   (full disclosure):  v = −0.60  (PII exploits fully)

  The value of partial information is EXACTLY LINEAR in p.
"""


def analytical_game_value(heads_prob: float = 0.5) -> float:
    """Closed-form game value: v = −0.6 × P(heads)."""
    v = -0.6 * heads_prob
    return v if v != 0.0 else 0.0  # avoid −0.0


# ═══════════════════════════════════════════════════════════════
#  DEMOS
# ═══════════════════════════════════════════════════════════════

def demo_conditional_payoffs():
    """Show the (i, j) → g(i,j) parity structure."""
    print(f"\n{'═' * 65}")
    print(f"  CONDITIONAL PAYOFFS  g(i, j) = E[payoff | i, j]")
    print(f"{'═' * 65}")

    print(f"\n  {'i':>3} │ {'j':>3} │ {'i+j':>5} │ {'Parity':>8} │ {'g(i,j)':>8}")
    print(f"  {'─' * 3}──┼{'─' * 5}┼{'─' * 7}┼{'─' * 10}┼{'─' * 10}")
    for i in PI_ACTIONS:
        for j in PII_ACTIONS:
            s = i + j
            par = "even" if s % 2 == 0 else "odd"
            g = conditional_payoff(i, j)
            print(f"  {i:>3} │ {j:>3} │ {s:>5} │ {par:>8} │ {g:>+8.1f}")

    print(f"\n  Rule: g = −0.6 if i ≡ j (mod 2), else g = +0.6")
    print(f"  Player I wants DIFFERENT parities; Player II wants SAME.")


def demo_game_tree():
    """Display the extensive form game tree with values."""
    print(f"\n{'═' * 65}")
    print(f"  EXTENSIVE FORM GAME TREE")
    print(f"{'═' * 65}\n")

    for i in PI_ACTIONS:
        print(f"  PI picks {i} (MAX)")
        for coin, coin_label in [("Heads", "H"), ("Tails", "T")]:
            info_set = f"H{chr(0x2080 + i)}" if coin == "Heads" else "T"
            info_desc = f"knows PI={i}" if coin == "Heads" else "does NOT know PI's choice"
            print(f"  ├── Coin: {coin} (p=0.5)")
            print(f"  │   └── PII at {info_set} (MIN) — {info_desc}")

            for j in PII_ACTIONS:
                g = conditional_payoff(i, j)
                match = "★" if g < 0 else " "
                conn = "├" if j == PII_ACTIONS[0] else "└"
                print(f"  │       {conn}── PII picks {j}:  E[payoff] = {g:+.2f}  {match}")

                for r, p_r in REFEREE_OUTCOMES:
                    s = i + j + r
                    payoff = parity_payoff(s)
                    par = "even" if s % 2 == 0 else "odd "
                    last = r == REFEREE_OUTCOMES[-1][0]
                    pipe = " " if j == PII_ACTIONS[-1] else "│"
                    sub_conn = "└" if last else "├"
                    print(f"  │       {pipe}   {sub_conn}── r={r} (p={p_r}): "
                          f"{i}+{j}+{r}={s} ({par}) → {payoff:+d}")

            if coin == "Heads":
                # PII optimal at this info set
                g_vals = {j: conditional_payoff(i, j) for j in PII_ACTIONS}
                opt_j = min(g_vals, key=g_vals.get)
                print(f"  │   PII minimises → pick {opt_j}, E = {g_vals[opt_j]:+.2f}")
        print()


def demo_payoff_table():
    """Display the full 2×8 payoff matrix."""
    M, pi_strats, pii_strats = build_payoff_matrix()

    print(f"\n{'═' * 65}")
    print(f"  PAYOFF TABLE  (expected $ from PII to PI)")
    print(f"{'═' * 65}")
    print(f"\n  PII strategy = (action at H₁, action at H₂, action at T)\n")

    col_strs = [f"({a},{b},{c})" for a, b, c in pii_strats]
    print(f"  {'':>8} │ " + " │ ".join(f"{c:>7}" for c in col_strs) + " │")
    print(f"  {'─' * 8}─┼" + "─┼─".join('─' * 7 for _ in col_strs) + "─┤")

    for idx, i in enumerate(pi_strats):
        vals = [f"{M[idx][j]:+.1f}" for j in range(len(pii_strats))]
        print(f"  PI = {i}   │ " + " │ ".join(f"{v:>7}" for v in vals) + " │")

    print(f"\n  Positive values favour Player I; negative favour Player II.")
    return M, pii_strats


def demo_dominance_analysis(M, pii_strats):
    """Eliminate dominated strategies and show the reduced game."""
    print(f"\n{'═' * 65}")
    print(f"  DOMINATED STRATEGY ELIMINATION")
    print(f"{'═' * 65}")

    dominated = find_dominated(M, pii_strats)

    if dominated:
        print(f"\n  Dominated PII strategies (for the minimiser):")
        for idx in sorted(dominated):
            s = pii_strats[idx]
            # Find a dominator
            for j in range(len(pii_strats)):
                if j in dominated or j == idx:
                    continue
                if (all(M[i][j] <= M[i][idx] for i in range(len(M))) and
                        any(M[i][j] < M[i][idx] for i in range(len(M)))):
                    d = pii_strats[j]
                    pay_dom = [round(M[r][idx], 2) for r in range(len(M))]
                    pay_by = [round(M[r][j], 2) for r in range(len(M))]
                    print(f"    ({s[0]},{s[1]},{s[2]}) dominated by ({d[0]},{d[1]},{d[2]})  "
                          f"  payoffs: {pay_dom} ≥ {pay_by}")
                    break

    surviving = [j for j in range(len(pii_strats)) if j not in dominated]
    print(f"\n  Surviving (undominated) PII strategies: "
          f"{[pii_strats[j] for j in surviving]}")

    # Show reduced matrix
    M_red = [[M[i][j] for j in surviving] for i in range(len(M))]
    col_strs = [f"({pii_strats[j][0]},{pii_strats[j][1]},{pii_strats[j][2]})"
                for j in surviving]

    print(f"\n  Reduced payoff matrix:")
    print(f"  {'':>8} │ " + " │ ".join(f"{c:>7}" for c in col_strs) + " │")
    print(f"  {'─' * 8}─┼" + "─┼─".join('─' * 7 for _ in col_strs) + "─┤")
    for idx, i in enumerate(PI_ACTIONS):
        vals = [f"{M_red[idx][j]:+.1f}" for j in range(len(surviving))]
        print(f"  PI = {i}   │ " + " │ ".join(f"{v:>7}" for v in vals) + " │")

    return M_red, [pii_strats[j] for j in surviving]


def demo_comparison_methods():
    """Compare expectiminimax (perfect info) with strategic form minimax."""
    M, pi_strats, pii_strats = build_payoff_matrix()

    print(f"\n{'═' * 65}")
    print(f"  METHOD COMPARISON")
    print(f"{'═' * 65}")

    # 1. Expectiminimax — perfect info
    stats_mm = TreeStats()
    v_perf = expectiminimax_perfect_info(stats_mm)

    # 2. Expectiminimax with alpha-beta — perfect info
    stats_ab = TreeStats()
    v_perf_ab = expectiminimax_perfect_info_ab(-math.inf, math.inf, stats_ab)

    # 3. Strategic form — pure minimax
    maximin_v, _, minimax_v, _ = minimax_pure(M)

    # 4. Strategic form — mixed minimax
    p_star, v_mixed, q_star = solve_2xn_mixed(M)

    # 5. Analytical formula
    v_analytical = analytical_game_value(0.5)

    print(f"\n  Method                           │ {'Value':>7} │ {'Nodes':>7}")
    print(f"  ─────────────────────────────────┼{'─' * 9}┼{'─' * 9}")
    print(f"  Expectiminimax (perfect info)     │ {v_perf:>+7.2f} │ {stats_mm.nodes:>7}")
    print(f"  Expectiminimax + α-β (perf. info) │ {v_perf_ab:>+7.2f} │ {stats_ab.nodes:>7}")
    print(f"  Strategic form, pure maximin (PI)  │ {maximin_v:>+7.2f} │     n/a")
    print(f"  Strategic form, pure minimax (PII) │ {minimax_v:>+7.2f} │     n/a")
    print(f"  Strategic form, mixed minimax      │ {v_mixed:>+7.2f} │     n/a")
    print(f"  Analytical formula (−0.6 × 0.5)   │ {v_analytical:>+7.2f} │     n/a")

    print(f"\n  Perfect info value:   {v_perf:+.2f}  (PII always matches parity)")
    print(f"  Actual game value:    {v_mixed:+.2f}  (PII can only match on heads)")
    print(f"  Difference:           {v_mixed - v_perf:+.2f}  (value of PI's partial concealment)")

    if abs(maximin_v - minimax_v) > 1e-9:
        print(f"\n  Pure maximin ({maximin_v:+.2f}) ≠ pure minimax ({minimax_v:+.2f})")
        print(f"  → No pure strategy saddle point; mixed strategies required.")
    print(f"\n  Mixed equilibrium: PI plays 1 with prob {p_star:.2f}, "
          f"2 with prob {1 - p_star:.2f}")

    return v_mixed


def demo_mixed_equilibrium():
    """Show the full mixed strategy equilibrium and its interpretation."""
    M, pi_strats, pii_strats = build_payoff_matrix()
    p_star, v_star, q_star = solve_2xn_mixed(M)

    print(f"\n{'═' * 65}")
    print(f"  MIXED STRATEGY EQUILIBRIUM")
    print(f"{'═' * 65}")

    print(f"\n  Game value:  v* = {v_star:+.2f}")

    print(f"\n  ── Player I's optimal strategy ──")
    print(f"  PI is indifferent: any mix of 1 and 2 yields E = {v_star:+.2f}")
    print(f"  against PII's equilibrium strategy.")

    print(f"\n  ── Player II's optimal mixed strategy ──")
    active = [(j, q_star[j]) for j in range(len(q_star)) if q_star[j] > 1e-12]
    for j, q in active:
        s = pii_strats[j]
        print(f"    ({s[0]},{s[1]},{s[2]}) with probability {q:.2f}")

    # Behavioral strategy interpretation
    print(f"\n  ── Behavioral strategy interpretation ──")
    # Compute action probabilities at each information set
    p_h1 = {3: 0.0, 4: 0.0}
    p_h2 = {3: 0.0, 4: 0.0}
    p_t = {3: 0.0, 4: 0.0}
    for j, q in enumerate(q_star):
        if q < 1e-12:
            continue
        a, b, c = pii_strats[j]
        p_h1[a] += q
        p_h2[b] += q
        p_t[c] += q

    print(f"    At H₁ (knows PI=1): play 3 with prob {p_h1[3]:.2f}, "
          f"4 with prob {p_h1[4]:.2f}")
    print(f"    At H₂ (knows PI=2): play 3 with prob {p_h2[3]:.2f}, "
          f"4 with prob {p_h2[4]:.2f}")
    print(f"    At T  (uninformed):  play 3 with prob {p_t[3]:.2f}, "
          f"4 with prob {p_t[4]:.2f}")

    print(f"\n  In words:")
    print(f"    • When informed → MATCH PI's parity (play 3 if PI=1, 4 if PI=2)")
    print(f"    • When uninformed → RANDOMISE uniformly between 3 and 4")

    # Verify: payoff against each PI choice
    print(f"\n  ── Verification ──")
    for idx, i in enumerate(PI_ACTIONS):
        e_payoff = sum(q_star[j] * M[idx][j] for j in range(len(pii_strats)))
        print(f"    E[payoff | PI={i}] = {e_payoff:+.4f}")
    print(f"    → PI is indifferent (both give {v_star:+.2f}). ✓")


def demo_value_of_information():
    """Analyze game value as a function of disclosure probability."""
    print(f"\n{'═' * 65}")
    print(f"  VALUE OF INFORMATION ANALYSIS")
    print(f"{'═' * 65}")

    print(f"\n  Game value v(p) as a function of P(heads) = p:")
    print(f"\n  {'p':>6} │ {'v(p) analytical':>16} │ {'Interpretation':>30}")
    print(f"  {'─' * 6}──┼{'─' * 18}┼{'─' * 32}")

    for p_val in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        v = analytical_game_value(p_val)
        if p_val == 0.0:
            interp = "no disclosure → fair game"
        elif p_val == 0.5:
            interp = "fair coin (the actual game)"
        elif p_val == 1.0:
            interp = "full disclosure → PII exploits"
        else:
            interp = ""
        print(f"  {p_val:>6.1f} │ {v:>+16.2f} │ {interp:>30}")

    print(f"\n  Formula:  v(p) = −0.6 × p")
    print(f"\n  The value is EXACTLY LINEAR in the disclosure probability.")
    print(f"  Each 10% increase in disclosure costs Player I $0.06 per game.")

    print(f"\n  ── Three regimes ──")
    print(f"    p = 0:   No info  → v = 0.00  (matching pennies, fair)")
    print(f"    p = 0.5: Half info → v = −0.30 (PII has $0.30 edge)")
    print(f"    p = 1:   Full info → v = −0.60 (PII always wins $0.60)")


def demo_strategy_walkthrough():
    """Walk through key strategies showing expected payoffs."""
    print(f"\n{'═' * 65}")
    print(f"  STRATEGY WALKTHROUGH")
    print(f"{'═' * 65}")

    M, _, pii_strats = build_payoff_matrix()

    key_strats = [
        ((3, 3, 3), "always play 3"),
        ((3, 4, 3), "match when informed, play 3 when not"),
        ((3, 4, 4), "match when informed, play 4 when not"),
        ((4, 4, 4), "always play 4"),
    ]

    for strat, desc in key_strats:
        j = pii_strats.index(strat)
        print(f"\n  ── PII strategy ({strat[0]},{strat[1]},{strat[2]}): "
              f"{desc} ──")

        for idx, i in enumerate(PI_ACTIONS):
            a_h1, a_h2, a_t = strat
            j_heads = a_h1 if i == 1 else a_h2
            j_tails = a_t
            g_h = conditional_payoff(i, j_heads)
            g_t = conditional_payoff(i, j_tails)
            e = M[idx][j]
            print(f"    PI={i}: heads→PII plays {j_heads} (g={g_h:+.1f}), "
                  f"tails→PII plays {j_tails} (g={g_t:+.1f}), "
                  f"E = 0.5×{g_h:+.1f} + 0.5×{g_t:+.1f} = {e:+.2f}")

        worst = max(M[0][j], M[1][j])
        print(f"    PII's worst case: {worst:+.2f}")


def demo_game_simulation():
    """Simulate games under different strategy profiles."""
    import random
    random.seed(42)

    print(f"\n{'═' * 65}")
    print(f"  GAME SIMULATIONS")
    print(f"{'═' * 65}")

    def simulate_one(pi_choice, pii_strat, verbose=True):
        a_h1, a_h2, a_t = pii_strat
        coin = random.choice(["Heads", "Tails"])
        if coin == "Heads":
            j = a_h1 if pi_choice == 1 else a_h2
            info = f"PII informed, plays {j}"
        else:
            j = a_t
            info = f"PII uninformed, plays {j}"
        r_draw = random.random()
        if r_draw < 0.4:
            r = 1
        elif r_draw < 0.6:
            r = 2
        else:
            r = 3
        s = pi_choice + j + r
        payoff = parity_payoff(s)
        if verbose:
            par = "even" if s % 2 == 0 else "odd"
            print(f"    PI={pi_choice}, coin={coin:5s} → {info}, "
                  f"r={r}, sum={s} ({par}) → payoff {payoff:+d}")
        return payoff

    def run_series(label, pi_choice, pii_strat, n=10000):
        payoffs = [simulate_one(pi_choice, pii_strat, verbose=False)
                   for _ in range(n)]
        avg = sum(payoffs) / n
        print(f"  {label}: avg payoff = {avg:+.3f}  (theory: "
              f"{compute_expected_payoff(pi_choice, pii_strat):+.3f})")

    # Show a few individual games
    print(f"\n  ── Sample games: PI=1, PII optimal (3,4,3)/(3,4,4) mixed ──\n")
    for _ in range(8):
        strat = random.choice([(3, 4, 3), (3, 4, 4)])
        simulate_one(1, strat)

    # Monte Carlo averages
    print(f"\n  ── Monte Carlo verification (10,000 games each) ──\n")
    run_series("PI=1 vs PII=(3,4,3)", 1, (3, 4, 3))
    run_series("PI=1 vs PII=(3,4,4)", 1, (3, 4, 4))
    run_series("PI=2 vs PII=(3,4,3)", 2, (3, 4, 3))
    run_series("PI=2 vs PII=(3,4,4)", 2, (3, 4, 4))

    # Equilibrium play
    print(f"\n  ── Equilibrium play (both sides optimal, 10,000 games) ──\n")
    total = 0
    n = 10000
    for _ in range(n):
        i = random.choice([1, 2])
        pii = random.choice([(3, 4, 3), (3, 4, 4)])
        total += simulate_one(i, pii, verbose=False)
    print(f"  Average payoff: {total / n:+.3f}  (theory: −0.300)")


def demo_full_verification():
    """Cross-check all methods agree on the game value."""
    M, _, pii_strats = build_payoff_matrix()
    p_star, v_mixed, q_star = solve_2xn_mixed(M)

    stats = TreeStats()
    v_perf = expectiminimax_perfect_info(stats)
    v_analytical = analytical_game_value(0.5)

    print(f"\n{'═' * 65}")
    print(f"  VERIFICATION")
    print(f"{'═' * 65}")

    checks = [
        ("Perfect info = −0.60", abs(v_perf - (-0.60)) < 1e-9),
        ("Mixed minimax = −0.30", abs(v_mixed - (-0.30)) < 1e-9),
        ("Analytical = −0.30", abs(v_analytical - (-0.30)) < 1e-9),
        ("Mixed = Analytical", abs(v_mixed - v_analytical) < 1e-9),
        ("PI indifferent at equilibrium",
         abs(sum(q_star[j] * M[0][j] for j in range(len(pii_strats))) -
             sum(q_star[j] * M[1][j] for j in range(len(pii_strats)))) < 1e-9),
    ]

    # Verify v(p) = −0.6p for several disclosure probabilities
    for p_test in [0.0, 0.25, 0.5, 0.75, 1.0]:
        expected = -0.6 * p_test
        actual = analytical_game_value(p_test)
        checks.append((f"v({p_test}) = {expected:+.2f}",
                        abs(actual - expected) < 1e-9))

    all_ok = True
    for desc, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {desc}")
        if not passed:
            all_ok = False

    if all_ok:
        print(f"\n  All {len(checks)} checks passed.")


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Part 1: Theory ──
    print(SECTION_1)

    # ── Part 2: Parity payoff structure ──
    demo_conditional_payoffs()

    # ── Part 3: Extensive form game tree ──
    demo_game_tree()

    # ── Part 4: Strategic form ──
    print(SECTION_4)
    M, pii_strats = demo_payoff_table()

    # ── Part 5: Dominance analysis ──
    demo_dominance_analysis(M, pii_strats)

    # ── Part 6: Method comparison ──
    demo_comparison_methods()

    # ── Part 7: Mixed strategy equilibrium ──
    demo_mixed_equilibrium()

    # ── Part 8: Strategy walkthrough ──
    demo_strategy_walkthrough()

    # ── Part 9: Analytical solution ──
    print(SECTION_6)

    # ── Part 10: Value of information ──
    demo_value_of_information()

    # ── Part 11: Game simulations ──
    demo_game_simulation()

    # ── Part 12: Verification ──
    demo_full_verification()

    print(f"\n{'═' * 65}")
    print(f"  CONCLUSION")
    print(f"{'═' * 65}")
    print(f"\n  The Random Disclosure Parity Game has value v = −0.30.")
    print(f"  Player II has a $0.30 per-game advantage, earned through")
    print(f"  the information revealed by the coin toss.")
    print(f"\n  PII's optimal behavioral strategy:")
    print(f"    • When informed of PI's choice → match parity")
    print(f"    • When uninformed → randomise 50/50")
    print(f"\n  The value of information is exactly linear: v = −0.6p")
    print(f"  where p is the probability of disclosure.")
    print()
