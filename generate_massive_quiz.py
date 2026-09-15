import json
import random
import math
import shutil
import re

questions_set = set()
final_questions = []

def add_q(q, opts):
    if q not in questions_set:
        questions_set.add(q)
        random.shuffle(opts)
        final_questions.append({"question": q, "options": opts})

def make_opts(correct, wrong1, wrong2, wrong3, exp):
    return [
        {"text": str(correct), "correct": True, "explanation": exp},
        {"text": str(wrong1), "correct": False, "explanation": "Incorrect."},
        {"text": str(wrong2), "correct": False, "explanation": "Incorrect."},
        {"text": str(wrong3), "correct": False, "explanation": "Incorrect."}
    ]

# 1. Ohm's Law (Voltage)
for v in [5, 10, 12, 15, 24, 48, 60, 70, 100, 120]:
    for r in [2, 4, 8, 16, 32, 50, 100]:
        i = v / r
        q = f"In a DC circuit with {v}V and {r}Ω resistance, what is the current (Amps)?"
        add_q(q, make_opts(round(i,3), round(i*2,3), round(i/2,3), round(v*r,3), "I = V / R"))

        i_val = round(i, 2)
        if i_val > 0 and (v, r, i_val) not in questions_set: # just to vary it
            q2 = f"If a circuit draws {i_val}A through {r}Ω of resistance, what is the voltage?"
            v_ans = i_val * r
            add_q(q2, make_opts(round(v_ans,2), round(v_ans/2,2), round(i_val/r,2), round(r/i_val,2), "V = I * R"))

# 2. Power Law
for v in [5, 10, 20, 50, 100, 120, 240]:
    for i in [0.5, 1, 2, 3, 5, 10, 15, 20]:
        p = v * i
        q = f"What is the power consumed by a device drawing {i}A at {v}V?"
        add_q(q, make_opts(f"{round(p,1)} W", f"{round(p/2,1)} W", f"{round(p*2,1)} W", f"{round(v/i,1)} W", "P = V * I"))

# 3. Inverse Square Law
for spl in [80, 85, 90, 95, 100, 105]:
    for d1 in [1, 2, 4]:
        for d2 in [2, 4, 8, 16, 32, 64]:
            if d1 < d2:
                drop = 20 * math.log10(d2/d1)
                new_spl = spl - drop
                q = f"A speaker produces {spl} dB SPL at {d1} meter(s). What is the SPL at {d2} meters?"
                add_q(q, make_opts(f"{round(new_spl,1)} dB", f"{round(new_spl+3,1)} dB", f"{round(spl-3,1)} dB", f"{round(spl-6,1)} dB", "Distance change uses 20*log10(D1/D2)"))

# 4. Aspect Ratios
ratios = [(16,9, "16:9"), (16,10, "16:10"), (4,3, "4:3"), (21,9, "21:9")]
for w in [40, 50, 60, 70, 80, 90, 100, 120, 140, 150, 160, 180, 200]:
    for rw, rh, name in ratios:
        h = w * (rh / rw)
        q = f"For a {name} aspect ratio display, if the image width is {w} inches, what is the exact image height?"
        add_q(q, make_opts(f"{round(h,2)} inches", f"{round(w*(rw/rh),2)} inches", f"{round(h*1.2,2)} inches", f"{round(h*0.8,2)} inches", f"Height = Width * ({rh}/{rw})"))

# 5. Throw Distance
for w in [40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 180, 200]:
    for tr in [0.5, 0.8, 1.0, 1.2, 1.3, 1.4, 1.5, 1.8, 2.0, 2.5, 3.0, 4.0]:
        td = w * tr
        q = f"A projector has a throw ratio of {tr}:1. If the screen width is {w} inches, what is the throw distance?"
        add_q(q, make_opts(f"{round(td,1)} inches", f"{round(w/tr,1)} inches", f"{round(td*1.5,1)} inches", f"{round(td*0.5,1)} inches", "Throw Distance = Screen Width * Throw Ratio"))

