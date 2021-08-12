from django.db import models
from enum import Enum


class VERBMAP(Enum):
    POST = "POST"
    GET = "GET"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class SOAPRequestLogger(models.Model):
    """
    Logs SOAP requests
    """
    date_sent = models.DateTimeField(auto_now_add=True)
    method = models.CharField(
        max_length=4,
        choices=VERBMAP.choices(),
        default=VERBMAP.POST
    )
    url = models.URLField(max_length=255, null=False)
    headers = models.TextField(blank=True, null=False)
    body = models.TextField(blank=True, null=True)
    request_time_ms = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date_sent} - {self.url} - {self.request_time_ms}"

    class Meta:
        ordering = ('-date_sent',)


class SOAPResponseLogger(models.Model):
    """
    Logs SOAP responses
    """
    date_received = models.DateTimeField(blank=True, null=True)
    request_id = models.ForeignKey(SOAPRequestLogger, on_delete=models.CASCADE)
    status = models.IntegerField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date_received} - {self.request_id} - {self.status}"

    class Meta:
        ordering = ('-date_received',)