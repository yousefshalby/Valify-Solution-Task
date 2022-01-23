from django.test import TestCase
from django.urls import reverse, resolve
from polls.views import GetPolls, VotePolls


class PollUrlsTestCase(TestCase):
    def test_get_polls_url_resolves(self):
        """
            set Up : we are calling url list all polls
            result : returning the correct view for the url
        """
        url = reverse('poll:list')
        self.assertEquals(resolve(url).func.view_class, GetPolls)

    def test_create_vote_url_resolves(self):
        """
                set Up : we are the url create vote url
                result : returning the correct view for the url
        """
        url = reverse('poll:post-vote', args=[1])
        self.assertEquals(resolve(url).func.view_class, VotePolls)
