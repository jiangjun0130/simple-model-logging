based Django 2.x to logging model instances update

## Installation

`pip install simple-model-logging`

Add `simple-model-logging` to your `INSTALLED_APPS`.

## Usage

#### Low-level use

```
from datetime import datetime

from django.db import models

from .simple_model_logging import SystemUserLogMixin


class AbstractModel(models.Model):
    """
    base model
    """
    STATUS_TYPE = (
        ('1', 'normal'),
        ('2', 'delete'),
        ('3', 'disable')
    )
    create_time = models.DateTimeField('create_time', default=datetime.now)
    update_time = models.DateTimeField('update_time', default=datetime.now)
    update_time = models.DateTimeField('update_time', default=None, null=True, blank=True)
    update_time = models.CharField('update_time', max_length=1, choices=STATUS_TYPE, default='1')

    def model_2_dict(self):
        """
        model to dict
        :return:
        """
        return dict([(attr, getattr(self, attr)) for attr in [field.name for field in self._meta.fields]])

    def delete(self, *args, **kw):
        # logging delete
        SystemUserLogMixin().log_delete(model=self)

        # override delete method
        self.delete_time = datetime.now()
        self.data_status = '2'
        super().save(*args, **kw)

    def save(self, *args, **kw):
        log = SystemUserLogMixin()
        is_insert = False
        if self.id:
            # update
            print('update model')
            # logging update
            log.log_update(model=self)
        else:
            # insert
            # set insert signal
            is_insert = True
            print('insert model')

        super().save(*args, **kw)
        if is_insert:
            # logging insert
            # this code can get the record id
            log.log_create(model=self)

    def create(self, *args, **kw):
        log = SystemUserLogMixin()
        super().create(*args, **kw)
        log.log_create(model=self)

    class Meta:
        abstract = True


class Person(AbstractModel):
    """
    bussiness model extends from AbstractModel.
    when invoke the model's save(),create(),delete() method will do logging
    """
    pass

```