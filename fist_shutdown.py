import cv2, mediapipe as mp, math, platform, subprocess

# --- SETTINGS ---
SMOOTH_FRAMES = 4
REQUIRED_TRUE = 2
FOLD_MARGIN = 0.08
DIST_RATIO = 0.95
# ---------------

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
TIPS, PIPS, MCPS = [8,12,16,20], [6,10,14,18], [5,9,13,17]

def dist(a,b):
    dx, dy, dz = a.x-b.x, a.y-b.y, getattr(a,"z",0.0)-getattr(b,"z",0.0)
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def finger_folded(lm, tip, pip, mcp, wrist):
    cond_y = (lm[tip].y > lm[pip].y + FOLD_MARGIN) and (lm[tip].y > lm[mcp].y + FOLD_MARGIN)
    cond_d = dist(lm[tip], wrist) < dist(lm[mcp], wrist) * DIST_RATIO
    return cond_y or cond_d

def fist_detect(lm):
    wrist = lm[0]
    folded = [finger_folded(lm,t,p,m,wrist) for t,p,m in zip(TIPS,PIPS,MCPS)]
    return sum(folded) >= 2, folded   # at least 2 folded fingers → fist

def shutdown_now():
    sys = platform.system().lower()
    if "windows" in sys:
        cmd = ["shutdown.exe", "/s", "/f", "/t", "0"]
    elif "darwin" in sys:
        cmd = ["sudo", "shutdown", "-h", "now"]
    else:
        cmd = ["shutdown", "now"]
    print("[EXEC]", " ".join(cmd), flush=True)
    subprocess.run(cmd)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

hist = []

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6) as hands:
    while True:
        ok, frame = cap.read()
        if not ok: break
        frame = cv2.flip(frame, 1)

        res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        raw, folded = False, [False]*4
        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            raw, folded = fist_detect(hand.landmark)

        hist.append(1 if raw else 0)
        if len(hist) > SMOOTH_FRAMES: hist.pop(0)
        smoothed = sum(hist) >= REQUIRED_TRUE

        cv2.putText(frame, f"FIST={smoothed} raw={raw} hist={hist}",
                    (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0,255,0) if smoothed else (0,0,255), 2)

        if smoothed:
            shutdown_now()
            break   # exit after shutdown command

        cv2.imshow("Fist Shutdown (LIVE)", frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
