from door import door_needs_to_close


def test_normal_close():
    input = [10, 50, 13, 13, 60, 14, 14.1]
    angles = None

    for a in input:
        angles, close = door_needs_to_close(angles, a)
        assert close == False
    assert angles == [60, 14, 14.1]

    angles, close = door_needs_to_close(angles, 14.2)
    assert close == True
    assert angles == [14, 14.1, 14.2]


def test_modify_seconds():
    wait = 4
    angles = [10, 50, 13]
    assert len(angles) != wait

    # presupunem ca setarea a fost schimbata in timp ce usa este deschisa
    # totusi, nu cred ca frigiderul ar trebui sa aiba optiunea asta
    angles, close = door_needs_to_close(angles, 14.2, wait=wait)
    assert close == False
    assert len(angles) == wait
