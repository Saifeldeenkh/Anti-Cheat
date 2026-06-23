import time

sessions = {}

WARNING_TIME = 3
KILL_TIME    = 5
MAX_WARNINGS = 2


def update_session(session_id: str, is_cheating: bool, cheat_reason: str = None) -> dict:
    now = time.time()

    if session_id not in sessions:
        sessions[session_id] = {
            "last_ok"      : now,
            "warnings"     : 0,
            "status"       : "OK",
            "cheat_reason" : None,
            "cheat_log"    : []
        }

    s = sessions[session_id]

    if not is_cheating:
        s["last_ok"]      = now
        s["status"]       = "OK"
        s["cheat_reason"] = None
        return s

    absent_time = now - s["last_ok"]
    s["cheat_reason"] = cheat_reason

    s["cheat_log"].append({
        "time"    : round(now, 2),
        "reason"  : cheat_reason,
        "duration": round(absent_time, 2)
    })

    if absent_time >= KILL_TIME:
        s["status"] = "TERMINATED"
    elif absent_time >= WARNING_TIME:
        s["warnings"] += 1
        s["last_ok"]   = now
        s["status"]    = f"WARNING_{s['warnings']}"
        if s["warnings"] >= MAX_WARNINGS:
            s["status"] = "TERMINATED"
    else:
        s["status"] = "WATCHING"

    return s
