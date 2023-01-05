from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta
from kintaiapp.models import Kintai


class TestViews(TestCase):

    def setUp(self) -> None:
        # TODO: fixturesに変更予定
        Kintai.objects.create(
            u_id=180,
            workingday=datetime.today(),
            begintime=datetime.now(),
            finishtime=datetime.now() + timedelta(hours=8)
        )

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_record_get(self):
        expected = Kintai.objects.all()
        response = self.client.get(reverse('record'))
        self.assertEqual(response.status_code, 200)
        len(response.context['kintailist'])
        self.assertQuerysetEqual(expected, response.context['kintailist'])

    def test_record_monthly_get(self):
        Kintai.objects.create(
            u_id=180,
            workingday=datetime(2022, 12, 29),
            begintime=datetime(2022, 12, 29, 9, 00, 00, 000),
            finishtime=datetime(2022, 12, 29, 18, 00, 00, 000),
        )
        expected = Kintai.objects.filter(workingday=datetime(2022, 12, 29))
        response = self.client.get(reverse('record/monthly'), {'year': 2022, 'month': 12})
        print("expected: ", expected)
        print("response: ", response.context['kintailist'])
        self.assertQuerysetEqual(expected, response.context['kintailist'])
