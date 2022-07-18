from django.db import models
from accounts.models import User

class FeedBack(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)
    suggestion = models.CharField(max_length=255)

    def __str__(self):
        return "{}:{}".format(self.user, self.suggestion)

def upload_directory_path(instance, filename):
    return 'UPLOADS/{0}/{1}'.format(instance.user.email, filename)


class BugReport(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    image = models.FileField(upload_to=upload_directory_path, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)
