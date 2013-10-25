from django_notification_framework.endpointregistry import EndpointBase


class ConsoleEndpoint(EndpointBase):
    def send(self):
        print
        print 'Topic: {}'.format(self.message.name)
        print 'Subject: {}'.format(self.message.subject)
        print 'To:'
        print ', '.join([unicode(user) for user in self.receiverUsers])
        print 'Body:'
        print self.message.body
        print '-'*70
