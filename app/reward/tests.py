from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
import json

from reward.models import Reward, Product, Funding

User = get_user_model()


def get_dummy_product():
    notebook_list = ['맥북', '그램', '맥북프로', '레노버']

    return [Product.objects.create(
        product_name=f'{notebook}',
        product_type='노트북',
        product_company_name='와디즈주식회사',
        product_img='노트북.jpg',
        product_detail_img='노트북상세.jpg',
        product_start_time='2018-08-15',
        product_end_time='2018-08-20',
        product_cur_amount=100000,
        product_total_amount=2000000,
        product_interested_count=100,
        product_description='2018년 금세기 최고의 노트북',
        product_is_funding='A',
        product_video_url='https://ryanden.kr',
    ) for notebook in notebook_list]


def get_dummy_user():
    return User.objects.create(
        username='a@nasd.com',
        password='1',
        nickname='lock'
    )


def get_dummy_funding():
    return Funding.objects.create(
        user=get_dummy_user(),
        username='홍길동',
        phone_number='01012341234',
        address1='서울',
        address2='강남',
        comment='경비실로',
    )


def get_dummy_reward():
    products = []

    funding = get_dummy_funding()

    for product in get_dummy_product():

        for num in range(5):
            reward = Reward.objects.create(
                reward_name=f'얼리버드{num}',
                reward_option='블루',
                reward_price=30000,
                reward_shipping_charge=2500,
                reward_expecting_departure_date='2018.08.08',
                reward_total_count=100,
                reward_sold_count=5,
                reward_on_sale=True,
                product=product,
                # funding=funding
            )
            products.append(reward)
    return products


class RewardListTest(APITestCase):
    URL = '/api/rewards/'

    def test_prodcut_list_status_code(self):
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_count(self):
        get_dummy_reward()
        response = self.client.get(self.URL)

        data = json.loads(response.content)

        self.assertEqual(len(data), Product.objects.count())

    # def test_product_list(self):
    #     for product in get_dummy_product():
    #         print(product)

    # def test_funding_list(self):
    #     reward = get_dummy_reward()
    #
    #
    #
    #     self.assertEqual(funding)
