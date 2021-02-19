import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class ActivateUser(GenericAPIView):

    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}

        # url = '{0}://{1}{2}'.format(settings.PROTOCOL, settings.DOMAIN, reverse('user-activate'))
        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())
