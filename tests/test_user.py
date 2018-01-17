from activecampaign3.group import Group
from activecampaign3.resource import InvalidParameters
from activecampaign3.resource import UserFeedback
from activecampaign3.user import User

def assert_user_not_exists(username):
    sr = User.search(search={'username' : username})
    assert sr.total == 0

def assert_user_exists(username):
    sr = User.search(search={'username' : username})
    assert sr.total == 1
    return sr[0]

def test_create_blank_user():
    user = User()
    assert not hasattr(user, 'resource_id')

def test_save_blank_user():
    user = User()
    try:
        user.save()
    except InvalidParameters as e:
        assert "InvalidParameters errors" in repr(e)
        assert len(e.errors) > 1

def test_get_current_user():
    user = User.me()
    assert user.username == 'admin'

def test_set_group_attr():
    user = User()

    try:
        user.group = '1'
        assert False
    except UserFeedback:
        assert not hasattr(user, 'group')

    user.group_id = '1'
    assert user.group_id == '1'

def test_create_user():
    assert_user_not_exists('test')

    user = User(
            username="test",
            email="test@example.com",
            firstName="Jane",
            lastName="Test",
            password="sekret",
            group='1'
            )
    assert not hasattr(user, 'resource_id')
    assert not hasattr(user, 'group')
    assert hasattr(user, 'group_id')
    user.save()
    assert hasattr(user, 'resource_id')

    assert_user_exists('test')

def test_search_by_email():
    sr = User.search(search={"email" : 'test@example.com'})
    assert sr.total == 1
    user = sr[0]
    assert user.email == 'test@example.com'

def test_get_group():
    user = assert_user_exists('test')
    user.load_group()
    assert isinstance(user.group, Group)
    assert user.group_id == '1'
    assert user.group.title == "Visitor"

def test_update_user():
    user = assert_user_exists('test')
    assert user.email == 'test@example.com'

    user.email = 'test2@example.com'
    user.save()

    user = assert_user_exists('test')
    assert user.email == 'test2@example.com'

def test_delete_user():
    user = assert_user_exists('test')
    user.delete()
    assert not hasattr(user, 'resource_id')
    assert_user_not_exists('test')
