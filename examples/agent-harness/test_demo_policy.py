from demo_policy import release_allowed

def test_zero_tests_cannot_approve_release():
    assert release_allowed(0, True) is False

def test_real_tests_and_oracle_can_approve_release():
    assert release_allowed(3, True) is True
