from django.db import models
from django.core.urlresolvers import reverse


def upload_location(instance, filename):
    #filebase, extention = filename.split(".")
    #return "%s/%s.%s" % (instance.id, instance.id, extention)
    return "%s/%s" % (instance.id, filename)


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field="height_field",
                              width_field="width_field")
    # class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)[source]
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    content = models.TextField()
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})
        # return "/posts/%s/" %(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]
