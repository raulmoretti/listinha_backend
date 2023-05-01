from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from ..serializers import MyTokenObtainPairSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    """
        _Resumo_
        Classe que define as operações de autenticação de usuários por meio de tokens JWT (JSON Web Token). Esta classe é uma subclasse da classe TokenObtainPairView, que é uma classe do pacote rest_framework_simplejwt, que é um pacote que implementa o padrão JWT para autenticação de usuários. O método permite a criação de dois tokens: um token de acesso e um token de atualização. O token de acesso é um token que expira em um curto período de tempo e é usado para autenticar o usuário em requisições que requerem autenticação. O token de atualização é um token que expira em um longo período de tempo e é usado para atualizar o token de acesso quando este expira. O token de atualização é usado em requisições que requerem autenticação, mas que não são feitas pelo usuário autenticado, como por exemplo, requisições para atualizar o token de acesso.
        
        _Requisições_
        - post (POST) para /token/: Cria um token de acesso e um token de atualização para o usuário. Não requer autenticação.
        - refresh (POST) para /token/refresh/: Atualiza o token de acesso do usuário por meio do token de atualização. Não requer autenticação.

    """
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer 