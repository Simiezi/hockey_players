from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin, HitCount


class Player(models.Model, HitCountMixin):
    first_name = models.CharField(max_length=100, default='Имя')
    last_name = models.CharField(max_length=100, default='Фамилия')
    date_of_birth = models.DateField()
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=200)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    player_photo = models.ImageField(upload_to='player_images/')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return reverse('plr:player_detail',
                       args=[self.slug])

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        # img = Image.open(self.player_photo.path)
        # if img.height > 512 or img.width > 512:
        #     output_size = (512, 512)
        #     img.thumbnail(output_size)
        #     img.save(self.player_photo.path)
        if not self.slug:
            self.slug = slugify(self.first_name + ' ' + self.last_name)
        super().save(*args, **kwargs)


class Comment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)