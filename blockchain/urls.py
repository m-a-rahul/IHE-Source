from django.urls import path
from blockchain.views import GetChain, MineBlock, RetrieveRecords, GainAccess, GetMyPatients

app_name = 'blockchain'

urlpatterns = [
    path('get/', GetChain.as_view(), name="get_chain"),
    path('mine/', MineBlock.as_view(), name="mine_block"),
    path('retrieve/', RetrieveRecords.as_view(), name="retrieve_records"),
    path('gain_access/', GainAccess.as_view(), name="gain_access"),
    path('get_mypatients/', GetMyPatients.as_view(), name="get_my_patients"),
]
