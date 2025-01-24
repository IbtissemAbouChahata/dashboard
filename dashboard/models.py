from django.db import models

class EnvironmentalData(models.Model):
    day = models.DateField(primary_key=True)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    current = models.IntegerField()
    voltage = models.IntegerField()
    luminosity = models.IntegerField()

    def __str__(self):
        return f"{self.day}: {self.temperature}°C, {self.humidity}%, {self.current}A, {self.voltage}V, {self.luminosity}lm"
class Meta:
        db_table = 'environmental_data' 