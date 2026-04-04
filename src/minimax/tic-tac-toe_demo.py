"""
Tic-Tac-Toe — Minimax & Bellman Equation Analysis
====================================================

GAME DEFINITION
───────────────
  Players X and O alternate placing their mark on a 3×3 grid.
  X always moves first.  Each move is made with full knowledge of
  the board (perfect information).
  The first player to place three marks in a row (horizontal,
  vertical, or diagonal) WINS and receives +1; the opponent receives −1.
  If the board is filled with no three-in-a-row, the game is a DRAW (0).

This is a finite, two-person, zero-sum game of perfect information —
a textbook setting for minimax and the Bellman optimality equation.

Run:  python tic-tac-toe_demo.py
"""

from __future__ import annotations
import math
import time
from dataclasses import dataclass, field
from typing import Optional

# ═══════════════════════════════════════════════════════════════
#  PART 1: FORMAL BELLMAN EQUATION
# ═══════════════════════════════════════════════════════════════

SECTION_1 = """
═══════════════════════════════════════════════════════════════════
  PART 1: THE BELLMAN EQUATION FOR TIC-TAC-TOE
═══════════════════════════════════════════════════════════════════

  STATE SPACE
  ───────────
  The state is the board configuration: a 3×3 grid where each
  cell is one of { Empty, X, O }.  The player to move is determined
  by counting marks — if #X == #O then X moves, else O moves.

  There are at most 3^9 = 19683 board configurations, but many are
  unreachable (e.g. both players having three-in-a-row).  The actual
  number of legal game states is 5478.

  ACTIONS
  ───────
  At state s, the current player picks any empty cell (r, c).

  TERMINAL CONDITIONS
  ───────────────────
  1. Three-in-a-row for X  →  payoff +1 (X wins)
  2. Three-in-a-row for O  →  payoff −1 (O wins)
  3. Board full, no winner  →  payoff  0 (draw)

  BELLMAN OPTIMALITY EQUATION
  ───────────────────────────
  Define V(s) = value of the game to Player X under optimal play
  from both sides, at board state s.

  Terminal states:
      V(s) = +1   if X has three-in-a-row
      V(s) = −1   if O has three-in-a-row
      V(s) =  0   if board is full with no winner

  Non-terminal states:
      If it is X's turn (MAX):
          V(s) = max     V(s')     where s' = result of X playing in cell c
                 c ∈ empty(s)

      If it is O's turn (MIN):
          V(s) = min     V(s')     where s' = result of O playing in cell c
                 c ∈ empty(s)

  CONNECTION TO STANDARD BELLMAN FORM
  ────────────────────────────────────
  The standard Bellman equation for zero-sum games is:

      V*(s) = max_a min_b [ R(s,a,b) + γ V*(s') ]

  In Tic-Tac-Toe:
  • MAX and MIN alternate turns (X maximizes, O minimizes).
  • R = 0 for non-terminal transitions; terminal reward ∈ {+1, 0, −1}.
  • γ = 1 (undiscounted, finite horizon).
  • The game tree has at most 9! = 362880 leaf nodes (in practice
    many branches terminate early with a win).

  KNOWN RESULT: Under perfect play from both sides, Tic-Tac-Toe is
  a DRAW (V(empty board) = 0).  Neither player can force a win.
"""


# ═══════════════════════════════════════════════════════════════
#  PART 2: BOARD REPRESENTATION AND GAME LOGIC
# ═══════════════════════════════════════════════════════════════

EMPTY = 0
X_MARK = 1
O_MARK = -1

SYMBOL = {EMPTY: '.', X_MARK: 'X', O_MARK: 'O'}

WIN_LINES = [
    # Rows
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    # Columns
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    # Diagonals
    (0, 4, 8), (2, 4, 6),
]


def make_board() -> list[int]:
    return [EMPTY] * 9


def current_player(board: list[int]) -> int:
    """X moves when #X == #O, O moves otherwise."""
    count_x = board.count(X_MARK)
    count_o = board.count(O_MARK)
    return X_MARK if count_x == count_o else O_MARK


def empty_cells(board: list[int]) -> list[int]:
    return [i for i in range(9) if board[i] == EMPTY]


