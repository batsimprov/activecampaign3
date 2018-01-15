from activecampaign3.user import User

def test_create_user():
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

def test_delete_user():
    sr = User.search(search={'username' : 'test'})
    assert sr.total == 1
    user = sr[0]
    assert user.email == 'test@example.com'
    user.delete()
    assert not hasattr(user, 'resource_id')
