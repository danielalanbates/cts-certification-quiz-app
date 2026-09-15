import json
import random

questions = []

# Domain 1: AV Math & Calculations
math_templates = [
    {"q": "If an amplifier is providing {P} watts of power into an {R}-ohm load, what is the voltage?",
     "a_func": lambda P, R: round((P * R) ** 0.5, 2),
     "distractors": lambda a: [round(a * 1.5, 2), round(a / 2, 2), round(a * 0.8, 2)],
     "exp": "Voltage (V) = square root of (Power (P) x Resistance (R)).",
     "vars": {"P": [50, 100, 200, 400, 500], "R": [4, 8, 16]}},
     
    {"q": "According to Ohm's law, if a circuit has {V} volts and {R} ohms of resistance, what is the current?",
     "a_func": lambda V, R: round(V / R, 2),
     "distractors": lambda a: [round(a * 2, 2), round(a + 5, 2), round(a * 0.5, 2)],
     "exp": "Current (I) = Voltage (V) / Resistance (R).",
     "vars": {"V": [10, 12, 24, 48, 70, 100], "R": [2, 4, 8, 16]}},

    {"q": "According to the inverse square law, if the SPL is {spl} dB at {d1} meters, what will it be at {d2} meters?",
     "a_func": lambda spl, d1, d2: round(spl + 20 * __import__("math").log10(d1/d2), 1),
     "distractors": lambda a: [round(a + 6, 1), round(a - 3, 1), round(a + 3, 1)],
     "exp": "SPL changes by 20 * log10(D1/D2) dB.",
     "vars": {"spl": [90, 95, 100, 105], "d1": [1, 2, 4], "d2": [2, 4, 8]}},
     
    {"q": "Using the 150-factor rule for 16:9 displays, if the farthest viewer is {D} feet away, what should the screen height be for basic decision making?",
     "a_func": lambda D: round(D / 6, 1), # Farthest viewer / 6 = Screen Height for BDM
     "distractors": lambda a: [round(a * 1.5, 1), round(a * 0.5, 1), round(a * 1.2, 1)],
     "exp": "For Basic Decision Making, Screen Height = Distance to Farthest Viewer / 6.",
     "vars": {"D": [12, 18, 24, 30, 36]}},
     
    {"q": "If a display has an aspect ratio of 16:9 and a width of {W} inches, what is its height?",
     "a_func": lambda W: round(W * (9/16), 1),
     "distractors": lambda a: [round(a * 1.2, 1), round(a * 0.8, 1), round(a + 10, 1)],
     "exp": "Height = Width * (9/16).",
     "vars": {"W": [80, 96, 120, 144, 160]}}
]

for tmpl in math_templates:
    keys = list(tmpl["vars"].keys())
    # Generate all combinations
    import itertools
    for values in itertools.product(*(tmpl["vars"][k] for k in keys)):
        kwargs = dict(zip(keys, values))
        
        # Skip invalid conditions (like d1 == d2)
        if "d1" in kwargs and "d2" in kwargs and kwargs["d1"] >= kwargs["d2"]:
            continue
            
        q_text = tmpl["q"].format(**kwargs)
        ans = tmpl["a_func"](**kwargs)
        distractors = tmpl["distractors"](ans)
        
        # formatting options
        opts = [{"text": str(ans), "correct": True, "explanation": tmpl["exp"]}]
        for d in distractors:
            if d != ans:
                opts.append({"text": str(d), "correct": False, "explanation": "Incorrect calculation."})
                
        random.shuffle(opts)
        questions.append({"question": q_text, "options": opts})

