from django.test import TestCase, Client, override_settings


class SocialMetaTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_og_tags_present_and_pixel_disabled_by_default(self):
        resp = self.client.get('/')
        html = resp.content.decode()
        self.assertIn('<meta property="og:title"', html)
        self.assertIn('og:image', html)
        self.assertNotIn("fbq('init'", html)

    def test_pixel_renders_when_env_set(self):
        with override_settings(FACEBOOK_PIXEL_ID='TEST_PIXEL'):
            resp = self.client.get('/')
            html = resp.content.decode()
            self.assertIn("fbq('init'", html)
            self.assertIn('TEST_PIXEL', html)
