from opencore.feed.base import BaseFeedAdapter
import doctest
import unittest

BaseFeedAdapter.memberURL = lambda x, y: 'http://www.openplans.org'
BaseFeedAdapter.member_portraitURL = lambda x, y: 'http://www.openplans.org/++resource++img/topp_logo.jpg'

class DummyContext(object):
    def Title(self):
        return 'Dummy title'
    def Description(self):
        return 'Dummy description'
    def absolute_url(self):
        return 'http://dummy/context/url'
    def getPhysicalPath(self):
        return ['dummy', 'context', 'url']
    def modified(self):
        from datetime import datetime
        return datetime.now()
    def Creator(self):
        return 'Dummy creator'

def test_suite():
    base_suite = doctest.DocFileSuite('base.txt',
                                      optionflags=doctest.ELLIPSIS)
    people_suite = doctest.DocFileSuite('people.txt',
                                        optionflags=doctest.ELLIPSIS)
    projects_suite = doctest.DocFileSuite('projects.txt',
                                          optionflags=doctest.ELLIPSIS)
    project_suite = doctest.DocFileSuite('project.txt',
                                         optionflags=doctest.ELLIPSIS)
    page_suite = doctest.DocFileSuite('page.txt',
                                      optionflags=doctest.ELLIPSIS)
    return unittest.TestSuite((base_suite,
                               people_suite,
                               projects_suite,
                               project_suite,
                               page_suite,
                               ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
