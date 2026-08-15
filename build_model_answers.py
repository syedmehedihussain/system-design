#!/usr/bin/env python3
"""Assemble CSE307_Model_Answers.html: one fully worked question per question type,
lifted verbatim from CSE307_Question_Walkthrough.html so the answers stay identical."""
import re, sys, os

REPO = "/home/husayn/Documents/University/system theory/system-design"
SRC = os.path.join(REPO, "CSE307_Question_Walkthrough.html")
OUT = os.path.join(REPO, "CSE307_Model_Answers.html")

lines = open(SRC, encoding="utf-8").read().split("\n")

# --- locate every question block -------------------------------------------------
starts = {}
for i, l in enumerate(lines):
    m = re.match(r'<h3 id="([a-z0-9]+)"', l)
    if m:
        starts[m.group(1)] = i
order = sorted(starts.items(), key=lambda x: x[1])
ends = {}
for n, (k, i) in enumerate(order):
    nxt = order[n + 1][1] if n + 1 < len(order) else len(lines)
    stop = nxt
    for j in range(i + 1, nxt):
        if lines[j].startswith(("<h2", "</main>", "<section", "</section>", '<div class="case"')):
            stop = j
            break
    ends[k] = stop

def block(qid):
    """Question block with its <h3> stripped (the section <h2> replaces it)."""
    b = lines[starts[qid] + 1 : ends[qid]]
    return "\n".join(b).strip()

def span(a, b):
    return "\n".join(lines[a - 1 : b]).strip()

# --- case studies reused across sections ----------------------------------------
CASE_CT2 = span(91, 99)
CASE_CT3 = span(413, 426)
CASE_A24Q2 = span(1131, 1134)

def details(summary, inner):
    inner = re.sub(r'^<div class="case">', "", inner)
    inner = re.sub(r"</div>$", "", inner).strip()
    inner = re.sub(r'<b class="t">.*?</b>', "", inner, flags=re.S).strip()
    return (f'<details class="ctx"><summary>{summary}</summary>\n'
            f'<div class="ctxbody">{inner}</div></details>')

SVG_HEAD = ('<svg viewBox="0 0 {vb}" xmlns="http://www.w3.org/2000/svg" '
            'style="width:100%;height:auto;background:#fff;display:block">'
            '<defs><marker id="mk" markerWidth="9" markerHeight="9" refX="8" refY="3.2" '
            'orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="#1b1f27"/></marker></defs>')
F = 'font-family="Segoe UI, Helvetica, Arial, sans-serif"'

def txt(x, y, s, size=11, anchor="middle", fill="#1b1f27", weight="600"):
    return f'<text x="{x}" y="{y}" {F} font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{s}</text>'

