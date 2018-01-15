from activecampaign3.deal import Deal

def test_status_values():
    assert Deal.Status.Open.value == 0
    assert Deal.Status.Won.value == 1
    assert Deal.Status.Lost.value == 2
