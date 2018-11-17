from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post
# Create your tests here.

class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
                username = 'testuser',
                email = 'test@email.com',
                password = 'secret',
        )

        self.post = Post.objects.create(
            title = 'A good title',
            body = 'sample body',
            author = self.user,
        )

    def test_string_representation(self):
        post = Post(title = 'A sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolut_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}' , 'A good title' )
        self.assertEqual(f'{self.post.body}', 'sample body'  )
        self.assertEqual(f'{self.post.author}', 'testuser')


    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'sample body')
        self.assertTemplateUsed(response, 'home.html')

    def test_detail_list_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), { 'title' : 'A new Title', 'body' : 'New text', 'author' : self.user })
        self.assertContains( response , 'A new Title')
        self.assertContains( response , 'New text' )
        self.assertEqual(response.status_code, 200)

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args = '1' ), { 'title' : 'Updated Title', 'body' : 'updated text'})
        self.assertEqual(response.status_code, 302 )

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args= '1' ))
        self.assertEqual(response.status_code, 200)

