from activecampaign3.pipeline import Pipeline
from activecampaign3.stage import Stage
from activecampaign3.contact import Contact
from activecampaign3.deal import Deal

def test_delete_pipelines():
    sr = Pipeline.search()
    for pipeline in sr:
        pipeline.delete()

def test_create_pipeline():
    pipeline = Pipeline(
            title = "Private Donations",
            autoassign = '1',
            currency = 'usd',
            )
    pipeline.save()
    pipeline.refresh()
    assert len(pipeline.stages) == 3

    stage = pipeline.stages[0]
    assert isinstance(stage, Stage)

    stage = Stage(
            title = 'Final Follow Up',
            pipeline_id = pipeline.resource_id,
            color = 'ff0000'
            )
    stage.save()

    pipeline.refresh()
    assert len(pipeline.stages) == 4
    assert pipeline.stages[3].resource_id == stage.resource_id

def test_create_deal():
    contact = Contact.find_or_create(
            email = 'test3@example.com'
            )

    pipeline = Pipeline.search()[0]

    deal = Deal(
            customer = contact,
            pipeline = pipeline,
            currency = 'usd',
            title = 'Big New Deal',
            value = 100000
            )
    deal.save()

def test_get_deal():
    deals = Deal.search()
    for deal in deals:
        deal.add_note("Hey this is a really big deal.")
        print(deal)
        print(deal.notes)
