from django.db import models

class Trajectory(models.Model):
    filename = models.CharField('filename', max_length=1024)
    initial_chemical_formula = models.CharField('initial chemical formula', max_length=128)
    num_timesteps = models.IntegerField('num_timesteps')
    time_step_interval = models.FloatField('time step interval')
    total_time = models.FloatField('total time')
    creator = models.CharField(max_length=128)
    timestamp = models.DateTimeField('time of creation')
    short_description = models.CharField("short description", max_length=200)

class Computation(models.Model):
    timestamp = models.DateTimeField('time of calculation')
    class Meta:
        abstract = True

class MdAnalysisCalc(Computation):
    time_steps_sampled = models.CharField("time steps sampled", default='[0, 0, 1]', max_length=128)
    #matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
    trajectory = models.ForeignKey(Trajectory)
    selected_atoms = models.CharField(name = 'selected_atoms', default = 'All',max_length=128)
    class Meta:
        abstract = True

class MeDynamicsCalc(MdAnalysisCalc):
    me_order = models.IntegerField("order", default = 50)
    me_precision = models.IntegerField("precision", default = 0)
    projection_vector = models.CharField("projection vector", max_length=200)
    weights = models.CharField(max_length=50)
    short_description = models.CharField("short description", max_length=200)