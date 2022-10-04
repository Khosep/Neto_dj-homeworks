import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from students.filters import CourseFilter
from students.models import Course


@pytest.fixture
def api_client():
    """Фикстура для клиента API"""
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)
    return factory


@pytest.mark.django_db
def test_courses_retrieve(api_client, course_factory):
    pattern = 'second'
    base_url = reverse('courses-list')
    names = ('first', 'second', 'third')
    courses = [course_factory(name=name) for name in names]
    course_id = Course.objects.get(name=pattern).id
    url = f'{base_url}?id={course_id}'
    resp = api_client.get(url)
    resp_json = resp.json()
    print(resp_json)
    assert resp.status_code == 200
    assert resp_json[0]['name'] == pattern

@pytest.mark.django_db
def test_courses_list(api_client, course_factory):
    url = reverse('courses-list')
    course_factory(_quantity=2)
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json
    assert len(resp_json) == 2

@pytest.mark.django_db
def test_courses_filter_id(api_client, course_factory):
    pattern ='second'
    base_url = reverse('courses-list')
    names = ('first', 'second', 'third')
    courses = [course_factory(name=name) for name in names]
    course_id = Course.objects.get(name=pattern).id
    url = f'{base_url}?id={course_id}'
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json[0].get('name') == pattern
    assert len(resp_json) == 1

@pytest.mark.django_db
def test_courses_filter_name(course_factory):
    pattern ='second'
    names = ('first', 'second', 'third')
    courses = [course_factory(name=name) for name in names]
    f = CourseFilter(data={'name': pattern})
    assert f.is_valid()
    assert f.qs.count() == 1
    assert f.qs[0].name == pattern

@pytest.mark.django_db
def test_courses_create(api_client):
    count = Course.objects.count()
    url = reverse('courses-list')
    course_data = {'name': 'first'}
    resp = api_client.post(url, course_data)
    assert resp.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_courses_update(api_client, course_factory):
    old_name = 'first'
    pattern = 'test'
    base_url = reverse('courses-list')
    names = ('first', 'second', 'third')
    courses = [course_factory(name=name) for name in names]
    count = Course.objects.count()
    course_id = Course.objects.get(name=old_name).id
    url = f'{base_url}{course_id}/'
    resp = api_client.put(url, data={'name': pattern})
    assert resp.status_code == 200
    assert Course.objects.get(id=course_id).name == pattern
    assert Course.objects.count() == count

@pytest.mark.django_db
def test_courses_delete(api_client, course_factory):
    base_url = reverse('courses-list')
    names = ('first', 'second', 'third')
    courses = [course_factory(name=name) for name in names]
    qset = Course.objects.all()
    count = qset.count()
    course_id = qset.get(name='first').id
    url = f'{base_url}{course_id}/'
    resp = api_client.delete(url)
    assert resp.status_code == 204
    assert Course.objects.count() == count - 1
    with pytest.raises(Course.DoesNotExist):
        Course.objects.get(id=course_id)
