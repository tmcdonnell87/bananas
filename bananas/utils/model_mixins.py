from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_choice_field_display(self, field, field_value=None):
        try:
            class_field = self.__class__._meta._forward_fields_map[field]
        except KeyError:
            raise Exception('{} not in {}'.format(
                field, self.__class__.meta.object_name))
        field_value = field_value or vars(self).get(field)
        for choice in class_field.choices:
            if choice[0] == field_value:
                return choice[1]
        return ''
