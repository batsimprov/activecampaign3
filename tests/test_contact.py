from activecampaign3.contact import Contact
from activecampaign3.resource import NotFound

def test_clean_old_contacts():
    sr = Contact.search()
    for contact in sr:
        contact.delete()

def test_create_contacts():
    contact = Contact(
            email = 'test@example.com',
            firstName = 'Jane',
            lastName = 'Test',
            phone = '555 1212'
            )
    contact.save()

    contact = Contact(
            email = 'test2@example.com',
            firstName = 'Sam',
            lastName = 'Test',
            phone = '555 1212'
            )
    contact.save()

def test_list_contacts():
    sr = Contact.search()
    assert sr.total == 2

def test_search_contact():
    sr = Contact.search(search={'email' : 'test@example.com'})
    assert sr.total == 1
    assert repr(sr[0]) == "<Contact Jane Test (test@example.com)>"

def test_delete_contacts():
    sr = Contact.search()
    assert sr.total == 2
    for contact in sr:
        resource_id = contact.resource_id
        contact.delete()
        assert not hasattr(contact, 'resource_id')
        try:
            Contact.get(resource_id)
            assert False
        except NotFound:
            pass
