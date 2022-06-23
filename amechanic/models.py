from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# profile
# posts
# reviews
#location
class Location(models.Model):
    location_name = models.CharField(max_length= 100)
    
    def save_location(self):
        return self.save()
    def delete_location(self):
        return self.delete()
    @classmethod
    def locations(self):
        locals = Location.objects.all()
        return locals
    
    @classmethod
    def search_location(cls, search_term):
        location = cls.objects.filter(location_name__icontains = search_term)
        return location 
    
    def __str__(self):
        return self.location_name
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'profile')
    username= models.CharField(max_length= 100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    prof_image = models.ImageField(default='default.png', upload_to = 'profiles/')
    bio = models.CharField(max_length= 30, null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True)
    second_name = models.CharField(max_length=40, null=True)
    location = models.ManyToManyField(Location)
    
    @receiver(post_save, sender=User,) 
    def create_profile(sender, instance, created, **kwargs, ):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
  
    
    def __str__(self):
        return f'{self.user.username} Profile'

    
# profile-mech
class Post(models.Model):
    user= models.ForeignKey(Profile, on_delete = models.CASCADE, null=True, related_name="posts")
    name = models.CharField(max_length=50)
    carmodel = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media/posts/')
    contact= models.PositiveIntegerField(default="0")
    pub_date= models.DateTimeField(auto_now_add=True)
    
    def save_post(self):
        return self.save()

    def delete_post(self):
        return self.delete()

    @classmethod
    def get_posts(self):
        all_posts = Post.objects.all()
        return all_posts
 
    def __str__(self):
        return self.description


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    quality_of_work = models.IntegerField(choices=rating, default=0, blank=True)
    punctuality = models.IntegerField(choices=rating, blank=True)
    customer_relations = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    quality_of_work_average = models.FloatField(default=0, blank=True)
    punctuality_average = models.FloatField(default=0, blank=True)
    customer_relations_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'