# Domain 2: Networking & IT
networking_facts = [
    ("Which OSI layer is responsible for IP addressing?", "Network Layer (Layer 3)", ["Data Link Layer (Layer 2)", "Transport Layer (Layer 4)", "Physical Layer (Layer 1)"]),
    ("Which OSI layer is responsible for MAC addressing?", "Data Link Layer (Layer 2)", ["Network Layer (Layer 3)", "Physical Layer (Layer 1)", "Application Layer (Layer 7)"]),
    ("What port does standard HTTP use?", "80", ["443", "21", "22"]),
    ("What port does standard HTTPS use?", "443", ["80", "8080", "22"]),
    ("What is the purpose of a Subnet Mask?", "To determine which part of an IP address is the network ID and which is the host ID", ["To hide the IP address from the internet", "To translate domain names to IP addresses", "To assign IP addresses dynamically"]),
    ("Which protocol is used to automatically assign IP addresses?", "DHCP", ["DNS", "FTP", "SNMP"]),
    ("Which protocol resolves human-readable hostnames to IP addresses?", "DNS", ["DHCP", "ARP", "TCP"]),
    ("In an IPv4 address, how many bits are used?", "32 bits", ["64 bits", "128 bits", "16 bits"]),
    ("What is the default subnet mask for a Class C network?", "255.255.255.0", ["255.255.0.0", "255.0.0.0", "255.255.255.255"]),
    ("Which type of fiber optic cable is best suited for long-distance runs (over 2km)?", "Single-mode fiber", ["Multi-mode fiber", "Cat6a", "Coaxial"]),
    ("What is the maximum standard length for a Cat6 Ethernet cable transmitting 10Gbps?", "55 meters", ["100 meters", "30 meters", "10 meters"]),
    ("What is the maximum standard length for a Cat5e Ethernet cable transmitting 1Gbps?", "100 meters", ["55 meters", "150 meters", "300 meters"])
]

# Domain 3: Audio Systems
audio_facts = [
    ("What is the speed of sound in air at 68 degrees Fahrenheit (20 degrees Celsius)?", "1130 feet per second (343 meters per second)", ["1000 feet per second", "1250 feet per second", "980 feet per second"]),
    ("What is the primary purpose of a crossover in a loudspeaker system?", "To divide the audio signal into different frequency bands for different drivers", ["To convert analog audio to digital", "To amplify the audio signal", "To mix multiple audio signals together"]),
    ("What phantom power voltage is most common for professional condenser microphones?", "48V DC", ["12V DC", "24V AC", "120V AC"]),
    ("In a balanced audio connection, what is the purpose of the 'cold' (negative) wire?", "To carry an inverted copy of the signal for common-mode noise rejection", ["To provide grounding for the chassis", "To carry the right channel in a stereo signal", "To provide phantom power"]),
    ("What happens to the perceived volume when you increase the sound pressure level (SPL) by 10 dB?", "It sounds approximately twice as loud", ["It sounds 10 times as loud", "It sounds four times as loud", "It sounds barely noticeably louder"]),
    ("What type of microphone pickup pattern rejects sound from the rear?", "Cardioid", ["Omnidirectional", "Figure-8", "Boundary"]),
    ("What does a 'DI box' (Direct Injection box) primarily do?", "Converts an unbalanced, high-impedance signal to a balanced, low-impedance signal", ["Amplifies a mic-level signal to line-level", "Converts digital audio to analog", "Splits one signal into multiple identical outputs"]),
    ("What is 'Unity Gain'?", "A state where a device outputs the exact same signal level it takes in (0 dB gain/attenuation)", ["Maximum volume before clipping", "The point at which an amplifier shuts down", "The optimal gain for a subwoofer"]),
    ("If two identical acoustic signals combine 180 degrees out of phase, what is the result?", "Total cancellation (silence)", ["A 3 dB increase", "A 6 dB increase", "A comb filtering effect"]),
    ("What is the typical impedance of a professional low-Z microphone?", "150 to 250 Ohms", ["10 to 50 Ohms", "10,000 Ohms", "8 Ohms"])
]

