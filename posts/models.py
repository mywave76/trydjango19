from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(
    	                      upload_to=upload_location,
    	                      null=True,
    	                      blank=True,
    	                      height_field="hight_field",
    	                      width_field="width_field"
    	                      )
    hight_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
    	return reverse("posts:detail", kwargs={"id": self.id})
    	#return "/posts/%s/" %(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]