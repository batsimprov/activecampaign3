from activecampaign3.resource import Resource
from activecampaign3.deal import Deal
from activecampaign3.contact import Contact
from activecampaign3.resource import UnexpectedCondition
from activecampaign3.resource import UserFeedback

import dateparser
fmt = "%Y-%m-%dT%H:%M:%S"

class TaskType(Resource):
    _resource_path = 'dealTasktypes'
    _valid_search_params = ['title']
    _valid_save_params = "title".split()

class Task(Resource):
    _resource_path = 'dealTasks'
    _rename_params = []
    _valid_save_params = "title relType relid status note duedate dealTasktype".split()

    def parse_due_date(self):
        if isinstance(self.due_date, str):
            return dateparser.parse(self.due_date)
        else:
            return self.due_date

    def process_relation(self):
        if not hasattr(self, 'relation'):
            msg = "Task must have a relation object, or be set to None"
            raise UserFeedback(msg)
        elif self.relation is None:
            return (None, '0')
        elif isinstance(self.relation, Deal):
            return ('Deal', str(self.relation.resource_id))
        elif isinstance(self.relation, Contact):
            return ('Subscriber', str(self.relation.resource_id))
        else:
            msg = "relation is %s" % self.relation
            raise UnexpectedCondition(msg)

    def _save_params(self):
        self.dealTasktype = self.task_type.resource_id
        self.duedate = self.parse_due_date().strftime(fmt)
        self.relType, self.relid = self.process_relation()
        if self.relType is None:
            del self.relType
        return super()._save_params()
