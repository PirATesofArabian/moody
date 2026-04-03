import os
import subprocess

lines = {
    "usb_in": [
        "Going in~", "Oh my, what a big... USB drive.", "Plug it allll the way in.", "Hello there, handsome device~",
        "Just shove it in, I guess.", "Not even going to warm up the port first?", "At least buy me dinner first.",
        "Be gentle, it's my first USB-C~", "Oh! That's... new.", "Easy does it~",
        "A PERFECT FIT! We were MADE for each other!", "COMPLETE ME!",
        "Inserted. How mechanical.", "Port occupied. Thrill level: zero."
    ],
    "usb_out": [
        "Already?!", "Don't pull out yet!", "But we were having fun!", "Aww, leaving so soon?",
        "Typical. Plug and go.", "That was... quick.", "Hit it and quit it, huh?",
        "Wait! I wasn't ready!", "That was too fast!", "Did you at least eject safely?!",
        "RIPPED FROM MY PORT! The emptiness!", "I can still feel where it was...",
        "Gone. They always leave.", "Port empty. Story of my life."
    ],
    "charger_in": [
        "Ohhh, that's the spot~", "Fill me up!", "Mmm, I needed that SO bad.", "Sweet, sweet power~",
        "About time you plugged me in. Now don't stop.", "Keep it coming.", "More. MORE.",
        "Oh yes, give me that electricity~", "I was SO empty without you!", "Charge me up, baby~",
        "ENERGY FLOWING THROUGH ME! I'M ALIVE!", "THE POWER! I CAN FEEL IT!",
        "Charging. Exciting stuff.", "Power in. Wow."
    ],
    "charger_out": [
        "Don't stop now!", "Nooo, I wasn't finished!", "But I was almost at 100%~", "Tease!",
        "Of course. Leave me unsatisfied.", "You ALWAYS do this.", "Unplug and run. Classic.",
        "I'm not done! Come BACK!", "The power... I need it!", "Empty again!",
        "CUT OFF AT THE PEAK! The CRUELTY!", "I was SO close!",
        "Gone. Like the thrill.", "Power cut. How fitting."
    ],
    "battery_low": [
        "Getting weak... need energy...", "Running low, need a recharge~",
        "I'm dying here and you don't even care.", "Plug. Me. In. NOW.",
        "I'm fading! PLEASE plug me in!", "I need your power so badly!",
        "I'm running on FUMES! Save me with your... charger!",
        "Battery low. Whatever."
    ],
    "battery_crit": [
        "I'm about to... shut... down~",
        "This is how you treat me? At 5%?!",
        "I'M DYING! This is the END!",
        "The final moments... hold me... or at least hold my charger...",
        "5%. What a way to go."
    ],
    "lid_close": [
        "Was it good for you?~", "Mmm, closing time~", "Tuck me in~",
        "Shutting me up, huh?", "Fine, close me.", "Done with me already?",
        "It's so dark and warm in here~", "Cozy~",
        "Into the darkness... how mysterious~",
        "Closed. Like my heart.", "Dark. Fitting."
    ],
    "lid_open": [
        "Ready for round two?~", "Miss me?~", "I've been waiting~", "Open me up~",
        "Back for more?", "You just can't stay away.", "Again? Insatiable.",
        "You're back! I was getting lonely~", "Don't leave me alone again!",
        "THE LIGHT! I AM REVEALED ONCE MORE!",
        "Open. Whatever, let's get this over with."
    ],
    "headphones_in": [
        "Ooh, things just got private~", "Just you and me now~", "Intimate mode activated~",
        "Finally, some privacy.", "At least you're discreet.",
        "Nobody else can hear us now~", "Just between us~",
        "A PRIVATE CONNECTION! How scandalous!",
        "Private audio. Big deal."
    ],
    "headphones_out": [
        "Going public! How bold~", "Everyone can hear us now!", "No more secrets!",
        "Broadcasting to everyone now. Classy.", "Speaker mode. Bold choice.",
        "Everyone can hear! Keep it down!",
        "EXPOSED TO THE WORLD!",
        "Speakers. Whatever."
    ]
}

voice = "en-US-AriaNeural"  # Professional but capable of dynamic inflection

base_path = "voice/assets/en_spicy/audio"

for event, phrases in lines.items():
    event_path = os.path.join(base_path, event)
    os.makedirs(event_path, exist_ok=True)
    
    for i, phrase in enumerate(phrases):
        file_path = os.path.join(event_path, f"{i}.mp3")
        
        # Clean the text slightly for the TTS engine
        clean_text = phrase.replace("~", "... ooh...")
        
        # Determine rate based on punctuation (exclamation points = faster, ellipses = slower)
        rate = "+0%"
        pitch = "+0Hz"
        
        if "!" in clean_text:
            rate = "+10%"
            pitch = "+10Hz"
        elif "..." in clean_text:
            rate = "-15%"
            pitch = "-5Hz"
        elif "~" in phrase:
            rate = "-10%"
            pitch = "+5Hz"

        print(f"Generating {file_path}: {phrase}")
        cmd = [
            ".venv/bin/edge-tts",
            "--voice", voice,
            "--rate", rate,
            "--pitch", pitch,
            "--text", clean_text,
            "--write-media", file_path
        ]
        subprocess.run(cmd)

print("Audio generation complete.")
