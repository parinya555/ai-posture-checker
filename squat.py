def detect(angle, stage, counter):

    # ย่อลง
    if angle < 90:
        stage = "DOWN"

    # ยืนขึ้น
    if angle > 160 and stage == "DOWN":
        stage = "UP"
        counter += 1

    return stage, counter