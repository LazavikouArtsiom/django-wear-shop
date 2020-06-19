from django.db import models


class Contact(models.Model):
    username = models.CharField(max_length=150)
    mail = models.EmailField()
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('time_posted',)
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f'{self.mail} {str(self.time_posted)}'