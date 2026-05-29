def detect(angle, stage, counter):

    # งอแขน
    if angle < 60:
        stage = "UP"

    # เหยียดแขน
    if angle > 140 and stage == "UP":
        stage = "DOWN"
        counter += 1

    return stage, counter