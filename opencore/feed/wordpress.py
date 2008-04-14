import feedparser
import urllib2

from Products.CMFCore.utils import getToolByName
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.base import FeedItemResponses
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from opencore.interfaces import IProject
from zope.component import adapts
from zope.component import createObject
from zope.interface import implements

class WordpressFeedAdapter(BaseFeedAdapter):
    """feed for recent wordpress blogs"""
    # XXX this should not be used if the project has no blog

    implements(IFeedData)
    adapts(IProject)

    title = 'Blog'

    def is_project_member(self):
        project = self.context
        membertool = getToolByName(project, 'portal_membership')
        mem_id = membertool.getAuthenticatedMember().getId()
        team_ids = project.getTeams()[0].getActiveMemberIds()
        return mem_id in team_ids

    @property
    def link(self):
        return '%s/blog' % self.context.absolute_url()

    @property
    def items(self, n_items=5):
        items = []

        # without the trailing slash, one gets different results!
        # see http://trac.openplans.org/openplans/ticket/2197#comment:3
        uri = '%s/blog/feed/' % self.context.absolute_url()

        # pull down the feed with the proper cookie
        req = urllib2.Request(uri)
        cookie = self.context.REQUEST.get_header('Cookie')
        if cookie:
            req.add_header('Cookie', cookie)
        try:
            feed = urllib2.urlopen(req).read()
        except urllib2.HTTPError:
            # fail silently for now
            feed = ''

        # parse with feedparser
        feed = feedparser.parse(feed)
        # feedparser takes care of HTML sanitization:
        # http://www.feedparser.org/docs/html-sanitization.html
        
        try:
            title = feed.feed.title
        except AttributeError:
            # this means the uri is not a feed (or something?)
            return

        # maybe this should be done after comments?
        # feed.entries.sort(key=date_key) # they appeared sorted already?
        feed.entries = feed.entries[:n_items]

        for entry in feed.entries:
            n_comments = int(entry.get('slash_comments', 0))

            if n_comments:
                response = FeedItemResponses(n_comments,
                                             entry.comments,
                                             'comment')
            else:
                response=None

            title = entry.title
            if not title.strip():
                title = entry.summary

            feed_item = createObject('opencore.feed.feeditem',
                                     title,
                                     entry.summary,
                                     entry.link,
                                     entry.author,
                                     entry.date,
                                     responses=response)

            items.append(feed_item)
        return items
