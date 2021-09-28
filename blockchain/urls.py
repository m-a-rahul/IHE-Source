from django.urls import path
from .views import GetChain, MineBlock, Validate, Consensus

app_name = 'blockchain'

urlpatterns = [
    path('get/', GetChain.as_view(), name="get_chain"),
    path('mine/', MineBlock.as_view(), name="mine_block"),
    path('validate/', Validate.as_view(), name="is_chain"),
    path('replace/', Consensus.as_view(), name="replace_chain"),
]
