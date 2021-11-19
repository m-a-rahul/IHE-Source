from django.urls import path
from blockchain.views import GetChain, MineBlock, RetrieveRecords, Consensus

app_name = 'blockchain'

urlpatterns = [
    path('get/', GetChain.as_view(), name="get_chain"),
    path('mine/', MineBlock.as_view(), name="mine_block"),
    path('retrieve/', RetrieveRecords.as_view(), name="retrieve_records"),
    path('consensus/', Consensus.as_view(), name="consensus"),
]
