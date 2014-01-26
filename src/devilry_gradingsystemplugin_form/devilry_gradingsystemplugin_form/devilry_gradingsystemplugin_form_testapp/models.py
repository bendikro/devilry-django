from django.db import models
from devilry_gradingsystemplugin_form.abstract_sortable_model import AbstractSortableModel



class SortableModel(AbstractSortableModel):
    label = models.CharField(max_length=20)

    def __repr__(self):
        return 'SortableModel({self.label}, sortindex={self.sortindex})'.format(self=self)

    def __unicode__(self):
        return repr(self)


class ContainerModel(models.Model):
    pass

class ContainedSortableModel(AbstractSortableModel):
    container = models.ForeignKey(ContainerModel)
    label = models.CharField(max_length=20)