from django.db import models

# Create your models here.
class Item_list(models.Model):
    Category_name = models.CharField( max_length=15)
    
    def __str__(self):
        return self.Category_name
    


class Items(models.Model):
    Item_name = models.CharField(max_length=25)
    description = models.TextField(blank=False)
    Price = models.IntegerField()
    Category = models.ForeignKey(Item_list,related_name='Name', on_delete=models.CASCADE)
    Image = models.ImageField( upload_to=('Items/'))

    def __str__(self):
        return self.Item_name

class AboutUs(models.Model):
    Description = models.TextField(blank=False)


class Feedback(models.Model):
    User_name = models.CharField(max_length=50)
    Description = models.TextField(blank=False)
    Rating = models.IntegerField()

    def __str__(self):
        return self.User_name


class Booktable(models.Model):
    Name = models.CharField(max_length=50)
    Phone_number = models.IntegerField()
    Email = models.EmailField()
    Total_person = models.IntegerField()
    Booking_date = models.DateField()

    def __str__(self):
        return self.Name