# 6. Viewing Distance (DISCAS / 150-Factor / BDM)
for h in [40, 50, 60, 70, 80, 90, 100, 110, 120, 150]:
    bdm_dist = h * 6
    q = f"Under general guidelines, what is the maximum recommended viewing distance for Basic Decision Making (BDM) if the screen height is {h} inches?"
    add_q(q, make_opts(f"{bdm_dist} inches", f"{h*4} inches", f"{h*8} inches", f"{bdm_dist*2} inches", "BDM Distance = Height * 6"))

    adm_dist = h * 4
    q2 = f"What is the maximum recommended viewing distance for Analytical Decision Making (ADM) if the screen height is {h} inches?"
    add_q(q2, make_opts(f"{adm_dist} inches", f"{h*6} inches", f"{h*8} inches", f"{adm_dist*2} inches", "ADM Distance = Height * 4"))

# Factual Networking
ports = [(80, "HTTP"), (443, "HTTPS"), (21, "FTP"), (22, "SSH"), (23, "Telnet"), (53, "DNS"), (67, "DHCP Server"), (68, "DHCP Client"), (161, "SNMP"), (3389, "RDP")]
for port, name in ports:
    q = f"In networking, which protocol typically uses TCP/UDP port {port} by default?"
    wrongs = random.sample([n for p, n in ports if n != name], 3)
    add_q(q, make_opts(name, wrongs[0], wrongs[1], wrongs[2], f"Port {port} is for {name}."))

layers = {1: "Physical", 2: "Data Link", 3: "Network", 4: "Transport", 5: "Session", 6: "Presentation", 7: "Application"}
for num, name in layers.items():
    q = f"Which layer of the OSI model is Layer {num}?"
    wrongs = random.sample([n for num_other, n in layers.items() if n != name], 3)
    add_q(q, make_opts(name, wrongs[0], wrongs[1], wrongs[2], f"Layer {num} is {name}."))

# Additional math to ensure > 500
for ft in [10, 20, 50, 100, 150, 200, 250, 300, 328, 500, 1000]:
    m = round(ft / 3.28084, 2)
    add_q(f"Convert {ft} feet to meters (approximate).", make_opts(f"{m} m", f"{round(ft/2,2)} m", f"{round(ft*1.5,2)} m", f"{round(m*2,2)} m", "1 meter = ~3.28 feet"))

patterns = [
    ("Omnidirectional", "picks up sound equally from all directions"),
    ("Cardioid", "picks up sound primarily from the front, rejecting the rear"),
    ("Figure-8", "picks up sound from the front and rear, rejecting the sides"),
    ("Hypercardioid", "has a tighter front pickup than cardioid, but introduces a small rear lobe"),
    ("Supercardioid", "is tighter than cardioid, with slightly less rear lobe than hypercardioid")
]
for name, desc in patterns:
    wrongs = random.sample([n for n, d in patterns if n != name], 3)
    add_q(f"Which microphone polar pattern {desc}?", make_opts(name, wrongs[0], wrongs[1], wrongs[2], desc))

# Shuffle and pick exactly 500
random.shuffle(final_questions)
final_500 = final_questions[:500]

with open("/Users/daniel/code/cts-mastery-quiz-native/quizData.json", "w") as f:
    json.dump(final_500, f, indent=2)

# 1. Update HTML
icloud_html = "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/Downloads/CTS_Mastery_Quiz.html"
with open(icloud_html, "r") as f:
    html_content = f.read()

# Instead of re.sub, find the data array manually to avoid escape char issues in JSON dump
start_marker = "const data = "
end_marker = "];\n"
start_idx = html_content.find(start_marker)
if start_idx != -1:
    end_idx = html_content.find(end_marker, start_idx) + 2
    if end_idx > start_idx + len(start_marker):
        html_content = html_content[:start_idx] + start_marker + json.dumps(final_500) + ";\n" + html_content[end_idx:]

with open(icloud_html, "w") as f:
    f.write(html_content)

# 2. Update Native App JSON
icloud_native_json = "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/Downloads/CTS_Mastery_Quiz_Native/quizData.json"
shutil.copy2("/Users/daniel/code/cts-mastery-quiz-native/quizData.json", icloud_native_json)

print(f"Successfully generated {len(final_500)} truly unique questions and injected them. Total pool size was {len(final_questions)}.")
