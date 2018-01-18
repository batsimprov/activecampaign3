from activecampaign3.deal import Deal
from activecampaign3.task import Task
from activecampaign3.task import TaskType

task_type_info = {'title' : 'Meeting'}

def test_filter():
    meeting = TaskType.filter_one(task_type_info)
    assert isinstance(meeting, TaskType)

def test_task_deal():
    deals = Deal.search({'title' : 'Big New Deal'})
    deal = deals[0]

    meeting = TaskType.filter_one(task_type_info)
    task = Task(
            title = "write a contact",
            relation = deal,
            task_type = meeting,
            due_date = 'in 2 days'
            )
    task.save()
