from numax.learning.critic_calibration import calibrate_confidence


def test_calibrate_confidence_stays_bounded():
    value = calibrate_confidence(0.9)

    assert 0.0 <= value <= 1.0
