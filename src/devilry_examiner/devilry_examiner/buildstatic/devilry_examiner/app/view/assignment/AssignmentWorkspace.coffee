Ext.define('devilry_examiner.view.assignment.AssignmentWorkspace', {
    extend: 'Ext.Component'
    alias: 'widget.assignmentworkspace'
    cls: 'devilry_assignmentworkspace bootstrap'

    #layout: 'border'
    #padding: '40'
    #autoScroll: true

    # Sent in via the route, and read by the controller to load the appropriate assignment.
    assignmentId: null

    #style: 'background-color: transparent !important;' # TODO: Replace with a ``devilry_transparentpanel`` class

    data: {}

    tpl: """
    <div class="header alert">
        Yo
    </div>

    <div class="container-fluid">
        <div class="row filelisting">
            <div class="span4">
                <ul class="nav nav-tabs nav-stacked">
                    <li><a href="#">helloworld.py</a></li>
                    <li class="active"><a href="#">readme.txt</a></li>
                </ul>
            </div>
            <div class="span8">
                <pre>This is a test</pre>
            </div>
        </div>
    </div>
    """
})
