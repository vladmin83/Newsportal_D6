from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        newRat = self.new_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += newRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser.username}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['-ratingAuthor']


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='категория')
    discription = models.TextField(null=True, blank=True, verbose_name='описание')
    subscribers = models.ManyToManyField(User, through='CategoryToUser')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class CategoryToUser (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{user}: {category}'.format(user=self.subscribers, category=self.category)


class New(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = "AR"
    CATEGORY_CHOICES = (
        (NEWS, "Новость"),
        (ARTICLE, "Статья")
    )
    newCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    title = models.CharField(max_length=128, verbose_name='заголовок')
    text = models.TextField(null=True, blank=True, verbose_name='текст публикации')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.text[:20]}, {self.newCategory}, {self.id}'


    def get_absolute_url(self):
        return f'/news/{self.id}'
        #return reverse('detail', kwargs={'pk': self.pk})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def date(self):
        return f'{self.dateCreation.strftime("%d.%m.%Y")}'


    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-dateCreation']


class Comment(models.Model):
    commentNew = models.ForeignKey(New, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentNew.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-dateCreation']

