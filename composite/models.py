from django.db import models
from fibre.models import Fibre
from matrix.models import Matrix
from purpose.models import Purpose
import os,datetime,uuid
# Create your models here.

def get_upload_path(instance, filename):
    today = datetime.date.today()
    return os.path.join('composite', today.strftime("%Y/%m/%d"), filename)

class Composite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    fibre = models.ForeignKey(Fibre,related_name='fibre',on_delete=models.PROTECT)
    matrix = models.ForeignKey(Matrix,related_name='matrix',on_delete=models.PROTECT)
    purpose = models.ForeignKey(Purpose,related_name='purpose',on_delete=models.PROTECT)
    best_tensile_strength = models.FloatField(null=True,blank=True)
    best_young_modulus = models.FloatField(null=True,blank=True)
    best_fibre_percentage = models.FloatField(null=True,blank=True)
    best_matrix_percentage = models.FloatField(null=True,blank=True)
    fibre_percentage_against_tensile_strength = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    matrix_percentage_against_tensile_strength = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    fibre_percentage_against_young_modulus = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    matrix_percentage_against_young_modulus = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    fibre_percentage_against_tensile_strength_young_modulus = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    matrix_percentage_against_tensile_strength_young_modulus = models.ImageField(upload_to=get_upload_path,null=True,blank=True)
    finished = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
        indexes = [
        models.Index(fields=['-id']),
        ]
    def __str__(self):
        return str(self.id)