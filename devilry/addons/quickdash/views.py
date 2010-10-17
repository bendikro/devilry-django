from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from devilry.core.models import Node, Subject, Period, Assignment, \
        AssignmentGroup
from devilry.ui.messages import UiMessages

from devilry.addons.dashboard.dashboardplugin_registry import registry


@login_required
def main(request):
    is_superuser = request.user.is_superuser
    kw = dict(
        is_candidate = AssignmentGroup.where_is_candidate(request.user).count() > 0,
        is_examiner = AssignmentGroup.where_is_examiner(request.user).count() > 0,
        is_nodeadmin = (is_superuser or Node.where_is_admin(request.user).count() > 0),
        is_subjectadmin = (is_superuser or Subject.where_is_admin(request.user).count() > 0),
        is_periodadmin = (is_superuser or Period.where_is_admin(request.user).count() > 0),
        is_assignmentadmin = (is_superuser or Assignment.where_is_admin(request.user).count() > 0),
    )
    important = [x for x in registry.iterimportant(request, **kw)]
    normal = [x for x in registry.iternormal(request, **kw)]
    items =important + normal
    js = registry.iterjs(**kw)
    messages = UiMessages()
    messages.load(request)
    print items
    return render_to_response('devilry/quickdash/main.django.html', {
            'items': items,
            'js': js,
            'messages': messages
            }, context_instance=RequestContext(request))
