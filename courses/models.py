from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from .fields import OrderField
from django.urls import reverse

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Status(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Language(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='coursesinsubject',
                                on_delete=models.CASCADE)
    status = models.ForeignKey(Status,
                                related_name='coursesinstatus',
                                on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language,
                                related_name='coursesinlanguage',)
    courselength = models.DurationField(blank=True,null=True)
    title = models.CharField(
        max_length=200,)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    image = models.ImageField(upload_to='course_main_images', blank=True)
    
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail',
                       args=[self.slug])


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='coursefiles')


class Image(ItemBase):
    file = models.FileField(upload_to='coursecontentimages')

class TextWithImage(ItemBase):
    content = models.TextField()
    file = models.FileField(upload_to='coursecontentimages')

class Video(ItemBase):
    url = models.URLField()
