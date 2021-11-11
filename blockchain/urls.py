from django.urls import path
from blockchain.views import GetChain, MineBlock

app_name = 'blockchain'

urlpatterns = [
    path('get/', GetChain.as_view(), name="get_chain"),
    path('mine/', MineBlock.as_view(), name="mine_block"),
]
