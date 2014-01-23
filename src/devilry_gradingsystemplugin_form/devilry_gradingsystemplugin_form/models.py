from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from devilry.apps.core.models import Assignment
from devilry_gradingsystem.models import FeedbackDraft


class Form(models.Model):
    """
    A form consists of zero or more :class:`sections <.Section>`, and
    configuration for how the form should be rendered.
    """
    assignment = models.OneToOneField(Assignment,
        related_name='devilry_gradingsystemplugin_form_form')
    users_can_see = models.CharField(
        default='everything',
        max_length=40,
        choices=(
            ('everything', _('Everything')),
            ('nothing', _('Nothing of the form, they can only see the result like you configure in the next steps')),
            ('points-for-each-section', _('The number of points for each section.')),
        ))

    def clean(self):
        if self.id == None: # If creating a new Form
            if not self.published:
                self.staticfeedback = None # We should NEVER set staticfeedback if published is not True
        else:
            raise ValidationError('Form is immutable (it can not be changed).')
        if self.published and self.staticfeedack is None:
            raise ValidationError('Published Form requires a StaticFeedback.')

    def save(self, *args, **kwargs):
        self.save_timestamp = datetime.now()
        super(Form, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Form')
        verbose_name_plural = _('Forms')



class Section(models.Model):
    """
    Each section contains one or more :class:`questions <.Question>`.
    """
    form = models.ForeignKey(Form)
    title = models.CharField(blank=True, default='', max_length=200)
    text = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')



class Question(models.Model):
    """
    A question of some sort. They all have a title and an optional help text,
    and they all define minimum and maximum points, though some question types
    define min/max points automatically from the alternatives.
    """
    section = models.ForeignKey(Form)
    question_type = models.ChoiceField(
        default='question',
        max_length=40,
        choices=(
            ('radio', _('Select one alternative')),
            ('checkbox', _('Select zero or more alternatives')),
            ('points', _('Point input field')),
            ('scale', _('Scale')),
        ))
    title = models.CharField(
        max_length=400, blank=False, null=False,
        verbose_name=_('Question title'))
    helptext = models.TextField(
        blank=True, default='',
        verbose_name=_('Help text'))
    min_points = models.IntegerField()
    max_points = models.IntegerField()


class Alternative(models.Model):
    """
    Represents an alternative for :class:`.Question` when ``question_type``
    is ``checkbox`` or ``radio``.
    """
    section = models.ForeignKey(Question)
    title = models.CharField(max_length=100)
    points = models.IntegerField()


class Answer(models.Model):
    """
    An answer to a single Question from one examiner.
    """
    draft = models.ForeignKey(FeedbackDraft)
    question = models.ForeignKey(Question)
    points = models.PositiveIntegerField()