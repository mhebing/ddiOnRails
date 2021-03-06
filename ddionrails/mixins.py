"""
Mixins for DDI on Rails.
"""
from django import forms

from ddionrails.helpers import render_markdown


class ModelMixin:
    """
    Default mixins for all classes in DDI on Rails.

    Requires two definition in the ``DOR`` class:

    * io_fields: Fields that are used for the default form and in the default dict.
    * id_fields: Fields that are used for the get_or_create default method.

    Example:

    ::

        from django.db import models
        from ddionrails.mixins import ModelMixin

        class Test(models.Model, ModelMixin):

            name = models.CharField(max_length=255, unique=True)

            class DOR:
                id_fields = ["name"]
                io_fields = ["name"]

    The default value for DOR is:

    ::

        class DOR:
            id_fields = ["name"]
            io_fields = ["name", "label", "description"]

    The ``id_fields`` are also use to construct a default string identifier.
    It is therefore recommended, to order them from the most general to the
    most specific one.

    """

    class DOR:
        id_fields = ["name"]
        io_fields = ["name", "label", "description"]

    @classmethod
    def get_or_create(cls, x, lower_strings=True):
        """
        Default for the get_or_create based on a dict.

        The method uses only relevant identifiers based on ``DOR.id_fields``.

        By default, all strings are set to lower case (option ``lower_strings``).
        """
        definition = {key: x[key] for key in cls.DOR.id_fields}
        for key, value in definition.items():
            if value.__class__ == str and lower_strings:
                definition[key] = value.lower()
        result, created = cls.objects.get_or_create(**definition)
        return result

    @classmethod
    def get(cls, x):
        """
        Default for the get_or_create based on a dict.

        The method uses only relevant identifiers based on ``DOR.id_fields``.
        """
        try:
            definition = {key: x[key] for key in cls.DOR.id_fields}
            result = cls.objects.get(**definition)
        except cls.DoesNotExist:
            result = None
        return result

    @classmethod
    def default_form(cls):
        """
        Creates a default form for all attributes defined in ``DOR.io_fields``.
        """
        class DefaultForm(forms.ModelForm):

            class Meta:
                model = cls
                fields = cls.DOR.io_fields
        return DefaultForm

    def to_dict(self):
        """
        Uses the ``DOR.io_fields`` attribute to generate a default
        dict object for the current instance.
        """
        default_dict = {}
        for field_name in self.DOR.io_fields:
            field = eval("self.%s" % field_name)
            try:
                default_dict[field_name] = field.pk
            except AttributeError:
                default_dict[field_name] = field
        return default_dict

    def title(self):
        """
        Default for the title. It first looks for a valid label, next for a
        valid name, and otherwise returns an empty string.
        """
        try:
            name = self.name
        except AttributeError:
            name = ""
        try:
            label = self.label
        except AttributeError:
            label = ""
        return name if label == "" else label

    def html_description(self):
        """
        Uses the ddionrails Markdown parser (ddionrails.helpers) to render
        the description into HTML.
        """
        try:
            html = render_markdown(self.description)
        except AttributeError:
            html = ""
        return html

    def get_attribute(self, attribute, default=None):
        """
        Example::

            study_id = variable.get_attribute("self.dataset.study.id")
        """
        try:
            return eval(attribute)
        except AttributeError:
            return default

    def string_id(self):
        a = []
        for field_name in self.DOR.id_fields:
            field = eval("self.%s" % field_name)
            try:
                s = field.string_id()
            except AttributeError:
                s = str(field)
            a.append(s)
        a = "/".join(a)
        return a

    def __str__(self):
        return self.string_id()
