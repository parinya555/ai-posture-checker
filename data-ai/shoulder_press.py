def detect(angle, stage, counter):

    # ดันขึ้น
    if angle > 160:
        stage = "UP"

    # ลง
    if angle < 90 and stage == "UP":
        stage = "DOWN"
        counter += 1

    return stage, counter