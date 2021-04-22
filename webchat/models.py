from django.db import models
from bbs.models import UserProfile

# Create your models here.


# QQ群
class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    # 群介绍
    brief = models.CharField(max_length=255, blank=True, null=True)
    # 群主
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # 管理员
    admins = models.ManyToManyField(UserProfile, related_name="group_admin")
    # 成员
    members = models.ManyToManyField(UserProfile, blank=True, related_name="group_members")
    max_person = models.IntegerField(default=200)

    def __str__(self):
        return self.name