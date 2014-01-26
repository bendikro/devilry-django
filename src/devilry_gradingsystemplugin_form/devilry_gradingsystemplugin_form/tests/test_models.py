from mock import patch, MagicMock
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import models


#from devilry_developer.testhelpers.corebuilder import PeriodBuilder
#from devilry_developer.testhelpers.corebuilder import UserBuilder
# from devilry_gradingsystemplugin_form.models import 
from devilry_gradingsystemplugin_form.devilry_gradingsystemplugin_form_testapp.models import SortableModel
from devilry_gradingsystemplugin_form.devilry_gradingsystemplugin_form_testapp.models import ContainerModel



class TestAbstractSortableModel(TestCase):
    def test_move_backward(self):
        a = SortableModel.objects.create(label="A", sortindex=0)
        c = SortableModel.objects.create(label="C", sortindex=1)
        d = SortableModel.objects.create(label="D", sortindex=2)
        b = SortableModel.objects.create(label="B", sortindex=3)
        e = SortableModel.objects.create(label="E", sortindex=4)
        SortableModel.objects.move_to_index(b, 1)
        self.assertEquals(SortableModel.objects.get(id=a.id).sortindex, 0)
        self.assertEquals(SortableModel.objects.get(id=b.id).sortindex, 1)
        self.assertEquals(SortableModel.objects.get(id=c.id).sortindex, 2)
        self.assertEquals(SortableModel.objects.get(id=d.id).sortindex, 3)
        self.assertEquals(SortableModel.objects.get(id=e.id).sortindex, 4)

    def test_move_forward(self):
        a = SortableModel.objects.create(label="A", sortindex=0)
        d = SortableModel.objects.create(label="D", sortindex=1)
        b = SortableModel.objects.create(label="B", sortindex=2)
        c = SortableModel.objects.create(label="C", sortindex=3)
        e = SortableModel.objects.create(label="E", sortindex=4)
        SortableModel.objects.move_to_index(d, 3)
        self.assertEquals(SortableModel.objects.get(id=a.id).sortindex, 0)
        self.assertEquals(SortableModel.objects.get(id=b.id).sortindex, 1)
        self.assertEquals(SortableModel.objects.get(id=c.id).sortindex, 2)
        self.assertEquals(SortableModel.objects.get(id=d.id).sortindex, 3)
        self.assertEquals(SortableModel.objects.get(id=e.id).sortindex, 4)

    def test_relatedmanager(self):
        container = ContainerModel.objects.create()
        container.containedsortablemodel_set.append(label='B')
        container.containedsortablemodel_set.insert(0, label='A')
        self.assertEquals(container.containedsortablemodel_set.all()[0].label, 'A')
        self.assertEquals(container.containedsortablemodel_set.all()[1].label, 'B')
        self.assertEquals(container.containedsortablemodel_set.all()[0].sortindex, 0)
        self.assertEquals(container.containedsortablemodel_set.all()[1].sortindex, 1)