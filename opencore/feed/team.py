from opencore.configuration import DEFAULT_ROLES
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from opencore.interfaces import IOpenTeam
from opencore.interfaces import IProject
from opencore.member.utils import profile_path
from Products.CMFCore.utils import getToolByName
from topp.utils.pretty_date import prettyDate
from zope.component import adapts
from zope.component import getUtility
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

def portrait_sort_key(member):
    """sorting function for member display by portrait"""
    return member.has_portrait()


class TeamFeedAdapter(BaseFeedAdapter):
    implements(IFeedData)
    adapts(IProject)

    title = 'Team'

    @property
    def link(self):
        return '%s/team' % self.context.absolute_url()


    @property
    def items(self, n_items=12):
        
        items = []
        members = list(self.context.projectMembers())
        project = self.context

        # XXX should probably go in Products.Openplans' project
        # maybe related to docstring above while filtering by hand is necessary?
        team = project.getTeams()[0]
        wf = getToolByName(project, 'portal_workflow')
        members = [ member for member in members 
                    if wf.getInfoFor(team.getMembershipByMemberId(member.id), 'review_state') == 'public' ]

        members.sort(key=portrait_sort_key, reverse=True) # could also sort by admin-ness, lastlogin, etc
        members = members[:n_items]

        for member in members:
            link = profile_path(member.id)
            feed_item = createObject('opencore.feed.feeditem',
                                     member.id,
                                     member.fullname,
                                     link,
                                     member.id,
                                     member.Date())

            items.append(feed_item)
        return items
