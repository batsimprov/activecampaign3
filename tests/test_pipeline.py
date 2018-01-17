from activecampaign3.pipeline import Pipeline
from activecampaign3.stage import Stage

def test_delete_pipelines():
    sr = Pipeline.search()
    for pipeline in sr:
        pipeline.delete()

def test_create_pipeline():
    pipeline = Pipeline(
            title = "Private Donations",
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

