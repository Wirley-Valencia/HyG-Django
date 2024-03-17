from enum import Enum


class OroderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = "PAYED"
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'


choices = [(tag, tag.value) for tag in OroderStatus]
