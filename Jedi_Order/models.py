from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JediManager(models.Manager):
    def get_queryset(self):
        return super(JediManager, self).get_queryset().annotate(padawans_cnt=models.Count('candidate'))

    def can_teach(self):
        return self.get_queryset().filter(padawans_cnt__lte=3)

    def more_than_one(self):
        return self.get_queryset().filter(padawans_cnt__gt=1)


class Jedi(models.Model):
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    objects = models.Manager()
    with_padawans = JediManager()

    def __str__(self):
        return self.name


class CandidateManager(models.Manager):
    def get_queryset(self):
        return super(CandidateManager, self).get_queryset().filter(jedi=None)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    age = models.IntegerField()
    email = models.EmailField()
    jedi = models.ForeignKey(Jedi, null=True, on_delete=models.CASCADE)
    objects = CandidateManager()

    def __str__(self):
        return "{} from {}".format(self.name, self.planet)


class Question(models.Model):
    text = models.TextField()
    right_answer = models.BooleanField()

    def __str__(self):
        return self.text[:20] + "..."


class Answer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()

    class Meta:
        unique_together = (('candidate', 'question'),)


class Challenge(models.Model):
    order = models.OneToOneField(Planet, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)

    def __str__(self):
        return "{} order challenge".format(self.order)
