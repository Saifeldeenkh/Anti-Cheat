from fastapi import FastAPI, UploadFile, File, Form
from backend.eye_detection.eye_detection import detect_eye_from_image
from backend.eye_tracking.eye_tracking import analyze_gaze
from backend.core.session import update_session

app = FastAPI(title="Anti Cheat AI")


@app.get("/")
async def health_check():
    return {"status": "online"}


@app.post("/frame")
async def process_frame(
    session_id: str = Form(...),
    image: UploadFile = File(...)
):
    img_bytes = await image.read()

    yolo_result = detect_eye_from_image(img_bytes)
    gaze_result = analyze_gaze(img_bytes)

    eye_present   = yolo_result["eye_detected"]
    gaze_cheating = gaze_result["is_cheating"]
    is_cheating   = (not eye_present) or gaze_cheating

    cheat_reason = None
    if not eye_present:
        cheat_reason = "no_eye_detected"
    elif gaze_cheating:
        cheat_reason = gaze_result["cheat_reason"]

    logic = update_session(session_id, is_cheating, cheat_reason)

    return {
        "yolo"       : yolo_result,
        "gaze"       : gaze_result,
        "anti_cheat" : logic
    }
