## two player game involving coin-toss and a number choice and total of four moves (a.k.a known as Blackwell game G.1.2.1)

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Game Tree — Extensive Form</title>
  <style>
    body {
      background: #fff;
      margin: 0;
      padding: 30px;
      display: flex;
      flex-direction: column;
      align-items: center;
      font-family: "Times New Roman", Times, serif;
    }
    h2 {
      font-size: 18px;
      font-weight: normal;
      margin-bottom: 20px;
      letter-spacing: 0.5px;
      color: #222;
    }
    .tree-container {
      overflow-x: auto;
      max-width: 100%;
    }
  </style>
</head>
<body>
  <h2>Extensive-Form Game Tree</h2>
  <div class="tree-container">
    <?xml version="1.0" encoding="UTF-8"?>
<svg width="1400" height="820" xmlns="http://www.w3.org/2000/svg"
     style="background:white;font-family:'Times New Roman',Times,serif;font-size:15px;">

  <defs>
    <style>
      text { font-family: "Times New Roman", Times, serif; }
      .node-label { font-style: italic; font-size: 16px; }
      .edge-label { font-size: 14px; }
      .payoff { font-size: 15px; font-weight: normal; }
      .small { font-size: 13px; }
    </style>
  </defs>

  <line x1="175" y1="232" x2="130" y2="106" stroke="black" stroke-width="1"/>
  <line x1="175" y1="232" x2="175" y2="106" stroke="black" stroke-width="1"/>
  <line x1="175" y1="232" x2="220" y2="106" stroke="black" stroke-width="1"/>
  <text x="130" y="62" text-anchor="middle" class="payoff">9</text>
  <text x="175" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="220" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="130" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="175" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="220" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="175" y="237" text-anchor="middle" class="small">0</text>
  <line x1="325" y1="232" x2="280" y2="106" stroke="black" stroke-width="1"/>
  <line x1="325" y1="232" x2="325" y2="106" stroke="black" stroke-width="1"/>
  <line x1="325" y1="232" x2="370" y2="106" stroke="black" stroke-width="1"/>
  <text x="280" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="325" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="370" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="280" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="325" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="370" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="325" y="237" text-anchor="middle" class="small">0</text>
  <line x1="475" y1="232" x2="430" y2="106" stroke="black" stroke-width="1"/>
  <line x1="475" y1="232" x2="475" y2="106" stroke="black" stroke-width="1"/>
  <line x1="475" y1="232" x2="520" y2="106" stroke="black" stroke-width="1"/>
  <text x="430" y="62" text-anchor="middle" class="payoff">9</text>
  <text x="475" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="520" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="430" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="475" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="520" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="475" y="237" text-anchor="middle" class="small">0</text>
  <line x1="625" y1="232" x2="580" y2="106" stroke="black" stroke-width="1"/>
  <line x1="625" y1="232" x2="625" y2="106" stroke="black" stroke-width="1"/>
  <line x1="625" y1="232" x2="670" y2="106" stroke="black" stroke-width="1"/>
  <text x="580" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="625" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="670" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="580" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="625" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="670" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="625" y="237" text-anchor="middle" class="small">0</text>
  <line x1="775" y1="232" x2="730" y2="106" stroke="black" stroke-width="1"/>
  <line x1="775" y1="232" x2="775" y2="106" stroke="black" stroke-width="1"/>
  <line x1="775" y1="232" x2="820" y2="106" stroke="black" stroke-width="1"/>
  <text x="730" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="775" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="820" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="730" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="775" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="820" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="775" y="237" text-anchor="middle" class="small">0</text>
  <line x1="925" y1="232" x2="880" y2="106" stroke="black" stroke-width="1"/>
  <line x1="925" y1="232" x2="925" y2="106" stroke="black" stroke-width="1"/>
  <line x1="925" y1="232" x2="970" y2="106" stroke="black" stroke-width="1"/>
  <text x="880" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="925" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="970" y="62" text-anchor="middle" class="payoff">5</text>
  <text x="880" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="925" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="970" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="925" y="237" text-anchor="middle" class="small">0</text>
  <line x1="1075" y1="232" x2="1030" y2="106" stroke="black" stroke-width="1"/>
  <line x1="1075" y1="232" x2="1075" y2="106" stroke="black" stroke-width="1"/>
  <line x1="1075" y1="232" x2="1120" y2="106" stroke="black" stroke-width="1"/>
  <text x="1030" y="62" text-anchor="middle" class="payoff">8</text>
  <text x="1075" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="1120" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="1030" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="1075" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="1120" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="1075" y="237" text-anchor="middle" class="small">0</text>
  <line x1="1225" y1="232" x2="1180" y2="106" stroke="black" stroke-width="1"/>
  <line x1="1225" y1="232" x2="1225" y2="106" stroke="black" stroke-width="1"/>
  <line x1="1225" y1="232" x2="1270" y2="106" stroke="black" stroke-width="1"/>
  <text x="1180" y="62" text-anchor="middle" class="payoff">7</text>
  <text x="1225" y="62" text-anchor="middle" class="payoff">6</text>
  <text x="1270" y="62" text-anchor="middle" class="payoff">5</text>
  <text x="1180" y="100" text-anchor="middle" class="payoff">3</text>
  <text x="1225" y="100" text-anchor="middle" class="payoff">2</text>
  <text x="1270" y="100" text-anchor="middle" class="payoff">1</text>
  <text x="1225" y="237" text-anchor="middle" class="small">0</text>

  <line x1="250" y1="415" x2="175" y2="232" stroke="black" stroke-width="1"/>
  <text x="200" y="323" text-anchor="middle" class="edge-label">4</text>
  <line x1="250" y1="415" x2="325" y2="232" stroke="black" stroke-width="1"/>
  <text x="299" y="323" text-anchor="middle" class="edge-label">3</text>
  <line x1="550" y1="415" x2="475" y2="232" stroke="black" stroke-width="1"/>
  <text x="500" y="323" text-anchor="middle" class="edge-label">4</text>
  <line x1="550" y1="415" x2="625" y2="232" stroke="black" stroke-width="1"/>
  <text x="599" y="323" text-anchor="middle" class="edge-label">3</text>
  <line x1="850" y1="415" x2="775" y2="232" stroke="black" stroke-width="1"/>
  <text x="800" y="323" text-anchor="middle" class="edge-label">4</text>
  <line x1="850" y1="415" x2="925" y2="232" stroke="black" stroke-width="1"/>
  <text x="899" y="323" text-anchor="middle" class="edge-label">3</text>
  <line x1="1150" y1="415" x2="1075" y2="232" stroke="black" stroke-width="1"/>
  <text x="1100" y="323" text-anchor="middle" class="edge-label">4</text>
  <line x1="1150" y1="415" x2="1225" y2="232" stroke="black" stroke-width="1"/>
  <text x="1199" y="323" text-anchor="middle" class="edge-label">3</text>

  <circle cx="250" cy="415" r="22" fill="white" stroke="black" stroke-width="1.5"/>
  <text x="250" y="421" text-anchor="middle" class="node-label">II</text>
  <circle cx="550" cy="415" r="22" fill="white" stroke="black" stroke-width="1.5"/>
  <text x="550" y="421" text-anchor="middle" class="node-label">II</text>
  <circle cx="850" cy="415" r="22" fill="white" stroke="black" stroke-width="1.5"/>
  <text x="850" y="421" text-anchor="middle" class="node-label">II</text>
  <circle cx="1150" cy="415" r="22" fill="white" stroke="black" stroke-width="1.5"/>
  <text x="1150" y="421" text-anchor="middle" class="node-label">II</text>
  <ellipse cx="700" cy="415" rx="185" ry="40" fill="none" stroke="black" stroke-width="1.5"/>

  <line x1="400" y1="590" x2="250" y2="415" stroke="black" stroke-width="1"/>
  <text x="303" y="498" text-anchor="middle" class="edge-label">Head</text>
  <text x="303" y="514" text-anchor="middle" class="edge-label">0</text>
  <line x1="400" y1="590" x2="550" y2="415" stroke="black" stroke-width="1"/>
  <text x="497" y="498" text-anchor="middle" class="edge-label">Tail</text>
  <text x="497" y="514" text-anchor="middle" class="edge-label">0</text>
  <line x1="1000" y1="590" x2="850" y2="415" stroke="black" stroke-width="1"/>
  <text x="903" y="498" text-anchor="middle" class="edge-label">Tail</text>
  <text x="903" y="514" text-anchor="middle" class="edge-label">0</text>
  <line x1="1000" y1="590" x2="1150" y2="415" stroke="black" stroke-width="1"/>
  <text x="1097" y="498" text-anchor="middle" class="edge-label">Head</text>
  <text x="1097" y="514" text-anchor="middle" class="edge-label">0</text>

  <circle cx="400" cy="590" r="5" fill="black" stroke="black"/>
  <circle cx="1000" cy="590" r="5" fill="black" stroke="black"/>

  <line x1="700" y1="750" x2="400" y2="590" stroke="black" stroke-width="1"/>
  <text x="538" y="670" text-anchor="middle" class="edge-label">2</text>
  <line x1="700" y1="750" x2="1000" y2="590" stroke="black" stroke-width="1"/>
  <text x="862" y="670" text-anchor="middle" class="edge-label">1</text>

  <circle cx="700" cy="750" r="26" fill="white" stroke="black" stroke-width="1.5"/>
  <text x="700" y="756" text-anchor="middle" class="node-label">I</text>
  <text x="273" y="460" text-anchor="middle" class="edge-label">Head</text>
  <text x="527" y="460" text-anchor="middle" class="edge-label">Tail</text>
  <text x="873" y="460" text-anchor="middle" class="edge-label">Tail</text>
  <text x="1127" y="460" text-anchor="middle" class="edge-label">Head</text>

</svg>
  </div>
</body>
</html>
