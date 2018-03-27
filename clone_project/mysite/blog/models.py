from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
#        POSTS
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null= True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


#       COMMENTS

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text


class Mail(models.Model):
    subject = models.CharField(max_length=20)
    message = models.TextField()
    author = models.EmailField()

    def send_email(self):
        if subject and message and author:
            try:
                send_email(subject, message, author, ['marekssj2@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return reverse('about')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
