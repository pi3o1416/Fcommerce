
from operator import __and__
from functools import reduce
from django.utils.translation import gettext_lazy as _
from django.db.models import CharField, Q, QuerySet, TextField


class TemplateQuerySet(QuerySet):
    def filter_with_related_fields(self, request, related_fields: list):
        """
        Filter objects with foreign key references.
        """
        # Default filter
        filtered_tasks = self.filter_from_query_params(request=request)
        # Filter for foreignkey relation
        for field in get_model_foreignkey_fields(self.model):
            FieldModel = field.remote_field.model
            field_name = field.name
            if field_name in related_fields:
                filtered_tasks = self.select_related(field_name).filter_from_query_params(
                    request=request,
                    FieldModel=FieldModel,
                    related_field=field_name
                )
        return filtered_tasks

    def filter_from_query_params(self, request, FieldModel=None, related_field=None):
        """
        Filter queryset from request query parameters.
        Parameter:
            request         : Request object
            related_field   : field_name of Foreign Key field.(None if not filter in )
            Model           : Model of related_field.(If filter in related field)
        Return:
            Filtered queryset
        """
        assert not ((related_field is not None) ^ (FieldModel is not None)), "If related_field is True, Provide a Model."
        if not FieldModel:
            FieldModel = self.model
        q_objects = generate_q_objects_from_query_params(FieldModel, request, related_field)
        if q_objects:
            return self.filter(reduce(__and__, q_objects))
        return self.all()


def generate_q_objects_from_query_params(ModelName, request, related_field=None):
    """
    Generate q_object from query_params
    Parameter:
        ModelName   : Model that fields should be filtered
        request     : Request object.
        related_fields: related field name if filter occure on a related field.
    Return:
        q_object list
    """
    query_params = request.query_params
    fields = {field.name: field for field in ModelName._meta.fields}
    q_objects = []
    for param, value in query_params.items():
        if related_field:
            splited_param = param.split('.')
            if len(splited_param) == 2 and splited_param[0] == related_field and splited_param[1]:
                param = splited_param[1]
            else:
                continue
        if param in fields.keys():
            q_object = get_q_object(fields=fields, field=param, value=value, related_field=related_field)
            q_objects.append(q_object)
    return q_objects


def get_q_object(fields, field, value, related_field=None):
    """
    Return a single Q object based on field type
    Parameter:
        fields      : List of all fields
        field       : Perticular field that Q object should be generated
        value       : Value that will be used on filter
        related_field: Related field name if filter occure on a realted field.
    Return:
        One Q object
    """
    if isinstance(fields[field], CharField) or isinstance(fields[field], TextField):
        return _get_textdata_q_object(field=field, value=value, related_field=related_field)
    else:
        return _get_default_q_object(field=field, value=value, related_field=related_field)


def _get_textdata_q_object(field, value, related_field=None):
    """
    Generate q object for TextField and CharField
    Parameter:
        fields      : List of all fields
        field       : Perticular field that Q object should be generated
        value       : Value that will be used on filter
        related_field: Related field name if filter occure on a realted field.
    Return:
        One Q object
    """
    if related_field:
        return Q(('{}__{}__icontains'.format(related_field, field), value))
    return Q(('{}__icontains'.format(field), value))


def _get_default_q_object(field, value, related_field=None):
    """
    Generate simple Q object with direct comparison
    Parameter:
        fields      : List of all fields
        field       : Perticular field that Q object should be generated
        value       : Value that will be used on filter
        related_field: Related field name if filter occure on a realted field.
    Return:
        One Q object
    """
    if related_field:
        return Q(('{}__{}'.format(related_field, field), value))
    return Q((field, value))


def get_model_foreignkey_fields(ModelName):
    for field in ModelName._meta.fields:
        if field.remote_field:
            yield field
