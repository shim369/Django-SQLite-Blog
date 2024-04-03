# from turtle import title
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class Category(models.Model):
  name = models.CharField('カテゴリー', max_length=50)
  slug = models.SlugField('スラッグ', unique=True, null=True)

  def __str__(self):
      return self.name

class Tag(models.Model):
  name = models.CharField('タグ', max_length=50)
  slug = models.SlugField('スラッグ', unique=True, null=True)

  def __str__(self):
      return self.name

class Article(models.Model):
  title = models.CharField('タイトル', max_length=200, null=True)
  description = models.CharField('説明', max_length=500, null=True)
  content = models.TextField('テキスト')
  article_body = models.CharField('プレーンテキスト', max_length=3000, null=True)
  created_at = models.DateField('作成日', auto_now_add=True)
  updated_at = models.DateField('更新日', auto_now=True)
  slug = models.SlugField('スラッグ',blank=True, unique=False, max_length=255)
  category = models.ForeignKey(
                Category, verbose_name='カテゴリー',
                on_delete=models.PROTECT
              )
  tag = models.ManyToManyField(Tag, verbose_name='タグ')
  thumbnail_image_name = models.CharField('画像用タグ名称', max_length=200, null=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('detail', args=[self.slug])

  def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super(Article, self).save(*args, **kwargs)