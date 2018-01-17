from activecampaign3.group import Group

def test_get_visitors():
    group = Group.get('1')
    assert group.resource_id == '1'
    assert isinstance(group, Group)
    assert group.title == 'Visitor', group.title

def test_get_admin():
    group = Group.get('3')
    assert group.resource_id == '3'
    assert isinstance(group, Group)
    assert group.title == 'Admin'
    assert repr(group) == "<Group 3: Admin>"

def test_list_groups():
    sr = Group.search()
    assert sr.total == 1
    # Visitor group doesn't show up in group list
