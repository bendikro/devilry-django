from django.db import models
# from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class SortableQuerySet(models.query.QuerySet):
    def sorted(self, *args, **kwargs):
        return self.order_by('sortindex')


class SortableManager(models.Manager):
    def get_queryset(self):
        return SortableQuerySet(self.model, using=self._db)

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(*args, **kwargs)

    def all(self, *args, **kwargs):
        return self.get_queryset().all(*args, **kwargs)

    def sorted(self, *args, **kwargs):
        return self.get_queryset().sorted()

    def re_enumerate_sortindex(self):
        for index, obj in enumerate(self.sorted()):
            obj.sortindex = index
            obj.save()

    def move_to_index(self, object_to_move, new_sortindex):
        if object_to_move.sortindex == new_sortindex:
            return

        # Re-sort all - not required as long as we are 100% sure that we never insert
        # multiple items with the same index, but I choose to prioritize correctness
        # over speed here. This makes sense as long as we use this to keep small sets
        # of data sorted.
        self.re_enumerate_sortindex()

        # Shift all 
        range_between_new_and_current = None
        shift = 0
        if object_to_move.sortindex < new_sortindex:
            range_between_new_and_current = (object_to_move.sortindex, new_sortindex)
            shift = -1
        else:
            range_between_new_and_current = (new_sortindex, object_to_move.sortindex)
            shift = 1
        self.filter(sortindex__range=range_between_new_and_current)\
            .exclude(id=object_to_move.id)\
            .update(sortindex=models.F('sortindex')+shift)

        object_to_move.sortindex = new_sortindex
        object_to_move.save()

    def append(self, **kwargs):
        sortindex = self.count()
        self.create(sortindex=sortindex, **kwargs)

    def insert(self, sortindex, **kwargs):
        self.filter(sortindex__gte=sortindex)\
            .update(sortindex=models.F('sortindex')+1)
        self.create(sortindex=sortindex, **kwargs)



class AbstractSortableModel(models.Model):
    """
    Defines a sortable model, where the sort order is maintained through the ``sortindex`` field.

    The actual sorting (append, insert and move) should be performed though the :class:`manager <.SortableManager>`::

        class MySortableModel(AbstractSortableModel):
            title = models.CharField(max_length=10)

        x = MySortableModel.objects.append(MySortableModel(title='X'))
        a = MySortableModel.objects.append(MySortableModel(title='A'))
        c = MySortableModel.objects.append(MySortableModel(title='B'))
        d = MySortableModel.objects.append(MySortableModel(title='C'))
        b = MySortableModel.objects.insert(MySortableModel(2, title='B'))
        MySortableModel.objects.move_to_index(5, x)

    It may seem strange to have the functionality on the manager instead of on the
    model, but it makes sense when we use it in a hierarchy of relatedmanagers::

        class MyContainerModel(models.Model):
            name = models.CharField(max_length=10)

        class MySortableModel(AbstractSortableModel):
            container = models.ForeignKey(MyContainerModel)
            title = models.CharField(max_length=10)

        container = MyContainerModel(name='Test')
        container.mysortablemodel_set.append(title='B')
        container.mysortablemodel_set.insert(0, title='A')
    """
    objects = SortableManager()

    #: The sort index - the first index is 0
    sortindex = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['sortindex']