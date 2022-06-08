from django.db import models


class Assignment(models.Model):
    creator = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="assignment",
        verbose_name="Criador da tarefa",
        null=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="assignment",
        verbose_name="Categoria",
    )
    task_name = models.CharField("Nome da tarefa", max_length=100)
    description = models.TextField("Descrição da tarefa", blank=True)
    create_day = models.DateField("Dia da criação", auto_now_add=True)
    final_day = models.DateField("Dia da finalização", blank=True, null=True)
    active = models.BooleanField("Tarefa ativa", default=True)

    def __str__(self):
        return f"{self.creator.username} -> {self.task_name}"


class Category(models.Model):
    creator = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="category",
        verbose_name="Criador da categoria",
    )
    name = models.CharField("Nome", max_length=50)
    used = models.IntegerField("Usada", default=0, blank=True)

    def __str__(self):
        return self.name
