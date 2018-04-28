__author__ = 'jiangjun'
__date__ = '2018/4/28 上午11:36'

from .views import SystemUserLogViewMixin
from .json_utils import JsonUtils


class View:
    """
    placeholder for from django.views.generic import View
    """
    pass


class Person:
    """
    placeholder for models
    """
    pass


class TestLogView(View, SystemUserLogViewMixin):

    def get_create_model_user(self, user_id):
        """
        return model create user
        :param user_id:  create_user_id
        :return:
        """
        pass

    def get(self, request):
        person = Person()
        person.name = 'Tom'
        person.save()
        # log to create model
        super(TestLogView, self).log_create(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_id=person.id)
        person.age = 20
        person.save()
        create_user_id = super(TestLogView, self).get_create_model_user_id(model_id=person.id, model_class=Person)
        model_create_user = self.get_create_model_user(create_user_id)

        # log to update model
        super(TestLogView, self).log_update(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_create_user=model_create_user, model_id=person.id)

        # log to delete model
        super(TestLogView, self).log_delete(model_class=Person, json_data=JsonUtils.obj_2_json_str(person),
                                            model_create_user=model_create_user, model_id=person.id)

