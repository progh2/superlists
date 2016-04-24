from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

class ItemModeTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')

# Create your tests here.
class SmokeTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')

        self.assertEquals(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        self.assertEquals(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method='POST'

        request.POST['item_text'] = '신규 작업 아이템'
        response = home_page(request)

        self.assertEquals(Item.objects.count(),1)
        new_item = Item.objects.first()
        # 외와 동일한 내용 new_item = Item.objects.all()[0]
        self.assertEquals(new_item.text, '신규 작업 아이템')


    def test_home_page_redirects_after_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'

        request.POST['item_text'] = '신규 작업 아이템'
        response = home_page(request)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'], '/')

    def test_홈페이지는_필요할때만_아이템을_저장해야한다(self): #home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEquals(Item.objects.count(), 0)


    def test_home_page_displays_all_list_itmes(self):
        Item.objects.create(text='함기훈 하나')
        Item.objects.create(text='조성미 둘')
        request = HttpRequest()
        response = home_page(request)

        self.assertIn('함기훈 하나', response.content.decode())
        self.assertIn('조성미 둘', response.content.decode())
#    def test_bad_maths(self):
#        self.assertEquals(1 +1, 4)

