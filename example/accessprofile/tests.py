from django.test import TestCase as _TestCase
from django.test import Client

import unittest
import mock

import re
import json

import os

from django.core.exceptions import ValidationError

import logging

from django.utils.six import text_type, string_types

class TestCase(_TestCase):
    if not hasattr(_TestCase,'assertRegex'):
        assertRegex = _TestCase.assertRegexpMatches
    if not hasattr(_TestCase,'assertNotRegex'):
        assertNotRegex = _TestCase.assertNotRegexpMatches

class TestBase(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User, Group, Permission
        from django.contrib import auth
        from django.contrib.contenttypes.models import ContentType
        from django.db.models import Model
        from someapp.models import SomeObject, SomeChild

        self.user = User.objects.create(username="test",is_active=True,is_staff=True)
        self.user.set_password("test")
        self.user.save()
        self.another = User.objects.create(username="another",is_active=True,is_staff=True)
        self.another.set_password("test")
        self.another.save()
        self.third = User.objects.create(username="third",is_active=True,is_staff=True)
        self.third.set_password("test")
        self.third.save()
        self.fourth = User.objects.create(username="fourth",is_active=True,is_staff=True)
        self.fourth.set_password("test")
        self.fourth.save()
        self.group = Group.objects.create(name="some")
        self.group.save()
        self.other_group = Group.objects.create(name="other")
        self.other_group.save()
        self.some = SomeObject.objects.create(name='some',editor_group=self.group)

        for c in [getattr(auth.models,cn) for cn in dir(auth.models)] + [SomeObject, SomeChild]:
            if isinstance(c,type) and issubclass(c,Model) and not c._meta.abstract and c._meta.app_label in ('auth','someapp'):
                for cc in ['add','change','delete']:
                    self.user.user_permissions.add(
                        Permission.objects.get(
                            content_type=ContentType.objects.get(app_label=c._meta.app_label,model=c._meta.model_name),
                            codename='%s_%s' % (cc,c._meta.model_name),
                        )
                    )
                    self.group.permissions.add(
                        Permission.objects.get(
                            content_type=ContentType.objects.get(app_label=c._meta.app_label,model=c._meta.model_name),
                            codename='%s_%s' % (cc,c._meta.model_name),
                        )
                    )

        self.group.user_set.add(self.third)
        self.other_group.user_set.add(self.fourth)

    def tearDown(self):
        from django.contrib.auth.models import User, Group, Permission
        User.objects.all().delete()
        Group.objects.all().delete()

class DropdownFieldFilterTest(TestBase):
    def test_1_check_dropdown_field_filter(self):
        c = Client()
        c.login(username='third',password='test')
        response = c.get('/admin/someapp/someobject/%s/change/' % self.some.id)
        content = text_type(response.content)
        self.assertEqual(response.status_code,200)
        rx_select = re.compile(r'<select[^>]*class="django-select2 django-select2-heavy"[^>]*>')
        rx_name = re.compile(r'name="([^"]*)"')
        rx_field_id = re.compile(r'data-field_id="([^"]*)"')
        selects = {}
        start = 0
        while 42:
            m = rx_select.search(content,start)
            if not m:
                break
            s = content[m.start():m.end()]
            selects[rx_name.search(s).group(1)] = dict(
                s = s,
                name = rx_name.search(s).group(1),
                field_id = rx_field_id.search(s).group(1),
            )
            start = m.end()
        self.assertEqual(len(selects),2)
        response = c.get('/select2/fields/auto.json?field_id=%s' % selects['editor_group']['field_id'])
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertDictContainsSubset({"results": [{"text": self.group.name, "id": self.group.id }]},content)
        response = c.get('/select2/fields/auto.json?field_id=%s' % selects['viewer_groups']['field_id'])
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertDictContainsSubset({"results": [{"text": self.group.name, "id": self.group.id}]},content)

    def test_2_check_dropdown_field_empty(self):
        c = Client()
        c.login(username='test',password='test')
        response = c.get('/admin/someapp/someobject/add/')
        content = text_type(response.content)
        self.assertEqual(response.status_code,200)
        rx_select = re.compile(r'<select[^>]*class="django-select2 django-select2-heavy"[^>]*>')
        rx_name = re.compile(r'name="([^"]*)"')
        rx_field_id = re.compile(r'data-field_id="([^"]*)"')
        selects = {}
        start = 0
        while 42:
            m = rx_select.search(content,start)
            if not m:
                break
            s = content[m.start():m.end()]
            selects[rx_name.search(s).group(1)] = dict(
                s = s,
                name = rx_name.search(s).group(1),
                field_id = rx_field_id.search(s).group(1),
            )
            start = m.end()
        self.assertEqual(len(selects),2)
        response = c.get('/select2/fields/auto.json?field_id=%s' % selects['editor_group']['field_id'])
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertDictContainsSubset({"results": []},content)
        response = c.get('/select2/fields/auto.json?field_id=%s' % selects['viewer_groups']['field_id'])
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertDictContainsSubset({"results": []},content)
