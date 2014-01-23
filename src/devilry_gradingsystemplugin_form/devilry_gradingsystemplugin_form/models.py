from django.db import models
from django.core.exceptions import ValidationError

from devilry.apps.core.models import Assignment



class Form(models.Model):
    """
    Created by examiners when they provide feedback. A StaticFeedback is
    automatically created when a Form is published.
    """

    # delivery = models.ForeignKey(Delivery, related_name='devilry_gradingsystem_feedbackdraft_set')
    # feedbacktext_editor = models.CharField(
    #     default=DEFAULT_FEEDBACKTEXT_EDITOR,
    #     max_length='20',
    #     choices=(
    #         ('devilry-markdown', 'Markdown editor'),
    #         ('wysiwyg-html', 'WYSIWYG html')
    #     ))
    # published = models.BooleanField(default=False,
    #     help_text='Has this draft been published as a StaticFeedback? Setting this to true on create automatically creates a StaticFeedback.')

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