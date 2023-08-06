from uuid import uuid4

import pytest
from mock import MagicMock, patch

from pyzeebe.credentials.camunda_cloud_credentials import \
    CamundaCloudCredentials
from pyzeebe.errors import (InvalidCamundaCloudCredentialsError,
                            InvalidOAuthCredentialsError)


def test_init():
    client_id = str(uuid4())
    client_secret = str(uuid4())
    cluster_id = str(uuid4())

    with patch("pyzeebe.credentials.oauth_credentials.OAuthCredentials.__init__") as init:
        CamundaCloudCredentials(client_id, client_secret, cluster_id)
        init.assert_called_with(url=f"https://login.cloud.camunda.io/oauth/token", client_id=client_id,
                                client_secret=client_secret, audience=f"{cluster_id}.zeebe.camunda.io")


def test_invalid_credentials():
    CamundaCloudCredentials.get_access_token = MagicMock(
        side_effect=InvalidOAuthCredentialsError(str(uuid4()), str(uuid4()), str(uuid4())))

    with pytest.raises(InvalidCamundaCloudCredentialsError):
        CamundaCloudCredentials(str(uuid4()), str(uuid4()), str(uuid4()))