def box(x, y, w, h, fill, stroke, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'

def line(x1, y1, x2, y2, dash=None, mark=True):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#mk)"' if mark else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1b1f27" stroke-width="1.4"{d}{m}/>'

# --- decision tree SVG ----------------------------------------------------------
COND_F, COND_S = "#eef2ff", "#1d4ed8"
ACT_F, ACT_S = "#ecfdf3", "#067647"
t = [SVG_HEAD.format(vb="1000 470")]
t.append(txt(500, 22, "Decision Tree &#8212; Rent-A-Tool rental approval", 13, weight="700"))
t.append(box(30, 190, 165, 52, COND_F, COND_S))
t.append(txt(112, 213, "Account status?", 11.5, fill="#1e3a8a"))
t.append(box(290, 60, 215, 56, ACT_F, ACT_S))
t.append(txt(397, 82, "Prompt payBalance()", 11, fill="#065f46"))
t.append(txt(397, 98, "Cancel the rental", 11, fill="#065f46"))
t.append(box(290, 265, 165, 52, COND_F, COND_S))
t.append(txt(372, 288, "Tool available?", 11.5, fill="#1e3a8a"))
t.append(box(545, 175, 215, 56, ACT_F, ACT_S))
t.append(txt(652, 197, "Display error", 11, fill="#065f46"))
t.append(txt(652, 213, "Cancel the order", 11, fill="#065f46"))
t.append(box(545, 340, 190, 52, COND_F, COND_S))
t.append(txt(640, 363, "Payment confirmed?", 11.5, fill="#1e3a8a"))
t.append(box(790, 285, 180, 56, ACT_F, ACT_S))
t.append(txt(880, 307, "Display error", 11, fill="#065f46"))
t.append(txt(880, 323, "Cancel the order", 11, fill="#065f46"))
t.append(box(790, 400, 180, 52, ACT_F, ACT_S))
t.append(txt(880, 430, "Create Rental Order", 11, fill="#065f46"))
t.append(line(195, 205, 288, 105))
t.append(txt(236, 143, "Suspended", 10, fill="#5b6472", weight="700"))
t.append(line(195, 228, 288, 285))
t.append(txt(232, 282, "Active", 10, fill="#5b6472", weight="700"))
t.append(line(455, 280, 543, 218))
t.append(txt(497, 240, "No", 10, fill="#5b6472", weight="700"))
t.append(line(455, 300, 543, 358))
t.append(txt(500, 344, "Yes", 10, fill="#5b6472", weight="700"))
t.append(line(735, 355, 788, 320))
t.append(txt(762, 328, "No", 10, fill="#5b6472", weight="700"))
t.append(line(735, 372, 788, 415))
t.append(txt(757, 414, "Yes", 10, fill="#5b6472", weight="700"))
t.append("</svg>")
TREE_SVG = "".join(t)

# --- statechart SVG -------------------------------------------------------------
ST_F, ST_S = "#f5f3ff", "#7c3aed"
s = [SVG_HEAD.format(vb="1000 330")]
s.append(txt(500, 22, "Statechart &#8212; Account life cycle (Rent-A-Tool)", 13, weight="700"))
s.append('<circle cx="60" cy="95" r="9" fill="#1b1f27"/>')
s.append(line(70, 95, 148, 95))
s.append(txt(105, 85, "create", 9.5, fill="#5b6472", weight="400"))
s.append(box(150, 68, 160, 56, ST_F, ST_S, rx=22))
s.append(txt(230, 101, "Active", 12.5, fill="#4c1d95", weight="700"))
s.append(box(560, 68, 175, 56, ST_F, ST_S, rx=22))
s.append(txt(647, 101, "Suspended", 12.5, fill="#4c1d95", weight="700"))
s.append(line(310, 84, 558, 84))
s.append(txt(434, 74, "[balance &lt; minBalance]", 10, fill="#1b1f27"))
s.append('<path d="M 558 112 C 470 150 400 150 312 112" fill="none" stroke="#1b1f27" stroke-width="1.4" marker-end="url(#mk)"/>')
s.append(txt(434, 158, "payBalance() [balance &#8805; minBalance]", 10, fill="#1b1f27"))
s.append(line(230, 124, 230, 218))
s.append(txt(238, 176, "closeAccount()", 10, anchor="start", fill="#1b1f27"))
s.append(box(150, 220, 160, 54, ST_F, ST_S, rx=22))
s.append(txt(230, 252, "Closed", 12.5, fill="#4c1d95", weight="700"))
s.append(line(310, 247, 408, 247))
s.append('<circle cx="428" cy="247" r="13" fill="none" stroke="#1b1f27" stroke-width="1.6"/>')
s.append('<circle cx="428" cy="247" r="7" fill="#1b1f27"/>')
s.append("</svg>")
STATE_SVG = "".join(s)

# --- hand-written sections (no past paper asked these) --------------------------
SPEC_BLOCK = """
<div class="qbox">Drill question (constructed from the Rent-A-Tool case, not from a past paper). A rental is approved only when the account is Active, the tool is available, and the gateway confirms payment. Build the decision table, simplify it, then redraw the same logic as a decision tree. <span>Method drill</span></div>

<div class="step">
<h4>Step 1 &#8212; Draw the four quadrants</h4>
<p>Top-left holds the <b>conditions</b>, top-right the <b>condition alternatives</b>, bottom-left the <b>actions</b>, bottom-right the <b>action entries</b>. Nothing else goes in a decision table.</p>
</div>

<div class="step">
<h4>Step 2 &#8212; Count the columns before you draw them</h4>
<p>Columns = alternatives raised to the number of conditions. Three yes/no conditions give 2&#179; = <b>8 rule columns</b>. Draw all eight even if some collapse later, otherwise you cannot prove completeness.</p>
</div>

<div class="step">
<h4>Step 3 &#8212; Fill the alternatives by halving</h4>
<p>First condition: fill the first half Y, the second half N. Second condition: halve again (YYNN YYNN). Third: alternate every column (YNYN YNYN). This mechanical pattern is what guarantees no combination is missed.</p>
</div>

<div class="step">
<h4>Step 4 &#8212; Put an X where the rule triggers the action</h4>
<p>Work down one column at a time and ask what the business actually does under that exact combination. Blank cells are correct answers.</p>
</div>

<div class="ans">
<h4>Answer &#8212; full table, all 8 rules</h4>
<table>
<tr><th style="width:34%">Conditions</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th></tr>
<tr><td>C1 &#183; Account is Active</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>N</td><td>N</td><td>N</td><td>N</td></tr>
<tr><td>C2 &#183; Tool is available</td><td>Y</td><td>Y</td><td>N</td><td>N</td><td>Y</td><td>Y</td><td>N</td><td>N</td></tr>
<tr><td>C3 &#183; Payment confirmed</td><td>Y</td><td>N</td><td>Y</td><td>N</td><td>Y</td><td>N</td><td>Y</td><td>N</td></tr>
<tr><th>Actions</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr>
<tr><td>A1 &#183; Calculate fee and request payment</td><td>X</td><td>X</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>A2 &#183; Create Rental Order</td><td>X</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>A3 &#183; Display error and cancel order</td><td></td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td><td>X</td></tr>
<tr><td>A4 &#183; Prompt payBalance() to reactivate</td><td></td><td></td><td></td><td></td><td>X</td><td>X</td><td>X</td><td>X</td></tr>
</table>

<h4>Simplified table</h4>
<p>Rules 3 and 4 have identical actions and differ only in C3, so C3 stops mattering and becomes a dash. Rules 5 to 8 are all identical, so both C2 and C3 collapse. Four rules survive:</p>
<table>
<tr><th style="width:34%">Conditions</th><th>R1</th><th>R2</th><th>R3</th><th>R4</th></tr>
<tr><td>C1 &#183; Account is Active</td><td>Y</td><td>Y</td><td>Y</td><td>N</td></tr>
<tr><td>C2 &#183; Tool is available</td><td>Y</td><td>Y</td><td>N</td><td>&#8211;</td></tr>
<tr><td>C3 &#183; Payment confirmed</td><td>Y</td><td>N</td><td>&#8211;</td><td>&#8211;</td></tr>
<tr><th>Actions</th><th></th><th></th><th></th><th></th></tr>
<tr><td>A1 &#183; Calculate fee and request payment</td><td>X</td><td>X</td><td></td><td></td></tr>
<tr><td>A2 &#183; Create Rental Order</td><td>X</td><td></td><td></td><td></td></tr>
<tr><td>A3 &#183; Display error and cancel order</td><td></td><td>X</td><td>X</td><td>X</td></tr>
<tr><td>A4 &#183; Prompt payBalance() to reactivate</td><td></td><td></td><td></td><td>X</td></tr>
</table>

<h4>Answer &#8212; the same logic as a decision tree</h4>
<div class="fig">__TREE__</div>
<div class="figcap">One condition per node, branching left to right in the order the business actually checks them, an action at every leaf. Four leaves for four surviving rules, which is the cross-check that the tree and the table agree.</div>

<h4>Structured English for the same logic</h4>
<pre>IF account status is Active
    IF tool is available
        calculate rentalFee
        request payment from Payment Gateway
        IF payment confirmed
            create Rental Order
        ELSE
            display error
            cancel order
    ELSE
        display error
        cancel order
ELSE
    prompt payBalance() to reactivate account
    cancel order</pre>
</div>

<div class="chk">
<b>Marker's checklist</b>
<ul>
<li>Four quadrants drawn and labelled &#10004;</li>
<li>Column count justified as 2&#179; = 8 &#10004;</li>
<li>Alternatives filled by the halving pattern, no combination missing &#10004;</li>
<li>Simplification shown with dashes, and the merge explained &#10004;</li>
<li>Checked for the four problems: incompleteness, impossible situations, contradictions, redundancy &#10004;</li>
<li>Tree leaves match the simplified rule count &#10004;</li>
</ul>
</div>
"""

STATE_BLOCK = """
<div class="qbox">Drill question (constructed from the Rent-A-Tool case, not from a past paper). Draw a statechart diagram for the Account class. <span>Method drill</span></div>

<div class="step">
<h4>Step 1 &#8212; Pick one class with a life cycle</h4>
<p>A statechart is drawn for a <b>single class</b>, never for the whole system. Choose one whose object visibly changes condition over time: Account, RentalOrder, Job, Student. The CT2 case hands you Account directly, since it is specialized into ActiveAccount and SuspendedAccount.</p>
</div>

<div class="step">
<h4>Step 2 &#8212; List the states, not the actions</h4>
<p>States are conditions of being, so they read as adjectives or past participles: <b>Active</b>, <b>Suspended</b>, <b>Closed</b>. If you catch yourself writing a verb inside a state box you are drawing an activity diagram by mistake.</p>
</div>

<div class="step">
<h4>Step 3 &#8212; Label every transition with the event that causes it</h4>
<p>Transitions are the verbs and the triggers, optionally with a guard in brackets: <code>[balance &lt; minBalance]</code>, <code>payBalance() [balance &#8805; minBalance]</code>. An unlabelled arrow earns nothing.</p>
</div>

<div class="step">
<h4>Step 4 &#8212; Start and finish properly</h4>
<p>A filled circle marks the initial state, and a bullseye marks the final state if the object's life actually ends. Not every statechart needs a final state, but Account does once it can be closed.</p>
</div>

<div class="ans">
<h4>Answer</h4>
<div class="fig">__STATE__</div>
<div class="figcap">Account has exactly the two states the case study names, plus a terminal Closed state. The return transition carries both the event and the guard, which is where the marks concentrate.</div>
<p class="alt">Same method, different class: RentalOrder runs Created &#8594; Paid &#8594; Active &#8594; Returned &#8594; Closed, with the payment failure branch going straight from Created to Cancelled.</p>
</div>

<div class="chk">
<b>Marker's checklist</b>
<ul>
<li>One class named as the diagram title &#10004;</li>
<li>Initial filled circle present &#10004;</li>
<li>States are conditions of being, transitions are events &#10004;</li>
<li>Every transition labelled, guards in square brackets &#10004;</li>
<li>Final state shown as a bullseye &#10004;</li>
</ul>
</div>
"""

SPEC_BLOCK = SPEC_BLOCK.replace("__TREE__", TREE_SVG)
STATE_BLOCK = STATE_BLOCK.replace("__STATE__", STATE_SVG)

# --- section table --------------------------------------------------------------
# (anchor, nav label, heading, meta line, context html, body html)
SECTIONS = [
    ("usecase", "Use Case", "Use Case Diagram",
     "Source: CT2 Q1 &#183; 10 marks &#183; Lecture 7",
     details("Case study &#8212; Rent-A-Tool", CASE_CT2), block("ct2q1")),
    ("narration", "Narration", "Use Case Narration",
     "Source: Final Aut24 Q2c &#183; 10 marks &#183; Lecture 7",
     details("Case study &#8212; forwarding NOC or rejection letter", CASE_A24Q2), block("a24q2c")),
    ("activity", "Activity", "Activity Diagram",
     "Source: CT2 Q2 &#183; 10 marks &#183; Lecture 7",
     details("Case study &#8212; Rent-A-Tool", CASE_CT2), block("ct2q2")),
    ("sequence", "Sequence", "Sequence Diagram",
     "Source: CT2 Q4 &#183; 15 marks &#183; Lecture 7",
     details("Case study &#8212; Rent-A-Tool", CASE_CT2), block("ct2q4")),
    ("classd", "Class", "Class Diagram",
     "Source: CT2 Q3 &#183; 15 marks &#183; Lecture 7",
     details("Case study &#8212; Rent-A-Tool", CASE_CT2), block("ct2q3")),
    ("state", "Statechart", "Statechart Diagram",
     "Not asked in CT2, CT3, Sum25 or Aut24 &#183; method drill &#183; Lecture 7",
     "", STATE_BLOCK),
    ("deployment", "Deployment", "Deployment Diagram",
     "Source: Final Aut24 Q4 &#183; 10 marks &#183; Lecture 7", "", block("a24q4")),
    ("dfd", "DFD", "Data Flow Diagram &#8212; Levels 0, 1 and 2",
     "Source: CT3 Q1 &#183; 35 marks &#183; Lecture 8",
     details("Case study and event response table &#8212; Home-Fix", CASE_CT3), block("ct3q1")),
    ("crud", "CRUD", "CRUD Matrix",
     "Source: CT3 Q2 &#183; 15 marks &#183; Lecture 8",
     details("Case study and event response table &#8212; Home-Fix", CASE_CT3), block("ct3q2")),
    ("spec", "Decision Table", "Process Spec &#8212; Decision Table &amp; Tree",
     "Not asked in CT2, CT3, Sum25 or Aut24 &#183; method drill &#183; Lecture 9",
     "", SPEC_BLOCK),
    ("output", "Output Chart", "Output Report &amp; Chart",
     "Source: Final Aut24 Q1b &#183; 10 marks &#183; Lecture 10", "", block("a24q1b")),
    ("inputf", "Input Form", "Input Form",
     "Source: Final Aut24 Q1a &#183; 10 marks &#183; Lecture 11", "", block("a24q1a")),
]

CSS = """
:root{--bg:#0f1115;--card:#171a21;--txt:#e8eaed;--mut:#a0a6b1;--acc:#6ea8fe;--acc2:#ffd166;--ok:#5ddba0;--vio:#c78bff;--line:#262b35}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
header{padding:32px 24px 20px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#1a2030,#0f1115)}
header .in{max-width:1020px;margin:0 auto}
h1{margin:0 0 8px;font-size:26px}
header p{margin:0;color:var(--mut);font-size:14px;max-width:76ch}
nav{position:sticky;top:0;z-index:20;background:#12151c;border-bottom:1px solid var(--line);padding:10px 16px}
nav .in{max-width:1020px;margin:0 auto;display:flex;gap:8px;flex-wrap:wrap}
nav a{color:var(--acc);text-decoration:none;font-size:13px;padding:5px 10px;border:1px solid var(--line);border-radius:20px}
nav a:hover{background:#1d2330}
nav a.home{color:var(--ok);border-color:#2c4a3c}
nav a.bk{color:var(--vio);border-color:#4a3a5e}
main{max-width:1020px;margin:0 auto;padding:26px 20px 80px}
section{margin:0 0 54px;scroll-margin-top:64px}
h2{font-size:23px;margin:0 0 4px;padding-bottom:8px;border-bottom:2px solid var(--acc);scroll-margin-top:64px}
h3{font-size:18px;margin:30px 0 8px;color:var(--vio)}
h4{font-size:14px;margin:20px 0 6px;color:var(--ok);text-transform:uppercase;letter-spacing:.6px}
.meta{color:var(--mut);font-size:12.5px;margin:8px 0 4px;letter-spacing:.3px}
.drill{color:var(--acc2)}
.case{background:#14202b;border-left:3px solid var(--ok);border-radius:8px;padding:14px 18px;margin:14px 0;font-size:14.5px}
.case b.t{display:block;color:var(--ok);text-transform:uppercase;font-size:12px;letter-spacing:.8px;margin-bottom:6px}
.ctx{background:#14202b;border-left:3px solid var(--ok);border-radius:8px;padding:10px 16px;margin:14px 0;font-size:14.5px}
.ctx summary{cursor:pointer;color:var(--ok);text-transform:uppercase;font-size:12px;letter-spacing:.8px;font-weight:700;list-style:none}
.ctx summary::-webkit-details-marker{display:none}
.ctx summary::before{content:"\\25B8 ";display:inline-block;transition:transform .15s}
.ctx[open] summary::before{content:"\\25BE "}
.ctxbody{margin-top:10px}
.qbox{background:#2a1f10;border-left:3px solid var(--acc2);border-radius:8px;padding:12px 16px;margin:20px 0 12px;font-weight:600}
.qbox span{float:right;color:var(--acc2);font-weight:400;font-size:13px}
.step{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:14px 18px;margin:12px 0}
.ans{background:#1a1524;border-left:3px solid var(--vio);border-radius:8px;padding:14px 18px;margin:12px 0}
.chk{background:#122019;border-left:3px solid var(--ok);border-radius:8px;padding:12px 18px;margin:12px 0;font-size:14.5px}
.fig{background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px;margin:14px 0;overflow-x:auto}
.fig svg{min-width:640px}
.figcap{color:var(--mut);font-size:12.5px;margin:-6px 0 14px;padding-left:2px}
table.steps th{background:#1d2330}
table.steps td{font-size:13.5px}
p.alt{font-size:13.5px;color:var(--acc2);margin:8px 0 0}
pre{background:#0b0e13;border:1px solid var(--line);border-radius:8px;padding:14px;overflow-x:auto;font-size:12.5px;line-height:1.45;color:#d6dae2;white-space:pre}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:#1d2330;color:var(--acc2)}
ol{padding-left:22px}ol li{margin:5px 0}
ul{padding-left:20px}ul li{margin:3px 0}
code{background:#242a35;padding:1px 5px;border-radius:4px;font-size:13px}
.toc{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin:20px 0 0}
.toc a{display:block;text-decoration:none;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--vio);border-radius:8px;padding:11px 14px;color:var(--txt);font-size:14px}
.toc a:hover{background:#1d2330;border-color:var(--vio)}
.toc a b{display:block;color:var(--vio);font-size:14.5px}
.toc a em{font-style:normal;color:var(--mut);font-size:12px}
footer{border-top:1px solid var(--line);color:var(--mut);font-size:12.5px;text-align:center;padding:24px}
footer a{color:var(--mut)}
"""

navlinks = "\n".join(
    f'<a href="#{a}">{lab}</a>' for a, lab, *_ in SECTIONS
)
toc = "\n".join(
    f'<a href="#{a}"><b>{h}</b><em>{m}</em></a>' for a, lab, h, m, ctx, body in SECTIONS
)

parts = [
    "<!DOCTYPE html>", '<html lang="en">', "<head>", '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width,initial-scale=1">',
    "<title>CSE 307 &#8212; Model Answers, One Per Question Type</title>",
    '<meta name="description" content="One fully worked question per CSE 307 question type: use case, narration, activity, sequence, class, statechart, deployment, DFD, CRUD, decision table, output chart and input form.">',
    f"<style>{CSS}</style>", "</head>", "<body>",
    '<header><div class="in">',
    "<h1>CSE 307 &#8212; Model Answers, One Per Question Type</h1>",
    "<p>Every kind of question the exam can ask, once each, worked end to end: the question, how to think about it, how to draw it, the answer, and the marker's checklist. Answers are taken from the walkthrough book so they match exactly. Use the bar below to jump straight to the type you are practising.</p>",
    f'<div class="toc">{toc}</div>',
    "</div></header>",
    '<nav><div class="in">',
    '<a class="home" href="index.html">&#8592; Home</a>',
    navlinks,
    '<a class="bk" href="CSE307_Question_Walkthrough.html">All questions &#8599;</a>',
    "</div></nav>", "<main>",
]

for a, lab, h, m, ctx, body in SECTIONS:
    cls = ' class="meta drill"' if "Not asked" in m else ' class="meta"'
    parts.append(f'<section id="{a}">')
    parts.append(f"<h2>{h}</h2>")
    parts.append(f"<p{cls}>{m}</p>")
    if ctx:
        parts.append(ctx)
    parts.append(body)
    parts.append("</section>")

parts += [
    "</main>",
    '<footer>Answers lifted from the <a href="CSE307_Question_Walkthrough.html">Question Walkthrough Book</a>. '
    'Theory in the <a href="CSE307_Final_Cram_Sheet.html">Full Cram Sheet</a>. '
    'Start at the <a href="index.html">revision hub</a>.<br>'
    "Statechart and decision table sections are method drills, built from the Rent-A-Tool case, since no available past paper asked them.</footer>",
    "</body>", "</html>",
]

html = "\n".join(parts)
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, len(html), "bytes")
print("sections:", len(SECTIONS))
for a, lab, h, m, ctx, body in SECTIONS:
    print(f"  {a:11} svg={body.count('<svg'):2} table={body.count('<table'):2} chars={len(body):7}  {h}")
