from django.db import models
from django.db.models import Q
from django.utils.timezone import now

class ConnectionManager(models.Manager):
    def received_requests(self, id):
        return self.filter(receiver_seeker_id=id).filter(is_requested=True)

    def sent_requests(self, id):
        return self.filter(sender_seeker_id=id).filter(is_requested=True)
    
    def view_friends(self, id):
        return self.filter(Q(sender_seeker_id=id) | Q(sender_seeker_id=id)).filter(is_accepted=True)
        

class Connections(models.Model):
    # sender_seeker=models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="sender")
    # receiver_seeker=models.ForeignKey("accounts.User",  on_delete=models.CASCADE)
    is_requested=models.BooleanField(default=True)
    is_accepted=models.BooleanField(default=False)
    request_date=models.TimeField(default=now)
    accept_date=models.TimeField()

    objects=ConnectionManager()

class FollowingManager(models.Manager):
    def followings(self, id):
        return self.filter(sender_seeker_id=id)
        
class Following(models.Model):
    # sender_seeker=models.ForeignKey("accounts.Seeker", on_delete=models.CASCADE)
    # organization=models.ForeignKey("accounts.Organization", on_delete=models.CASCADE)

    objects=FollowingManager()
    

class Blog(models.Model):
    # user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    body = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        return '{}: {}'.format(self.user, self.title)

class ReplyToBlog(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    reply = models.CharField(max_length = 125)


    def __str__(self):
        return '{}: {}'.format(self.blog, self.user)


class SavedBlogs(models.Model):
    # user=models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    blogId=models.ForeignKey(Blog,on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.user.email)

class Feed(models.Model):
    # user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    body = models.CharField(max_length=125)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.title)

class SavedFeed(models.Model):
    # user=models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    feedId=models.ForeignKey(Feed,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.user.email)

class ReplyToFeed(models.Model):
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    reply = models.CharField(max_length = 125)

    def __str__(self):
        return '{}: {}'.format(self.blog, self.user)