from Products.CMFCore.utils import getToolByName
from opencore.interfaces.adding import IAddProject
from opencore.interfaces import IProject
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from zope.component import adapts
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

class ProjectsFeedAdapter(BaseFeedAdapter):
    """feed for new projects"""
    
    implements(IFeedData)
    adapts(IAddProject)

    @property
    def items(self):
        cat = getToolByName(self.context, 'portal_catalog')
        #XXX put in max depth 1 to not search subfolders
        for brain in cat(portal_type='OpenProject',
                              sort_on='created',
                              sort_order='descending',
                              sort_limit=10):

            title = brain.Title
            description = brain.Description
            link = brain.getURL()
            pubDate = brain.created

            feed_item = createObject('opencore.feed.feeditem',
                                     title,
                                     description,
                                     link,
                                     pubDate)
            yield feed_item