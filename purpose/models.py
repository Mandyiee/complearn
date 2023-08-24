from django.db import models

# Create your models here.

class Purpose(models.Model):
    usage = models.CharField(max_length=200,null=True,blank=True)
    tensile_strength = models.DecimalField(decimal_places=3,max_digits=13,null=True,blank=True)
    young_modulus = models.DecimalField(decimal_places=3,max_digits=13,null=True,blank=True)

    class Meta:
        verbose_name = 'Purpose'
        verbose_name_plural = 'Purposes'

    def __str__(self):
        return self.usage
