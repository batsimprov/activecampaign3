from activecampaign3.mailing_list import MailingList

def test_create_list():
    l = MailingList.find_or_create(name = "Main List")
    print(l)

def test_read_lists():
    sr = MailingList.search()
    for l in sr:
        print(l)
