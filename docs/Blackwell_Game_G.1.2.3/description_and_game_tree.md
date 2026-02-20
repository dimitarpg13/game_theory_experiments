# The Game G — Parity Selection

## Game Description

This is a two-player zero-sum game involving a chance draw and binary choices across three moves.

**Move 1 — Player I:** selects one of two integers **{0, 1}**.

**Move 2 — Referee (chance):** selects one of two integers **{0, 1}** with equal probabilities **{½, ½}**.

**Move 3 — Player II:** selects one of two integers **{0, 1}**.

**Outcome:** The integers chosen in Moves 1, 2 and 3 are **summed**:
- If **i + j + k = 1** → Player I pays Player II **one unit**
- Otherwise → Player II pays Player I **one unit**

**Information of Player II at Move 3:** Player II is told the value of **j** (the chance outcome) but is **not** told the value of **i** (Player I's choice).

---

## Game Tree

```mermaid
graph TD

    %% ═══════════════════════════════════════
    %% ROOT — Player I
    %% ═══════════════════════════════════════
    I((I))
    I -->|"i = 0"| CL(( ))
    I -->|"i = 1"| CR(( ))

    %% ═══════════════════════════════════════
    %% CHANCE NODES — Referee draws j
    %% ═══════════════════════════════════════
    CL -->|"j = 0 · ½"| II_00((II))
    CL -->|"j = 1 · ½"| II_01((II))
    CR -->|"j = 0 · ½"| II_10((II))
    CR -->|"j = 1 · ½"| II_11((II))

    %% ═══════════════════════════════════════
    %% PLAYER II → TERMINAL NODES
    %% ═══════════════════════════════════════
    II_00 -->|"k = 0"| T1["sum=0 → +1"]
    II_00 -->|"k = 1"| T2["sum=1 → −1"]
    II_01 -->|"k = 0"| T3["sum=1 → −1"]
    II_01 -->|"k = 1"| T4["sum=2 → +1"]
    II_10 -->|"k = 0"| T5["sum=1 → −1"]
    II_10 -->|"k = 1"| T6["sum=2 → +1"]
    II_11 -->|"k = 0"| T7["sum=2 → +1"]
    II_11 -->|"k = 1"| T8["sum=3 → +1"]

    %% ═══════════════════════════════════════
    %% STYLING
    %% ═══════════════════════════════════════

    %% Player I — blue
    style I fill:#4a90d9,color:#fff,stroke:#2c6fad,stroke-width:2px

    %% Chance nodes — grey
    style CL fill:#d0d0d0,stroke:#888,stroke-width:1.5px
    style CR fill:#d0d0d0,stroke:#888,stroke-width:1.5px

    %% Player II nodes — grouped by j value known to II
    %% j=0 information set: II_00 and II_10 (solid green)
    style II_00 fill:#6abf69,color:#fff,stroke:#388e3c,stroke-width:2px
    style II_10 fill:#6abf69,color:#fff,stroke:#388e3c,stroke-width:2px

    %% j=1 information set: II_01 and II_11 (orange dashed)
    style II_01 fill:#ffb74d,color:#000,stroke:#e65100,stroke-width:2px,stroke-dasharray:6 3
    style II_11 fill:#ffb74d,color:#000,stroke:#e65100,stroke-width:2px,stroke-dasharray:6 3

    %% Terminal nodes
    classDef win  fill:#d5ede4,stroke:#2e7d5e,font-size:12px
    classDef loss fill:#fde2de,stroke:#c0392b,font-size:12px
    class T1,T4,T6,T7,T8 win
    class T2,T3,T5 loss

    %% ═══════════════════════════════════════
    %% LEGEND
    %% ═══════════════════════════════════════
    subgraph Legend["Legend"]
        direction LR
        LG1[🔵 Player I — chooses i from 0 or 1 at move 1]
        LG2[⬤ Chance node — draws j = 0 or 1 with prob ½ each]
        LG3[🟢 Player II — H0 info set knows j = 0 uninformed of i]
        LG4[🟠 Player II — H1 info set knows j = 1 uninformed of i]
        LG5[🟩 Terminal — II pays I one unit sum ≠ 1]
        LG6[🟥 Terminal — I pays II one unit sum = 1]
    end
```

> **Note on information sets:** Player II observes **j** but not **i**, yielding two information sets — one per value of j. Each information set contains two nodes (one for each possible value of i), so Player II must choose k without knowing Player I's move.
>
> - **H₀** (green): {(i=0, j=0), (i=1, j=0)} — Player II knows j=0, does **not** know i
> - **H₁** (orange dashed): {(i=0, j=1), (i=1, j=1)} — Player II knows j=1, does **not** know i

---

## Payoff Table

Payoffs shown as **(Player I, Player II)**: +1 means that player receives one unit, −1 means that player pays one unit.

| i | j | Info set | k | i+j+k | Payoff (I, II) | Result |
|:-:|:-:|:--------:|:-:|:-----:|:--------------:|:------:|
| 0 | 0 | H₀ | 0 | 0 | **(+1, −1)** | II pays I |
| 0 | 0 | H₀ | 1 | 1 | **(−1, +1)** | I pays II |
| 0 | 1 | H₁ | 0 | 1 | **(−1, +1)** | I pays II |
| 0 | 1 | H₁ | 1 | 2 | **(+1, −1)** | II pays I |
| 1 | 0 | H₀ | 0 | 1 | **(−1, +1)** | I pays II |
| 1 | 0 | H₀ | 1 | 2 | **(+1, −1)** | II pays I |
| 1 | 1 | H₁ | 0 | 2 | **(+1, −1)** | II pays I |
| 1 | 1 | H₁ | 1 | 3 | **(+1, −1)** | II pays I |

> **Payoff rule:** i + j + k = 1 → I pays II one unit. All other sums (0, 2, 3) → II pays I one unit.

---

## Information Sets

| Player | Info Set | Nodes Included | Known to II | Hidden from II |
|:------:|:--------:|:---------------|:-----------:|:--------------:|
| I | Singleton | Root node only | — | — |
| II | **H₀** | (i=0, j=0), (i=1, j=0) | j = 0 | **i unknown** |
| II | **H₁** | (i=0, j=1), (i=1, j=1) | j = 1 | **i unknown** |

Player II has **two information sets**, each containing **two nodes** — one for each value of i. Since i is unobserved, Player II's strategy is a mapping from {j=0, j=1} to {k=0, k=1}, giving **four pure strategies** in total: (k|j=0, k|j=1) ∈ {(0,0), (0,1), (1,0), (1,1)}.

---

## Node Key

| Style | Node Type | Player | Action Space |
|:-----:|:---------:|:------:|:------------:|
| 🔵 Blue circle | Decision node | Player I | Chooses i ∈ {0, 1} |
| ⚫ Grey circle | Chance node | Referee | Draws j ∈ {0, 1} with prob ½ each |
| 🟢 Green circle | Decision node | Player II — H₀ | Chooses k ∈ {0, 1}, knows j = 0, not i |
| 🟠 Orange dashed circle | Decision node | Player II — H₁ | Chooses k ∈ {0, 1}, knows j = 1, not i |
| 🟩 Green rectangle | Terminal node | — | sum ≠ 1 → II pays I one unit |
| 🟥 Red rectangle | Terminal node | — | sum = 1 → I pays II one unit |
