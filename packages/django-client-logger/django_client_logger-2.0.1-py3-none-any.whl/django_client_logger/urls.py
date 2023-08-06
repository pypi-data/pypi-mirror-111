# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf.urls import url
from django_client_logger.views import LogReceiver


urlpatterns = [
    url(r'log', LogReceiver.as_view(), name='client_log_api')
]
