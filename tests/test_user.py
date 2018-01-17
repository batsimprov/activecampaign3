from activecampaign3.user import User

def assert_user_not_exists(username):
    sr = User.search(search={'username' : username})
    assert sr.total == 0

def assert_user_exists(username):
    sr = User.search(search={'username' : username})
    assert sr.total == 1
    return sr[0]

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
    user.save()
    assert hasattr(user, 'resource_id')

    assert_user_exists('test')

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