def check_winner(board: list[int]) -> Optional[int]:
    """Return X_MARK, O_MARK, or None."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    return None


def is_terminal(board: list[int]) -> bool:
    return check_winner(board) is not None or len(empty_cells(board)) == 0


def terminal_value(board: list[int]) -> Optional[int]:
    """Return +1 (X wins), −1 (O wins), 0 (draw), or None (not terminal)."""
    w = check_winner(board)
    if w is not None:
        return w  # +1 for X, −1 for O
    if len(empty_cells(board)) == 0:
        return 0
    return None


def board_str(board: list[int], indent: str = "  ") -> str:
    rows = []
    for r in range(3):
        cells = [SYMBOL[board[3 * r + c]] for c in range(3)]
        rows.append(indent + " ".join(cells))
    return "\n".join(rows)


def board_str_numbered(board: list[int], indent: str = "  ") -> str:
    """Board with cell numbers for empty cells."""
    rows = []
    for r in range(3):
        cells = []
        for c in range(3):
            idx = 3 * r + c
            if board[idx] == EMPTY:
                cells.append(str(idx))
            else:
                cells.append(SYMBOL[board[idx]])
        rows.append(indent + " ".join(cells))
    return "\n".join(rows)


# ═══════════════════════════════════════════════════════════════
#  PART 3: MINIMAX SOLVER (plain, no pruning)
# ═══════════════════════════════════════════════════════════════

@dataclass
class TreeStats:
    nodes: int = 0


def minimax(board: list[int], stats: TreeStats) -> int:
    """
    Plain minimax on the game tree.
    Returns the value to Player X: +1, 0, or −1.
    """
    stats.nodes += 1

    tv = terminal_value(board)
    if tv is not None:
        return tv

    player = current_player(board)
    if player == X_MARK:
        best = -math.inf
        for cell in empty_cells(board):
            board[cell] = X_MARK
            val = minimax(board, stats)
            board[cell] = EMPTY
            best = max(best, val)
        return best
    else:
        best = math.inf
        for cell in empty_cells(board):
            board[cell] = O_MARK
            val = minimax(board, stats)
            board[cell] = EMPTY
            best = min(best, val)
        return best


# ═══════════════════════════════════════════════════════════════
#  PART 4: MINIMAX WITH ALPHA-BETA PRUNING
# ═══════════════════════════════════════════════════════════════

def minimax_ab(board: list[int], alpha: float, beta: float,
               stats: TreeStats) -> int:
    """Minimax with alpha-beta pruning. Returns value to Player X."""
    stats.nodes += 1

    tv = terminal_value(board)
    if tv is not None:
        return tv

    player = current_player(board)
    if player == X_MARK:
        best = -math.inf
        for cell in empty_cells(board):
            board[cell] = X_MARK
            val = minimax_ab(board, alpha, beta, stats)
            board[cell] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = math.inf
        for cell in empty_cells(board):
            board[cell] = O_MARK
            val = minimax_ab(board, alpha, beta, stats)
            board[cell] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best


# ═══════════════════════════════════════════════════════════════
#  PART 5: FULL GAME SOLUTION WITH MEMOIZATION
# ═══════════════════════════════════════════════════════════════

def solve_game() -> dict[tuple[int, ...], int]:
    """
    Solve every reachable position via memoized minimax.
    Returns a dict mapping board tuples → value to X.
    """
    memo: dict[tuple[int, ...], int] = {}

    def _solve(board: list[int]) -> int:
        key = tuple(board)
        if key in memo:
            return memo[key]

        tv = terminal_value(board)
        if tv is not None:
            memo[key] = tv
            return tv

        player = current_player(board)
        if player == X_MARK:
            best = -math.inf
            for cell in empty_cells(board):
                board[cell] = X_MARK
                val = _solve(board)
                board[cell] = EMPTY
                best = max(best, val)
        else:
            best = math.inf
            for cell in empty_cells(board):
                board[cell] = O_MARK
                val = _solve(board)
                board[cell] = EMPTY
                best = min(best, val)

        memo[key] = int(best)
        return int(best)

    _solve(make_board())
    return memo


def optimal_move(board: list[int], memo: dict[tuple[int, ...], int]) -> int:
    """Return the best cell index for the current player."""
    player = current_player(board)
    best_val = -math.inf if player == X_MARK else math.inf
    best_cell = -1

    for cell in empty_cells(board):
        board[cell] = player
        val = memo[tuple(board)]
        board[cell] = EMPTY

        if player == X_MARK:
            if val > best_val:
                best_val = val
                best_cell = cell
        else:
            if val < best_val:
                best_val = val
                best_cell = cell

    return best_cell


# ═══════════════════════════════════════════════════════════════
#  PART 6: ANALYTICAL PROPERTIES
# ═══════════════════════════════════════════════════════════════

SECTION_6 = """
═══════════════════════════════════════════════════════════════════
  PART 6: ANALYTICAL PROPERTIES OF TIC-TAC-TOE
