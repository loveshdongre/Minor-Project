from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20)
    course = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sem = models.CharField(max_length=5)
    branch = models.CharField(max_length=15)
    status = models.CharField(max_length=10)
    res_des = models.CharField(max_length=20)
    sgpa = models.DecimalField(max_digits = 5, decimal_places = 2) 
    res_type = models.CharField(max_length=5)

    def __str__(self):
        return self.student.name + " " + str(self.sgpa)

class ResType(models.Model):
    position = models.IntegerField()
    roll_no = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    sgpa = models.DecimalField(max_digits = 5, decimal_places = 2) 
    res_des = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    
    def __init__(self, position, name, roll_no, sgpa, res_des, status):
        self.position = position
        self.roll_no = roll_no
        self.name = name
        self.sgpa = sgpa
        self.res_des = res_des
        self.status = status