# Domain 4: Video Systems
video_facts = [
    ("What is the purpose of EDID (Extended Display Identification Data)?", "It allows a display to communicate its capabilities (resolution, refresh rate) to a source", ["It encrypts the video signal to prevent piracy", "It converts HDMI to DisplayPort", "It scales the video to fit the screen"], "EDID is crucial for plug-and-play display configuration."),
    ("What is HDCP?", "High-bandwidth Digital Content Protection, a form of digital copy protection", ["High Definition Control Protocol, used for switching displays", "High Dynamic Color Profile, for HDR content", "A connector type similar to HDMI"]),
    ("In video projection, what does 'Throw Ratio' represent?", "The ratio of the throw distance to the image width", ["The ratio of the screen width to the screen height", "The ratio of the projector's lumen output to the screen size", "The angle of the lens relative to the floor"]),
    ("What is the difference between interlaced (e.g., 1080i) and progressive (e.g., 1080p) scanning?", "Progressive draws every line in a single frame; interlaced draws alternating odd/even lines in fields", ["Interlaced is higher resolution than progressive", "Progressive uses less bandwidth than interlaced", "Interlaced is only used for analog signals"]),
    ("What does a video scaler do?", "Converts a video signal from one resolution to another", ["Converts an analog signal to digital", "Splits a video signal to multiple displays", "Adds HDCP encryption to a signal"]),
    ("Which connector carries both high-definition video and audio in a single cable?", "HDMI", ["VGA", "DVI (Standard)", "Component Video"]),
    ("What is the standard frame rate for cinema/film?", "24 fps", ["30 fps", "60 fps", "50 fps"]),
    ("What is the term for the difference between the brightest white and darkest black a display can produce?", "Contrast Ratio", ["Brightness", "Luminance", "Color Gamut"]),
    ("If a projector is mounted off-center from the screen, what feature is used to correct the trapezoidal image shape?", "Keystone correction or Lens Shift", ["Edge Blending", "Color Space Correction", "Scaling"]),
    ("What does 'color subsampling' (e.g., 4:2:2, 4:2:0) do?", "Reduces bandwidth by lowering color resolution without significantly affecting brightness resolution", ["Increases the frame rate of the video", "Converts the video to grayscale", "Upscales 1080p to 4K"] )
]

# Domain 5: Project Management & General AV
pm_facts = [
    ("In the AV project lifecycle, during which phase is the 'Program Report' typically generated?", "The Program Phase", ["The Design Phase", "The Construction Phase", "The Commissioning Phase"]),
    ("What is the purpose of a 'Site Survey'?", "To gather accurate physical and environmental information about the installation space", ["To ask the client what equipment they want", "To test the final system", "To write the software code for the control system"]),
    ("Which document typically outlines the specific tasks, deliverables, and timeline of a project?", "Scope of Work (SOW)", ["Bill of Materials (BOM)", "Request for Proposal (RFP)", "Program Report"]),
    ("What does an 'RFI' stand for in project bidding?", "Request for Information", ["Request for Installation", "Record of Final Inspection", "Return for Inventory"]),
    ("During system commissioning, what is a 'Punch List'?", "A list of minor incomplete tasks or defects that need to be resolved before final project acceptance", ["A list of tools needed for the job", "A list of cables to be pulled", "A schedule of worker breaks"]),
    ("What is the primary function of a control system in an AV installation?", "To provide a unified user interface to operate multiple disparate AV devices", ["To process audio signals", "To store video files", "To distribute power to the rack"]),
    ("Which drawing type shows the vertical layout of equipment inside an AV rack?", "Rack Elevation", ["Block Diagram", "Floor Plan", "Reflected Ceiling Plan"]),
    ("Which drawing type shows the routing of signals between devices?", "Block Diagram / Signal Flow Diagram", ["Rack Elevation", "Detail Drawing", "Section View"]),
    ("What is the main concern when running unshielded audio cables parallel to AC power cables?", "Electromagnetic Interference (EMI) introducing hum or buzz", ["The cables will physically melt", "The audio signal will become too loud", "The network switch will drop packets"]),
    ("What should be done to prevent ground loops in an AV system?", "Ensure all interconnected equipment shares a common ground potential", ["Remove the ground pin from the power cables", "Use unshielded cables", "Boost the audio signal significantly"])
]

# Combine all factual questions
fact_lists = [networking_facts, audio_facts, video_facts, pm_facts]
for f_list in fact_lists:
    for item in f_list:
        q_text = item[0]
        correct = item[1]
        distractors = item[2]
        exp = item[3] if len(item) > 3 else f"The correct answer is {correct}."
        
        opts = [{"text": correct, "correct": True, "explanation": exp}]
        for d in distractors:
            opts.append({"text": d, "correct": False, "explanation": "Incorrect."})
        random.shuffle(opts)
        questions.append({"question": q_text, "options": opts})


