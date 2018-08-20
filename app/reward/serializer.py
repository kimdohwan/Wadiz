from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.serializer import UserSerializer
from reward.models import Product, Reward, ProductLike, Funding

User = get_user_model()


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward

        fields = (
            'pk',
            'reward_name',
            'reward_option',
            'reward_price',
            'reward_shipping_charge',
            'reward_expecting_departure_date',
            'reward_total_count',
            'reward_sold_count',
            'reward_on_sale',
            'reward_amount',
            'product',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            'pk',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_detail_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
            'product_video_url',
            'product_is_funding',

        )


class ProductLikeSerializer(serializers.ModelSerializer):
    liked_product = ProductSerializer(many=True)

    class Meta:
        model = ProductLike

        fields = (
            'pk',
            'user',
            'product',
            'liked_at'
        )


class FundingSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(many=True)
    # user = UserSerializer()

    class Meta:
        model = Funding

        fields = (
            'pk',
            'user',
            'username',
            'phone_number',
            'address1',
            'address2',
            'comment',
            'requested_at',
            'cancel_at',
            'reward'
        )


class ProductDetailSerializer(ProductSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_detail_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
            'product_description',
            'product_video_url',
            'rewards',
        )


class ProductFundingSerializer(RewardSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(RewardSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'rewards',
        )
