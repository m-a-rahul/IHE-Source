from django.urls import path
from blockchain.views import GetChain, MineBlock, RetrieveRecords, GainAccess, GetMyPatients, CheckAccess, RequestAccess

app_name = 'blockchain'

urlpatterns = [
    path('get/', GetChain.as_view(), name="get_chain"),
    path('mine/', MineBlock.as_view(), name="mine_block"),
    path('retrieve/', RetrieveRecords.as_view(), name="retrieve_records"),
    path('request_access/', RequestAccess.as_view(), name="request_access"),
    path('gain_access/', GainAccess.as_view(), name="gain_access"),
    path('check_access/', CheckAccess.as_view(), name="check_access"),
    path('get_mypatients/', GetMyPatients.as_view(), name="get_my_patients"),
]