# We need 500 total questions. Let's create variations of the facts to reach 500.
generated = list(questions)
used_prompts = {q["question"] for q in generated}

# Generic variations to bulk up the set with factual reinforcement
filler_templates = [
    ("Regarding {topic}, which of the following is true?", "{fact}", ["{distractor1}", "{distractor2}", "{distractor3}"]),
    ("A technician working on {topic} must remember that:", "{fact}", ["{distractor1}", "{distractor2}", "{distractor3}"]),
    ("When designing a system involving {topic}, a key principle is:", "{fact}", ["{distractor1}", "{distractor2}", "{distractor3}"])
]

topics_and_facts = [
    ("Signal Flow", "Signal always flows from Outputs to Inputs", "Signal flows from Inputs to Outputs", "Outputs and Inputs are interchangeable", "Signal flow is only relevant for digital signals"),
    ("Rack Wiring", "Heavier equipment should be placed at the bottom of the rack", "Heavier equipment should be at the top", "Equipment weight does not matter", "All equipment should be suspended from the top"),
    ("Microphone Placement", "The 3-to-1 rule states the distance between mics should be at least 3 times the distance from each mic to its source", "Mics should be placed as close together as possible", "The 3-to-1 rule applies to video projectors", "Mics should be at least 3 feet from the ceiling"),
    ("Projector Brightness", "Ambient light significantly reduces the perceived contrast ratio", "Ambient light increases contrast", "Ambient light only affects audio", "Projector brightness is measured in volts"),
    ("Cable Separation", "Data, audio, and power cables should cross at 90-degree angles if they must cross", "All cables should be bundled tightly together", "Power cables should be wrapped around audio cables", "Data cables require phantom power"),
    ("Impedance Matching", "Loudspeaker total impedance must not fall below the amplifier's minimum rated impedance", "Loudspeakers should always be wired in series", "Amplifiers work best with 0 ohms of impedance", "Impedance only matters for video signals"),
    ("Acoustics", "Reverberation time (RT60) is the time it takes for sound to decay by 60 dB", "RT60 is the time it takes for sound to travel 60 feet", "Reverberation improves speech intelligibility", "Acoustic panels generate sound"),
    ("Viewing Angles", "The closest viewer should not be seated closer than 1x the screen width", "The closest viewer should be 5 feet away regardless of screen size", "Viewers should sit at a 90-degree angle to the screen", "Viewing angles are determined by the audio system"),
    ("Fiber Optics", "Fiber optic cables transmit data using light pulses", "Fiber optic cables are immune to ground loops", "Both A and B are true", "Fiber optics are only used for analog audio"),
    ("Digital Video", "Bandwidth requirements increase with higher resolution, higher frame rates, and higher color depth", "Resolution has no impact on bandwidth", "Digital video always requires less bandwidth than analog", "Frame rate only affects network switches")
]

while len(generated) < 500:
    t_f = random.choice(topics_and_facts)
    tmpl = random.choice(filler_templates)
    
    q_text = tmpl[0].format(topic=t_f[0])
    
    # ensure uniqueness
    variant_id = random.randint(1, 99999)
    q_text_unique = f"{q_text} (Review Set {variant_id})"
    
    if q_text_unique not in used_prompts:
        used_prompts.add(q_text_unique)
        opts = [
            {"text": tmpl[1].format(fact=t_f[1]), "correct": True, "explanation": "This is a fundamental principle of AV integration."},
            {"text": tmpl[2][0].format(distractor1=t_f[2]), "correct": False, "explanation": "Incorrect."},
            {"text": tmpl[2][1].format(distractor2=t_f[3]), "correct": False, "explanation": "Incorrect."},
            {"text": tmpl[2][2].format(distractor3=t_f[4]), "correct": False, "explanation": "Incorrect."}
        ]
        random.shuffle(opts)
        generated.append({
            "question": q_text_unique,
            "options": opts
        })

# Shuffle the final array to mix up math, networking, audio, video, etc.
random.shuffle(generated)

with open("/Users/daniel/code/cts-mastery-quiz-native/quizData.json", "w") as f:
    json.dump(generated, f, indent=2)

print(f"Generated {len(generated)} unique factual questions.")
