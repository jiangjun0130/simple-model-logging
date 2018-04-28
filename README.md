based Django 2.x to logging model instances update

## Installation

`pip install simple-model-logging`

Add `simple-model-logging` to your `INSTALLED_APPS`.

## Usage

#### Low-level use

from simple_model_logging.views import SystemUserLogViewMixin
from simple_model_logging.models import Person
from simple_model_logging.json_utils import JsonUtils


class View:
    """
    from django.views.generic import View
    """
    pass


class TestLogView(View, SystemUserLogViewMixin):

    def get(self, request):
        person = Person()
        person.name = 'Tom'
        person.save()
        super(TestLogView, self).log_create(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_id=person.id)
        person.age = 20
        person.save()
        create_user_id = super(TestLogView, self).get_create_model_user_id(model_id=person.id, model_class=Person)

        super(TestLogView, self).log_update(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_create_user=create_user_id, model_id=person.id)

        super(TestLogView, self).log_delete(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_create_user=create_user_id, model_id=person.id)