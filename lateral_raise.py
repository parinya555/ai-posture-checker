def detect(angle, stage, counter):

    # ยกแขน
    if angle > 80:
        stage = "UP"

    # ลดแขน
    if angle < 30 and stage == "UP":
        stage = "DOWN"
        counter += 1

    return stage, counter