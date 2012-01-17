"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from checkerboard.community.models import Mentor, Learner
from django.contrib.auth.models import User

class CommunityUserTest(TestCase):
    def test_add_mentor(self):
        """
        Tests that a mentor can be added.
        """
        user = User.objects.create_user("test_mentor", "test_mentor@example.com", "test")
        user.first_name = "First"
        user.last_name = "Last"
        user.save()
        mentor = Mentor.objects.create(user=user)
        self.failUnlessEqual(mentor.user.first_name,"First", "Mentor user's name not First")
        self.failUnlessEqual(user.mentor.pk,mentor.pk, "Mentor primary keys do not match")

    def test_add_learner(self):
        """
        Tests that a learner can be added.
        """
        user = User.objects.create_user("test_learner", "test_learner@example.com", "test")
        user.first_name = "First"
        user.last_name = "Last"
        user.save()
        learner = Learner.objects.create(user=user)
        self.failUnlessEqual(learner.user.first_name,"First", "Learner user's name not First")
        self.failUnlessEqual(user.learner.pk,learner.pk, "Learner primary keys do not match")


