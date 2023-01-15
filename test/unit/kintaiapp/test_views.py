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
        self.assertQuerysetEqual(expected, response.context['kintailist'])

    def test_record_edit(self):
        row = Kintai.objects.create(
            u_id=180,
            workingday=datetime(2023, 1, 5),
            begintime=datetime(2023, 1, 5, 9, 00, 00, 000),
            finishtime=None
        )
        edited_date = datetime(2023, 1, 5, 12, 00, 00, 000)
        data = {
                'workingday': '2023-01-05',
                'begintime': '2023-01-05 09:00:00',
                'finishtime': '2023-01-05 12:00:00'
            }
        response = self.client.post(
            reverse('record/edit', kwargs={'pk': row.id}), data=data
        )
        row.refresh_from_db()
        self.assertEqual(edited_date, row.finishtime)
        self.assertEqual(302, response.status_code)
        # redirect to record page
        self.assertEqual('/record', response.url)

    def test_record_delete(self):
        row = Kintai.objects.create(
            u_id=180,
            workingday=datetime(2023, 1, 14),
            begintime=datetime(2023, 1, 14, 9, 00, 00, 000),
            finishtime=None
        )
        response = self.client.post(
            reverse('record/delete', kwargs={'pk': row.id})
        )
        # memo
        # filter: 該当のレコードがなかった場合空のQuerySetを返す
        # get: 該当のレコードがなかった場合エラー(DoesNotExist)返す
        actual = Kintai.objects.filter(id=row.id)
        self.assertEqual(302, response.status_code)
        self.assertEqual(0, len(actual))

