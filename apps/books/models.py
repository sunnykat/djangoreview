from ..login.models import User
from django.db import models


# Create your models here.
class BookManager(models.Manager):
    def addBooks(self, form_data):
        if not form_data['author'] == 'nothing':
            author=Author.objects.filter(name=form_data['author'])[0]
        else :
            author=Author.objects.create(name=form_data['newauthor'])
        book=Books.objects.create(title=form_data['title'], author=author)
        b_id=Books.objects.get(title=form_data['title'])
        return b_id.id
    def deleteBook(self, s_id):
        Books.objects.get(id=s_id).delete()
        return True
    def addLike(self, user_id, s_id):
        book=self.get(id=s_id)
        user=User.objects.get(id=user_id)
        book.likes.add(user)
        book.save()
        return True

class ReviewManager(models.Manager):
    def addReview(self, form_data, u_id):
        review=Reviews.objects.create(text=form_data['review'], book=Books.objects.get(id=form_data['book']), user=User.objects.get(id=u_id),score=form_data['score'])
        return True
    def deleteReview(self, r_id):
        Reviews.objects.get(id=r_id).delete()
        return True

class Books(models.Model):
    title=models.CharField(max_length=40)
    author=models.ForeignKey('Author', related_name='book_author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=BookManager()

class Author(models.Model):
    name=models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reviews(models.Model):
    text=models.CharField(max_length=150)
    book=models.ForeignKey('Books', related_name='book_review')
    user=models.ForeignKey('login.User', related_name='review_user')
    score=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=ReviewManager()
