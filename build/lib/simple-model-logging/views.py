from .models import SystemUserLog


class SystemUserLogMethodMixin:

    def __log(self, operation, model_class, json_data, model_create_user, model_update_user, model_id=None):
        """
        创建用户修改数据日志
        :param operation: 操作类型
        :param model_class: 实体类型【全路径】
        :param json_data: 实体json字符串
        :param model_create_user: 实体创建人
        :param model_update_user: 实体更新人
        :param model_id: 实体主键标识
        :return:
        """
        SystemUserLog.objects.create_log(
            operation=operation,
            model_class=model_class,
            json_data=json_data,
            model_create_user=model_create_user,
            model_update_user=model_update_user,
            model_id=model_id
        )

    def log_on_create(self, model_class, json_data, model_create_user, model_update_user, model_id=None):
        self.__log(
            operation=SystemUserLog.OPERATION_ADD,
            model_class=model_class,
            json_data=json_data,
            model_create_user=model_create_user,
            model_update_user=model_update_user,
            model_id=model_id
        )

    def log_on_update(self, model_class, json_data, model_create_user, model_update_user, model_id=None):
        self.__log(
            operation=SystemUserLog.OPERATION_UPDATE,
            model_class=model_class,
            json_data=json_data,
            model_create_user=model_create_user,
            model_update_user=model_update_user,
            model_id=model_id
        )

    def log_on_delete(self, model_class, json_data, model_create_user, model_update_user, model_id):
        self.__log(
            operation=SystemUserLog.OPERATION_DELETE,
            model_class=model_class,
            json_data=json_data,
            model_create_user=model_create_user,
            model_update_user=model_update_user,
            model_id=model_id
        )


class SystemUserLogViewMixin(SystemUserLogMethodMixin):
    """
    记录数据修改日志公共view

    继承该view即可对数据修改进行日志记录
    """

    def log_create(self, model_class, json_data, model_id=None):
        """
        记录新增操作日志
        :param model_class:
        :param json_data:
        :param model_id:
        :return:
        """
        super(SystemUserLogViewMixin, self).log_on_create(model_class=model_class, json_data=json_data,
                                                          model_create_user=self.request.user,
                                                          model_update_user=self.request.user, model_id=model_id)

    def log_update(self, model_class, json_data, model_create_user, model_id=None):
        """
        记录更新操作日志
        :param model_class:
        :param json_data:
        :param model_create_user:
        :param model_id:
        :return:
        """
        super(SystemUserLogViewMixin, self).log_on_update(model_class=model_class, json_data=json_data,
                                                          model_create_user=model_create_user,
                                                          model_update_user=self.request.user, model_id=model_id)

    def log_delete(self, model_class, json_data, model_create_user, model_id):
        """
        记录删除操作日志
        :param model_class:
        :param json_data:
        :param model_create_user:
        :param model_id:
        :return:
        """
        super(SystemUserLogViewMixin, self).log_on_update(model_class=model_class, json_data=json_data,
                                                          model_create_user=model_create_user,
                                                          model_update_user=self.request.user, model_id=model_id)

    def get_create_model_user_id(self, model_id, model_class):
        """
        查询创建实体的用户标识
        :param model_id:
        :param model_class:
        :return:
        """
        log_list = SystemUserLog.objects.filter(model_id=model_id, model_class=model_class,
                                                operation=SystemUserLog.OPERATION_ADD)
        if log_list is not None:
            return log_list[0].model_create_user_id
        else:
            return None
