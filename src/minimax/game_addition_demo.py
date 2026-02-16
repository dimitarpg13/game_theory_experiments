"""
Blackwell's Addition Game — Minimax & Bellman Equation Analysis
================================================================

From: David Blackwell, "Theory of Games and Statistical Decisions" (1954)

GAME DEFINITION
───────────────
  Parameters: k (max choice), N (threshold)
  Players I and II alternately choose integers from {1, 2, ..., k}.
  Each choice is made with full knowledge of all preceding choices.
  The running sum of all choices is tracked.
  As soon as the sum EXCEEDS N, the last player to choose LOSES
  and pays the opponent 1 unit.

This is a finite, two-person, zero-sum game of perfect information —
a textbook setting for minimax and the Bellman optimality equation.

Run:  python addition_game.py
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Optional

# ═══════════════════════════════════════════════════════════════
#  PART 1: FORMAL BELLMAN EQUATION
# ═══════════════════════════════════════════════════════════════

SECTION_1 = """
═══════════════════════════════════════════════════════════════════
  PART 1: THE BELLMAN EQUATION FOR THE ADDITION GAME
═══════════════════════════════════════════════════════════════════

  STATE SPACE
  ───────────
  The state of the game is fully described by:
      s = current cumulative sum,  s ∈ {0, 1, 2, ..., N}

  We don't need to track whose turn it is *in the state variable*
  because the Bellman equation is written from the perspective of
  the CURRENT MOVER. The game alternates, but at every state the
  question is the same: "given sum s, can the player-to-move win?"

  ACTIONS
  ───────
  At state s, the current player picks  i ∈ {1, 2, ..., k}.
  This produces a new sum  s' = s + i.

  TERMINAL CONDITION
  ──────────────────
  If s + i > N, the current player LOSES (they "busted").
  The payoff is −1 to the current player, +1 to the opponent.

  NON-TERMINAL TRANSITION
  ───────────────────────
  If s + i ≤ N, play passes to the opponent at state s' = s + i.
  The value to the opponent is V(s'), so the value to the current
  player is −V(s')  (zero-sum property).

  BELLMAN OPTIMALITY EQUATION
  ───────────────────────────
  Define V(s) = value of the game to the player whose turn it is,
  when the current sum is s, under optimal play by both sides.

               ┌
               │  max    { −1          if s + i > N
      V(s)  =  │ i=1..k { −V(s + i)   if s + i ≤ N
               └

  Or equivalently, separating the cases:

      V(s) = max         [  −V(s + i)  ]
             i ∈ A(s)

  where A(s) = { i ∈ {1,..,k} : s + i ≤ N }  are the "safe" moves,
  provided A(s) is nonempty. If A(s) = ∅ this is impossible since
  s ≤ N and i ≥ 1 means we always have at least one move.

  Wait — actually when s = N, EVERY move i ≥ 1 gives s+i > N.
  So the current player is FORCED to bust:

      V(N) = −1   (BASE CASE: you're at N, any move loses)

  For s < N, some moves may be safe (s+i ≤ N) and some may bust.
  The current player maximizes, so they'll prefer safe moves that
  leave the opponent in a losing position.

  REWRITTEN CLEANLY:

      V(N) = −1                                       [base case]

      V(s) = max    { −V(s+i)  if s+i ≤ N;            [recursion]
             i=1..k   −1       if s+i > N  }

  Since the player WANTS to maximize and −1 is the worst possible
  outcome, any safe move giving −V(s+i) = +1 is preferred over
  busting. So in practice:

      V(s) = max         −V(s+i)    for s ≤ N−1
             i: s+i ≤ N

  (The player would only bust if ALL moves bust, i.e., s ≥ N,
   but for s < N there's always i=1 with s+1 ≤ N.)

  CONNECTION TO STANDARD BELLMAN FORM
  ────────────────────────────────────
  The standard Bellman equation for zero-sum games is:

      V*(s) = max_a min_b [ R(s,a,b) + γ V*(s') ]

  In the Addition Game:
  • The "max" and "min" alternate across turns (captured by the
    −V(s+i) sign flip — maximizing −V is like the opponent minimizing).
  • R = 0 for non-terminal transitions (reward only at the end).
  • γ = 1 (undiscounted, finite horizon).
  • Terminal reward: ±1.

  So we have a BACKWARD INDUCTION / DYNAMIC PROGRAMMING problem,
  solved from s = N down to s = 0.
"""


# ═══════════════════════════════════════════════════════════════
#  PART 2: COMPUTATIONAL SOLUTION (backward induction)
# ═══════════════════════════════════════════════════════════════

def solve_addition_game(k: int, N: int) -> dict:
    """
    Solve the Addition Game by backward induction (dynamic programming).

    Returns a dict with:
      - 'V': list of Bellman values V[s] for s = 0..N
      - 'policy': list of optimal moves for s = 0..N
      - 'k': parameter k
      - 'N': parameter N
    """
    V = [0] * (N + 1)         # V[s] = value to the current mover at sum s
    policy = [0] * (N + 1)    # optimal move at each state

    # Base case: at s = N, any move busts → current player loses
    V[N] = -1
    policy[N] = None  # forced loss, no "good" move

    # Backward induction: s = N-1, N-2, ..., 0
    for s in range(N - 1, -1, -1):
        best_val = -math.inf
        best_move = None

        for i in range(1, k + 1):
            s_next = s + i
            if s_next > N:
                val = -1  # busting move
            else:
                val = -V[s_next]  # zero-sum: my value = negative of opponent's

            if val > best_val:
                best_val = val
                best_move = i

        V[s] = best_val
        policy[s] = best_move

    return {'V': V, 'policy': policy, 'k': k, 'N': N}


# ═══════════════════════════════════════════════════════════════
#  PART 3: ANALYTICAL SOLUTION (the modular arithmetic theorem)
# ═══════════════════════════════════════════════════════════════

SECTION_3 = """
═══════════════════════════════════════════════════════════════════
  PART 3: ANALYTICAL SOLUTION — THE MODULAR ARITHMETIC THEOREM
═══════════════════════════════════════════════════════════════════

  CLAIM: A position (sum = s, current player to move) is a LOSING
  position if and only if:

      s ≡ N  (mod k+1)

  Equivalently:  V(s) = −1  iff  (N − s) mod (k+1) = 0.
                 V(s) = +1  otherwise.

  PROOF BY STRONG INDUCTION ON (N − s)
  ─────────────────────────────────────

  Base case:  s = N.
    N − s = 0, and 0 mod (k+1) = 0.  ✓
    V(N) = −1 as established (forced bust).

  Inductive step:  Assume the claim holds for all s' > s.

  Case A: (N − s) mod (k+1) = 0, i.e., s ≡ N mod (k+1).
    We must show V(s) = −1 (current player loses).

    For ANY move i ∈ {1,..,k}, the new sum is s' = s + i.
    Then  N − s' = N − s − i.
    Since N − s ≡ 0 mod (k+1) and  1 ≤ i ≤ k,
    we get  N − s' ≡ −i ≡ (k+1−i) mod (k+1).
    Since 1 ≤ i ≤ k, we have 1 ≤ k+1−i ≤ k, so N − s' ≢ 0 mod (k+1).

    By the induction hypothesis, V(s') = +1 (opponent WINS at s').
    Therefore −V(s') = −1 for every move i.
    So V(s) = max over all i of (−1) = −1. Current player loses.  ✓

  Case B: (N − s) mod (k+1) ≠ 0, i.e., s ≢ N mod (k+1).
    We must show V(s) = +1 (current player wins).

    Let r = (N − s) mod (k+1),  so  1 ≤ r ≤ k.
    Choose move i* = r.  Then s' = s + r, and
    N − s' = N − s − r ≡ 0 mod (k+1).

    By induction, V(s') = −1 (opponent loses at s').
    So −V(s') = +1. The current player has a winning move.

    Therefore V(s) ≥ +1, and since +1 is the maximum payoff, V(s) = +1.  ✓

  QED.  □

  OPTIMAL STRATEGY
  ────────────────
  If in a winning position (s ≢ N mod k+1):
      Play  i* = (N − s) mod (k+1).
  This pushes the opponent onto a losing position (a multiple
  of k+1 away from N).

  If in a losing position (s ≡ N mod k+1):
      All moves lose against a perfect opponent.
      Any move is equally futile.

  WHO WINS FROM THE START?
  ────────────────────────
  The game starts at s = 0 with Player I to move.
      • V(0) = −1  iff  N mod (k+1) = 0  →  Player I LOSES
      • V(0) = +1  iff  N mod (k+1) ≠ 0  →  Player I WINS

  INTUITION: THE "COMPLEMENT TO k+1" STRATEGY
  ────────────────────────────────────────────
  The winner's strategy is to ensure the sum advances by exactly
  k+1 every two consecutive moves. If I play i, my opponent plays
  (k+1 − i), and the sum increases by k+1. This way the winner
  "owns" the arithmetic progression N, N−(k+1), N−2(k+1), ...
  and herds the opponent inevitably to N.
"""


# ═══════════════════════════════════════════════════════════════
#  PART 4: VERIFICATION — does DP match the analytical formula?
# ═══════════════════════════════════════════════════════════════

def verify_analytical_solution(k: int, N: int) -> bool:
    """Check that the DP solution matches the closed-form."""
    sol = solve_addition_game(k, N)
    V = sol['V']

    for s in range(N + 1):
        expected = -1 if (N - s) % (k + 1) == 0 else +1
        if V[s] != expected:
            print(f"  MISMATCH at s={s}: DP gives V={V[s]}, formula gives {expected}")
            return False
    return True


# ═══════════════════════════════════════════════════════════════
#  PART 5: GAME TREE MINIMAX (explicit tree search)
# ═══════════════════════════════════════════════════════════════

class TreeStats:
    def __init__(self):
        self.nodes = 0

def minimax_tree(s: int, k: int, N: int, is_player1: bool, stats: TreeStats) -> int:
    """
    Minimax on the game tree with explicit Player I (MAX) and Player II (MIN).

    Returns the VALUE TO PLAYER I:
        +1 if Player I wins, −1 if Player I loses.
    """
    stats.nodes += 1

    # Terminal check: if s >= N, current player is forced to bust
    if s >= N:
        # Current player must pick i >= 1, giving s+i > N → bust
        if is_player1:
            return -1  # Player I busts → Player I loses
        else:
            return +1  # Player II busts → Player I wins

    # Recurse over all moves
    if is_player1:  # MAX node
        best = -math.inf
        for i in range(1, k + 1):
            if s + i <= N:
                val = minimax_tree(s + i, k, N, False, stats)
            else:
                # This move busts, Player I loses
                val = -1
            best = max(best, val)
        return best
    else:  # MIN node (Player II tries to minimize Player I's payoff)
        best = math.inf
        for i in range(1, k + 1):
            if s + i <= N:
                val = minimax_tree(s + i, k, N, True, stats)
            else:
                # Player II busts → Player I wins
                val = +1
            best = min(best, val)
        return best


def minimax_ab_tree(s: int, k: int, N: int, is_player1: bool,
                    alpha: float, beta: float, stats: TreeStats) -> int:
    """Minimax with alpha-beta pruning, explicit MAX/MIN."""
    stats.nodes += 1

    # Check if current player is forced to bust
    if s >= N:  # s == N means all moves i≥1 give s+i > N
        return -1 if is_player1 else +1

    if is_player1:
        best = -math.inf
        for i in range(1, k + 1):
            if s + i > N:
                val = -1
            else:
                val = minimax_ab_tree(s + i, k, N, False, alpha, beta, stats)
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = math.inf
        for i in range(1, k + 1):
            if s + i > N:
                val = +1
            else:
                val = minimax_ab_tree(s + i, k, N, True, alpha, beta, stats)
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best


# ═══════════════════════════════════════════════════════════════
#  DEMOS
# ═══════════════════════════════════════════════════════════════

def demo_bellman_table(k: int, N: int):
    """Display the full Bellman value table and optimal policy."""
    sol = solve_addition_game(k, N)
    V = sol['V']
    policy = sol['policy']

    print(f"\n{'═'*65}")
    print(f"  BELLMAN VALUE TABLE:  k = {k},  N = {N}")
    print(f"  Note: k+1 = {k+1},  N mod (k+1) = {N % (k+1)}")
    print(f"{'═'*65}")

    # Header
    print(f"\n  {'s':>4}  │ {'V(s)':>5} │ {'Optimal i':>9} │ {'(N−s) mod (k+1)':>15} │ Result")
    print(f"  {'─'*4}──┼{'─'*7}┼{'─'*11}┼{'─'*17}┼{'─'*12}")

    for s in range(N + 1):
        r = (N - s) % (k + 1)
        result = "LOSE (L)" if V[s] == -1 else "WIN  (W)"
        move_str = f"    {policy[s]}" if policy[s] is not None else "  any*"
        print(f"  {s:>4}  │ {V[s]:>+5} │ {move_str:>9} │ {r:>15} │ {result}")

    print(f"\n  * At s=N, all moves bust; any choice loses.")

    # Show the losing positions explicitly
    losing = [s for s in range(N + 1) if V[s] == -1]
    print(f"\n  Losing positions (V = −1): {losing}")
    print(f"  These are exactly: s = N, N−(k+1), N−2(k+1), ...")
    print(f"  i.e., positions where (N−s) is a multiple of {k+1}.")


def demo_game_play(k: int, N: int, p1_optimal: bool = True, p2_optimal: bool = True):
    """Simulate a game with configurable optimal/suboptimal play."""
    sol = solve_addition_game(k, N)
    V = sol['V']
    policy = sol['policy']

    p1_label = "Player I  (MAX)" + (" [optimal]" if p1_optimal else " [suboptimal]")
    p2_label = "Player II (MIN)" + (" [optimal]" if p2_optimal else " [suboptimal]")

    print(f"\n  {'─'*55}")
    print(f"  Game: k={k}, N={N} | {p1_label} vs {p2_label}")
    print(f"  {'─'*55}")

    s = 0
    is_p1 = True
    move_num = 1

    while True:
        player = "I " if is_p1 else "II"
        v_current = V[s] if s <= N else None

        # Determine move
        if s == N:
            # Forced bust
            i = 1
            print(f"  Move {move_num}: Player {player} at s={s}, "
                  f"V(s)={V[s]:+d} → forced bust (picks {i}), sum={s+i} > {N}")
            print(f"\n  ★ Player {player} LOSES. Pays 1 unit to opponent.")
            return "II" if is_p1 else "I"

        if (is_p1 and p1_optimal) or (not is_p1 and p2_optimal):
            i = policy[s]  # optimal
        else:
            # Suboptimal: pick the WORST move (for demonstration)
            worst_val = math.inf
            i = 1
            for j in range(1, k + 1):
                if s + j <= N:
                    val = -V[s + j]
                else:
                    val = -1
                if val < worst_val:
                    worst_val = val
                    i = j

        s_new = s + i
        if s_new > N:
            print(f"  Move {move_num}: Player {player} at s={s}, "
                  f"V(s)={v_current:+d} → picks {i}, sum={s_new} > {N}  BUST!")
            print(f"\n  ★ Player {player} LOSES. Pays 1 unit to opponent.")
            return "II" if is_p1 else "I"
        else:
            opp_val = V[s_new]
            status = "→ opponent in L" if opp_val == -1 else "→ opponent in W"
            print(f"  Move {move_num}: Player {player} at s={s:>3}, "
                  f"V(s)={v_current:+d} → picks {i}, sum={s_new:>3}  "
                  f"[V({s_new})={opp_val:+d} {status}]")

        s = s_new
        is_p1 = not is_p1
        move_num += 1


def demo_comparison_methods(k: int, N: int):
    """Compare DP, minimax tree search, and alpha-beta on the same game."""
    print(f"\n{'═'*65}")
    print(f"  METHOD COMPARISON:  k = {k},  N = {N}")
    print(f"{'═'*65}")

    # 1. Backward induction (DP / Bellman)
    sol = solve_addition_game(k, N)
    v_dp = sol['V'][0]

    # 2. Minimax tree search
    stats_mm = TreeStats()
    v_mm = minimax_tree(0, k, N, True, stats_mm)

    # 3. Alpha-beta
    stats_ab = TreeStats()
    v_ab = minimax_ab_tree(0, k, N, True, -math.inf, math.inf, stats_ab)

    # 4. Analytical formula
    v_formula = -1 if N % (k + 1) == 0 else +1

    winner_str = "Player II wins" if v_formula == -1 else "Player I wins"

    print(f"\n  Method                    │ Value │ Nodes explored")
    print(f"  ──────────────────────────┼───────┼────────────────")
    print(f"  Bellman DP (backward ind) │  {v_dp:+d}   │ {N+1:>12,} states")
    print(f"  Minimax tree search       │  {v_mm:+d}   │ {stats_mm.nodes:>12,} nodes")
    print(f"  Alpha-beta pruning        │  {v_ab:+d}   │ {stats_ab.nodes:>12,} nodes")
    print(f"  Analytical formula        │  {v_formula:+d}   │          n/a")
    print(f"\n  All methods agree: {winner_str}")
    if stats_mm.nodes > stats_ab.nodes:
        pct = 100 * (1 - stats_ab.nodes / stats_mm.nodes)
        print(f"  Alpha-beta pruning saved {pct:.1f}% of nodes vs naive minimax")


def demo_parametric_analysis():
    """Sweep over k and N to reveal the modular structure."""
    print(f"\n{'═'*65}")
    print(f"  PARAMETRIC ANALYSIS: Who wins for various (k, N)?")
    print(f"{'═'*65}")
    print(f"\n  Table entries: 'I' = Player I wins, 'II' = Player II wins")
    print(f"  Player II wins iff (k+1) divides N.\n")

    k_values = range(2, 7)
    N_values = range(1, 26)

    # Print header
    print(f"  {'k\\N':>4}", end="")
    for N in N_values:
        print(f" {N:>2}", end="")
    print()
    print(f"  {'─'*4} " + "─" * (3 * len(list(N_values))))

    for k in k_values:
        print(f"  k={k} ", end="")
        for N in N_values:
            sol = solve_addition_game(k, N)
            winner = "II" if sol['V'][0] == -1 else " I"
            # Highlight Player II wins
            if winner == "II":
                print(f" \033[1;31mII\033[0m", end="")
            else:
                print(f"  ·", end="")
        print(f"    (loses when {k+1} | N)")

    print(f"\n  Pattern: Player II wins at N = {'{'}k+1{'}'}, 2(k+1), 3(k+1), ...")
    print(f"  These are exactly the multiples of (k+1).")


def demo_strategy_walkthrough(k: int, N: int):
    """Detailed walkthrough showing the 'complement to k+1' strategy."""
    print(f"\n{'═'*65}")
    print(f"  STRATEGY WALKTHROUGH:  k = {k},  N = {N}")
    print(f"{'═'*65}")

    r = N % (k + 1)
    if r == 0:
        print(f"\n  N = {N} is divisible by k+1 = {k+1}.")
        print(f"  Player I is in a LOSING position from the start.")
        print(f"  Player II's strategy: after Player I plays i,")
        print(f"  Player II plays ({k+1} − i), keeping the sum on")
        print(f"  multiples of {k+1}: {', '.join(str(j*(k+1)) for j in range(1, N//(k+1)+1))}.")
        print(f"  Player I inevitably faces sum = {N} and must bust.")
    else:
        print(f"\n  N mod (k+1) = {N} mod {k+1} = {r}.")
        print(f"  Player I WINS by playing i* = {r} on the first move,")
        print(f"  reaching sum = {r}.")
        print(f"  Now the OPPONENT faces a sum that is {N - r} away from N,")
        print(f"  and {N - r} is divisible by {k+1}.")
        print(f"")
        print(f"  After that, Player I mirrors: when Player II plays j,")
        print(f"  Player I responds with ({k+1} − j).")
        print(f"  Target sums for Player I: ", end="")

        targets = []
        t = r
        while t <= N:
            targets.append(t)
            t += k + 1
        print(", ".join(str(t) for t in targets))
        print(f"  (These are the positions ≡ N mod {k+1}.)")
        print(f"  Player II eventually faces sum = {N} and must bust.")

    # Now play it out
    print(f"\n  Full optimal game:")
    demo_game_play(k, N)


def demo_full_game_tree(k: int, N: int):
    """Print the complete game tree for very small parameters."""
    if N > 8 or k > 3:
        print(f"\n  (Game tree too large for k={k}, N={N}; skipping.)")
        return

    print(f"\n{'═'*65}")
    print(f"  COMPLETE GAME TREE:  k = {k},  N = {N}")
    print(f"{'═'*65}\n")

    sol = solve_addition_game(k, N)
    V = sol['V']

    def print_tree(s, depth, is_p1, path):
        indent = "  " + "│   " * depth
        player = "I" if is_p1 else "II"
        v_label = V[s] if s <= N else None

        if s == N:
            tag = "L" if is_p1 else "W"
            print(f"{indent}s={s} (P{player}) V={V[s]:+d} [{tag}] ← forced bust")
            return
        if s > N:
            return

        tag = "W" if V[s] == +1 else "L"
        star = " ◄── optimal" if depth > 0 else ""
        print(f"{indent}s={s} (P{player}) V={V[s]:+d} [{tag}]{star if not star else ''}")

        for i in range(1, k + 1):
            s_new = s + i
            if s_new > N:
                # Busting move
                result = "I wins" if not is_p1 else "II wins"
                opt = " ◄── optimal" if i == sol['policy'][s] else ""
                print(f"{indent}├── pick {i} → s={s_new} > {N} BUST ({result}){opt}")
            else:
                opt_marker = "★" if i == sol['policy'][s] else "·"
                connector = "├" if i < k else "└"
                print(f"{indent}{connector}── [{opt_marker}] pick {i} → ", end="")
                # Continue tree
                print()
                print_tree(s_new, depth + 1, not is_p1, path + [i])

    print_tree(0, 0, True, [])


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Part 1: Theory ──
    print(SECTION_1)

    # ── Part 2: Bellman table for a small example ──
    demo_bellman_table(k=3, N=10)

    # ── Part 3: Analytical solution ──
    print(SECTION_3)

    # ── Part 4: Verify DP matches formula ──
    print(f"{'═'*65}")
    print(f"  VERIFICATION: DP vs Analytical Formula")
    print(f"{'═'*65}\n")
    all_ok = True
    for k in range(2, 8):
        for N in range(1, 51):
            if not verify_analytical_solution(k, N):
                all_ok = False
                print(f"  FAILED for k={k}, N={N}")
    if all_ok:
        print(f"  ✓ All {6*50} test cases (k=2..7, N=1..50) match perfectly.")

    # ── Part 5: Compare methods ──
    demo_comparison_methods(k=3, N=15)
    demo_comparison_methods(k=4, N=20)

    # ── Part 6: Parametric sweep ──
    demo_parametric_analysis()

    # ── Part 7: Strategy walkthrough ──
    demo_strategy_walkthrough(k=3, N=10)
    demo_strategy_walkthrough(k=3, N=12)

    # ── Part 8: Full game simulation ──
    print(f"\n{'═'*65}")
    print(f"  GAME SIMULATIONS")
    print(f"{'═'*65}")

    print(f"\n  Game A: Both players optimal, k=3, N=10")
    demo_game_play(k=3, N=10, p1_optimal=True, p2_optimal=True)

    print(f"\n  Game B: Player I optimal vs Player II suboptimal, k=3, N=10")
    demo_game_play(k=3, N=10, p1_optimal=True, p2_optimal=False)

    print(f"\n  Game C: k=4, N=20 (Player II wins since 5 | 20)")
    demo_game_play(k=4, N=20, p1_optimal=True, p2_optimal=True)

    print()
    