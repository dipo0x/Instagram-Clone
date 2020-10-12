from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
app_name='core'
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:journal_list_by_category', args=[self.slug])

class JounalQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        return self.filter(Your_Post_Title__iexact=query)

class JournalManager(models.Manager):
    def get_queryset(self):
        return JounalQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().publised()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

class Journal(models.Model):
    #category = models.ForeignKey(Category, related_name='journals', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Your_Post_Title = models.CharField(max_length=2000)
    slug = models.SlugField(unique=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    Content = models.TextField()
    available = models.BooleanField(default=True)
    Country = models.CharField(max_length=2000)
    Link = models.CharField(max_length=1000)
    likes = models.ManyToManyField(User, related_name='core_journals', blank=True)
    profile_pix = models.ImageField(upload_to='blogpost_images/', blank=True, null=True)
    image = models.ImageField(upload_to='blogpost_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = JournalManager()

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('core:journal-detail', kwargs={'slug': self.slug})    

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type    


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        #comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        return qs

class Comment(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    #journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,help_text="")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True)

    content = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.user.username



    def children(self):
        return Comment.objects.filter(parent=self) 

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True    

           
class SearchQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)