═══════════════════════════════════════════════════════════════════

  KNOWN RESULTS
  ─────────────
  1. Under optimal play, Tic-Tac-Toe is a DRAW.
     V(empty board) = 0.

  2. The game tree (with early termination at wins) has:
     • 255,168 possible complete games (leaf sequences)
     • 5,478 distinct legal board positions (up to game history)
     • After memoization, only these 5,478 states are evaluated.

  3. Symmetry: The board has an 8-fold symmetry group (rotations
     and reflections of the square).  Exploiting this reduces
     the distinct positions further, but we solve the full state
     space here for clarity.

  4. First-move analysis: X's optimal first moves are the CENTER
     (cell 4) or any CORNER (cells 0, 2, 6, 8).  All guarantee
     a draw against perfect play.  The EDGE first moves (cells
     1, 3, 5, 7) also draw with perfect play but leave fewer
     winning traps against imperfect opponents.

  COMPLEXITY COMPARISON
  ─────────────────────
  Unlike the Addition Game, Tic-Tac-Toe has no clean closed-form
  formula.  The game's value (draw) and optimal strategies must
  be computed by exhaustive search or backward induction.

  However, the state space is small enough (< 6000 positions)
  that brute-force minimax solves it instantly.
"""


# ═══════════════════════════════════════════════════════════════
#  DEMOS
# ═══════════════════════════════════════════════════════════════

def demo_method_comparison():
    """Compare plain minimax, alpha-beta, and memoized solve."""
    print(f"\n{'═' * 65}")
    print(f"  METHOD COMPARISON: Tic-Tac-Toe from empty board")
    print(f"{'═' * 65}")

    board = make_board()

    # 1. Plain minimax
    stats_mm = TreeStats()
    t0 = time.perf_counter()
    v_mm = minimax(board[:], stats_mm)
    t_mm = time.perf_counter() - t0

    # 2. Alpha-beta
    stats_ab = TreeStats()
    t0 = time.perf_counter()
    v_ab = minimax_ab(board[:], -math.inf, math.inf, stats_ab)
    t_ab = time.perf_counter() - t0

    # 3. Memoized solve
    t0 = time.perf_counter()
    memo = solve_game()
    t_memo = time.perf_counter() - t0
    v_memo = memo[tuple(board)]

    result_str = {1: "X wins", -1: "O wins", 0: "Draw"}

    print(f"\n  Method                    │ Value │ Nodes / States │     Time")
    print(f"  ──────────────────────────┼───────┼────────────────┼──────────")
    print(f"  Plain minimax             │  {v_mm:+d}   │ {stats_mm.nodes:>12,}   │ {t_mm:>7.3f}s")
    print(f"  Alpha-beta pruning        │  {v_ab:+d}   │ {stats_ab.nodes:>12,}   │ {t_ab:>7.3f}s")
    print(f"  Memoized solve (all pos.) │  {v_memo:+d}   │ {len(memo):>12,}   │ {t_memo:>7.3f}s")

    print(f"\n  All methods agree: {result_str[v_memo]}")
    if stats_mm.nodes > stats_ab.nodes:
        pct = 100 * (1 - stats_ab.nodes / stats_mm.nodes)
        print(f"  Alpha-beta pruning saved {pct:.1f}% of nodes vs plain minimax")

    return memo


def demo_position_analysis(memo: dict[tuple[int, ...], int]):
    """Analyze the distribution of winning/losing/drawing positions."""
    print(f"\n{'═' * 65}")
    print(f"  POSITION ANALYSIS: All {len(memo):,} reachable states")
    print(f"{'═' * 65}")

    by_turn = {}  # (num_marks, player_to_move) → {+1: count, 0: count, -1: count}

    for board_tuple, value in memo.items():
        n_marks = sum(1 for c in board_tuple if c != EMPTY)
        player = "X" if board_tuple.count(X_MARK) == board_tuple.count(O_MARK) else "O"
        key = (n_marks, player)
        if key not in by_turn:
            by_turn[key] = {+1: 0, 0: 0, -1: 0}
        by_turn[key][value] += 1

    print(f"\n  {'Marks':>5} │ {'To Move':>7} │ {'X wins':>7} │ {'Draw':>7} │ {'O wins':>7} │ {'Total':>7}")
    print(f"  {'─' * 5}──┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}")

    total_x = total_d = total_o = 0
    for n_marks in range(10):
        player = "X" if n_marks % 2 == 0 else "O"
        key = (n_marks, player)
        if key not in by_turn:
            continue
        d = by_turn[key]
        total_x += d[+1]
        total_d += d[0]
        total_o += d[-1]
        print(f"  {n_marks:>5} │ {player:>7} │ {d[+1]:>7} │ {d[0]:>7} │ {d[-1]:>7} │ {sum(d.values()):>7}")

    print(f"  {'─' * 5}──┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}┼{'─' * 9}")
    print(f"  {'Total':>5} │ {'':>7} │ {total_x:>7} │ {total_d:>7} │ {total_o:>7} │ {total_x + total_d + total_o:>7}")


def demo_first_move_analysis(memo: dict[tuple[int, ...], int]):
    """Show the value of each possible first move for X."""
    print(f"\n{'═' * 65}")
    print(f"  FIRST-MOVE ANALYSIS: Value of each opening for X")
    print(f"{'═' * 65}")

    board = make_board()
    result_str = {1: "X wins", -1: "O wins", 0: "Draw"}

    print(f"\n  Cell layout:")
    print(f"    0 │ 1 │ 2       corner │ edge   │ corner")
    print(f"   ───┼───┼───     ────────┼────────┼────────")
    print(f"    3 │ 4 │ 5       edge   │ center │ edge")
    print(f"   ───┼───┼───     ────────┼────────┼────────")
    print(f"    6 │ 7 │ 8       corner │ edge   │ corner")

    print(f"\n  {'Cell':>6} │ {'Type':>8} │ {'V(after X plays here)':>22} │ Result")
    print(f"  {'─' * 6}──┼{'─' * 10}┼{'─' * 24}┼{'─' * 8}")

    cell_types = {0: "corner", 1: "edge", 2: "corner",
                  3: "edge", 4: "center", 5: "edge",
                  6: "corner", 7: "edge", 8: "corner"}

    for cell in range(9):
        board[cell] = X_MARK
        val = memo[tuple(board)]
        board[cell] = EMPTY
        print(f"  {cell:>6} │ {cell_types[cell]:>8} │ {val:>+22} │ {result_str[val]}")

    print(f"\n  All first moves lead to a draw under optimal play.")
    print(f"  Center and corners are equally good; edges are also draws")
    print(f"  but offer fewer traps against imperfect opponents.")


def demo_optimal_game(memo: dict[tuple[int, ...], int]):
    """Play a complete game with both sides playing optimally."""
    print(f"\n{'═' * 65}")
    print(f"  OPTIMAL GAME PLAY: X and O both play perfectly")
    print(f"{'═' * 65}")

    board = make_board()
    move_num = 1

    while not is_terminal(board):
        player = current_player(board)
        player_name = "X (MAX)" if player == X_MARK else "O (MIN)"
        val_before = memo[tuple(board)]

        cell = optimal_move(board, memo)
        row, col = divmod(cell, 3)

        board[cell] = player
        val_after = memo.get(tuple(board))

        status = ""
        if val_after is not None:
            status = f"  [position value: {val_after:+d}]"

        print(f"\n  Move {move_num}: {player_name} plays cell {cell} (row {row}, col {col}){status}")
        print(board_str(board, indent="    "))

        move_num += 1

    tv = terminal_value(board)
    result_str = {1: "X wins!", -1: "O wins!", 0: "Draw!"}
    print(f"\n  ★ Result: {result_str[tv]}")
    print(f"  (As expected — perfect play always draws.)")


def demo_x_exploits_mistake(memo: dict[tuple[int, ...], int]):
    """Show how X can exploit a suboptimal move by O."""
    print(f"\n{'═' * 65}")
    print(f"  X EXPLOITS A MISTAKE: O plays suboptimally")
    print(f"{'═' * 65}")

    board = make_board()
    move_num = 1

    # X plays center optimally
    board[4] = X_MARK
    print(f"\n  Move 1: X (MAX) plays cell 4 (center)")
    print(board_str(board, indent="    "))

    # O makes a mistake: plays edge instead of corner
    board[1] = O_MARK
    val = memo[tuple(board)]
    print(f"\n  Move 2: O (MIN) plays cell 1 (edge) — MISTAKE!")
    print(f"    Position value is now {val:+d} (X can force a win)")
    print(board_str(board, indent="    "))
    move_num = 3

    while not is_terminal(board):
        player = current_player(board)
        player_name = "X (MAX)" if player == X_MARK else "O (MIN)"

        cell = optimal_move(board, memo)
        row, col = divmod(cell, 3)

        board[cell] = player
        val = memo.get(tuple(board))
        status = f"  [position value: {val:+d}]" if val is not None else ""

        print(f"\n  Move {move_num}: {player_name} plays cell {cell} (row {row}, col {col}){status}")
        print(board_str(board, indent="    "))
        move_num += 1

    tv = terminal_value(board)
    result_str = {1: "X wins!", -1: "O wins!", 0: "Draw!"}
    print(f"\n  ★ Result: {result_str[tv]}")
    print(f"  One mistake by O and X converts the draw into a win.")


def demo_o_exploits_mistake(memo: dict[tuple[int, ...], int]):
    """Show how O can exploit a blunder by X to force a win."""
    print(f"\n{'═' * 65}")
    print(f"  O EXPLOITS A BLUNDER: X blunders, O forces a win")
    print(f"{'═' * 65}")

    cell_type = {0: "corner", 1: "edge", 2: "corner", 3: "edge",
                 4: "center", 5: "edge", 6: "corner", 7: "edge", 8: "corner"}
    board = make_board()

    board[1] = X_MARK
    print(f"\n  Move 1: X (MAX) plays cell 1 ({cell_type[1]})")
    print(board_str(board, indent="    "))

    o_cell = optimal_move(board, memo)
    board[o_cell] = O_MARK
    print(f"\n  Move 2: O (MIN) plays cell {o_cell} ({cell_type[o_cell]}) — optimal")
    print(board_str(board, indent="    "))

    # Find X's worst move (the one that minimizes V, hoping for V = −1)
    worst_val = math.inf
    worst_cell = -1
    for cell in empty_cells(board):
        board[cell] = X_MARK
        val = memo[tuple(board)]
        board[cell] = EMPTY
        if val < worst_val:
            worst_val = val
            worst_cell = cell

    board[worst_cell] = X_MARK
    val = memo[tuple(board)]
    print(f"\n  Move 3: X (MAX) plays cell {worst_cell} ({cell_type[worst_cell]}) — BLUNDER!")
    print(f"    Position value is now {val:+d} {'(O can force a win)' if val == -1 else ''}")
    print(board_str(board, indent="    "))

    move_num = 4
    while not is_terminal(board):
        player = current_player(board)
        player_name = "X (MAX)" if player == X_MARK else "O (MIN)"

        cell = optimal_move(board, memo)
        row, col = divmod(cell, 3)

        board[cell] = player
        val = memo.get(tuple(board))
        status = f"  [position value: {val:+d}]" if val is not None else ""

        print(f"\n  Move {move_num}: {player_name} plays cell {cell} (row {row}, col {col}){status}")
        print(board_str(board, indent="    "))
        move_num += 1

    tv = terminal_value(board)
    result_str = {1: "X wins!", -1: "O wins!", 0: "Draw!"}
    print(f"\n  ★ Result: {result_str[tv]}")
    if tv == -1:
        print(f"  The classic 'opposite edges' blunder lets O create a fork.")


def demo_bellman_values_on_board(memo: dict[tuple[int, ...], int]):
    """Show the minimax value of each possible move as a 3×3 grid."""
    print(f"\n{'═' * 65}")
    print(f"  BELLMAN VALUE MAPS: Value of each move for key positions")
    print(f"{'═' * 65}")

    def show_value_map(board: list[int], label: str):
        player = current_player(board)
        pname = "X" if player == X_MARK else "O"
        print(f"\n  {label}")
        print(f"  Current board:          Move values for {pname}:")

        board_rows = []
        value_rows = []
        for r in range(3):
            b_cells = []
            v_cells = []
            for c in range(3):
                idx = 3 * r + c
                b_cells.append(SYMBOL[board[idx]])
                if board[idx] == EMPTY:
                    board[idx] = player
                    val = memo[tuple(board)]
                    board[idx] = EMPTY
                    v_cells.append(f"{val:+d}")
                else:
                    v_cells.append(SYMBOL[board[idx]])
            board_rows.append("  " + " ".join(f"{x:>2}" for x in b_cells))
            value_rows.append("  " + " ".join(f"{x:>2}" for x in v_cells))

        for br, vr in zip(board_rows, value_rows):
            print(f"  {br}          {vr}")

    # Empty board — X to move
    show_value_map(make_board(), "Empty board (X to move):")

    # After X plays center
    b1 = make_board()
    b1[4] = X_MARK
    show_value_map(b1, "After X plays center (O to move):")

    # After X=center, O=corner
    b2 = make_board()
    b2[4] = X_MARK
    b2[0] = O_MARK
    show_value_map(b2, "After X=center, O=corner (X to move):")

    # After X=corner, O=non-center (a losing position for O)
    b3 = make_board()
    b3[0] = X_MARK
    b3[1] = O_MARK
    show_value_map(b3, "After X=corner, O=edge (X to move — X can force win!):")


def demo_game_statistics(memo: dict[tuple[int, ...], int]):
    """Print statistics about the solved game tree."""
    print(f"\n{'═' * 65}")
    print(f"  GAME TREE STATISTICS")
    print(f"{'═' * 65}")

    n_x_wins = sum(1 for v in memo.values() if v == +1)
    n_draws = sum(1 for v in memo.values() if v == 0)
    n_o_wins = sum(1 for v in memo.values() if v == -1)

    n_terminal = 0
    n_x_win_terminal = 0
    n_o_win_terminal = 0
    n_draw_terminal = 0
    for board_tuple in memo:
        board = list(board_tuple)
        if is_terminal(board):
            n_terminal += 1
            tv = terminal_value(board)
            if tv == +1:
                n_x_win_terminal += 1
            elif tv == -1:
                n_o_win_terminal += 1
            else:
                n_draw_terminal += 1

    print(f"\n  Total reachable positions:   {len(memo):>6,}")
    print(f"  Terminal positions:          {n_terminal:>6,}")
    print(f"    X wins (terminal):         {n_x_win_terminal:>6,}")
    print(f"    O wins (terminal):         {n_o_win_terminal:>6,}")
    print(f"    Draws  (terminal):         {n_draw_terminal:>6,}")
    print(f"  Non-terminal positions:     {len(memo) - n_terminal:>6,}")
    print(f"\n  Value distribution (all positions, minimax value):")
    print(f"    Positions where X wins (V=+1): {n_x_wins:>5,}")
    print(f"    Positions that draw   (V= 0): {n_draws:>5,}")
    print(f"    Positions where O wins (V=−1): {n_o_wins:>5,}")


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Part 1: Theory ──
    print(SECTION_1)

    # ── Part 2: Compare methods ──
    memo = demo_method_comparison()

    # ── Part 3: Analytical properties ──
    print(SECTION_6)

    # ── Part 4: Game statistics ──
    demo_game_statistics(memo)

    # ── Part 5: Position analysis ──
    demo_position_analysis(memo)

    # ── Part 6: First-move analysis ──
    demo_first_move_analysis(memo)

    # ── Part 7: Bellman value maps ──
    demo_bellman_values_on_board(memo)

    # ── Part 8: Optimal game play ──
    demo_optimal_game(memo)

    # ── Part 9: Exploiting mistakes ──
    demo_x_exploits_mistake(memo)
    demo_o_exploits_mistake(memo)

    print(f"\n{'═' * 65}")
    print(f"  CONCLUSION")
    print(f"{'═' * 65}")
    print(f"\n  Tic-Tac-Toe is SOLVED: the game-theoretic value is 0 (draw).")
    print(f"  Neither player can force a win against perfect play.")
    print(f"  The minimax algorithm proves this by exhaustive backward")
    print(f"  induction over all {len(memo):,} reachable positions.")
    print()
