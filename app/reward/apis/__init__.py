from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, filters
from rest_framework.response import Response

from ..models import Product, Reward, ProductLike, Funding
from ..serializer import ProductSerializer, RewardSerializer, ProductDetailSerializer, ProductFundingSerializer, \
    ProductLikeSerializer, FundingSerializer, IncreaseProductCountSerializer
from utils.paginations import ProductListPagination

User = get_user_model()


# DB 에서 Product 모든 정보를 요청한다.
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination


# Product 의 검색기능.
class ProductCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('product_interested_count', 'product_cur_amount', 'product_start_time', 'product_end_time')

    def get_queryset(self):
        category = self.request.query_params.get('category', '')
        product_name = self.request.query_params.get('product_name', '')
        is_funding = self.request.query_params.get('is_funding', 'A')

        return Product.objects.filter(product_type__contains=category, product_name__contains=product_name,
                                      product_is_funding__contains=is_funding)


# 좋아하는 Product 리스트를 요청한다.
class ProductLikeList(generics.ListAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer


# 펀딩한 리워드 정보를 요청한다. (장바구니)
class FundingList(generics.ListAPIView):
    queryset = Funding.objects.all()
    serializer_class = FundingSerializer


# 펀딩 페이지에서 불필요한 리워드 정보를 배제하고 펀딩에 필요한 리워드 정보 요청한다.
class ProductFundingList(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFundingSerializer


# 리워드 정보를 요청한다.
class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


# Product 의 Detail 페이지에 관한 정보를 요청한다.
# object 한개를 가져 올때는 generics.RetrieveAPIView 를 사용, CRUD 가능
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# 작명 (Api view 를 뒤에 추가 )
class ProductLikeCreate(generics.ListCreateAPIView):
    pass


# 좋아요를 누를때마다 좋아요 갯수가 오른다.
class IncreaseInterestedCount(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = IncreaseProductCountSerializer

            return serializer_class

        return serializer_class

    def patch(self, request, *args, **kwargs):
        product_pk = self.request.data.get('pk')

        product = Product.objects.get(pk=product_pk)

        product.product_interested_count += 1

        product.save()

        serializer = self.get_serializer_class()(product)

        return Response(serializer.data)
