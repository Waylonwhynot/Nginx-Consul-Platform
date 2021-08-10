import json
import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from nginx_platform_backend.libs.permissions import redis_storage_permissions


class UserLock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '用户已被锁定,请联系管理员'
    default_code = 'not_authenticated'


class RbacPermission(BasePermission):
    """
    自定义权限认证
    """

    @staticmethod
    def pro_uri(uri):
        base_api = settings.BASE_API
        uri = '/' + base_api + '/' + uri + '/'
        return re.sub('/+', '/', uri)

    def has_permission(self, request, view):
        # 验证用户是否被锁定
        if not request.user.is_active:
            raise UserLock()
        request_url = request.path
        print('请求的路径是------:  {}\n请求的方法是{}'.format(request_url,request.method))
        # 如果请求url在白名单，放行
        for safe_url in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=safe_url), request_url):
                print('请求url在白名单，放行')
                return True
        # admin权限放行
        conn = get_redis_connection('user_info')
        if not conn.exists('user_permissions_manage'): # 如果redis中没有用户权限表，则从数据库中获取所有权限并且存储到redis中
            redis_storage_permissions(conn)
        if conn.exists('user_info_%s' % request.user.id):
            user_permissions = json.loads(conn.hget('user_info_%s' % request.user.id, 'permissions').decode())
            # 根据user_id获取当前用户权限，如果是admin 放行
            if 'admin' in user_permissions:
                return True
        else:
            user_permissions = []
            print(request.user.roles.values_list('name', flat=True)) # 用户对应的角色名，如果是系统管理员，则放行
            if '系统管理员' in request.user.roles.values_list('name', flat=True):
                return True
        # RBAC权限验证
        # Step 1 验证redis中是否存储权限数据
        request_method = request.method
        # Step 2 判断请求路径是否在权限控制中
        url_keys = conn.hkeys('user_permissions_manage')
        # print('所有权限key值',url_keys)
        for url_key in url_keys: # 遍历权限列表返回匹配到的权限 key值 形式为"/api/system/org/"
            # print(settings.REGEX_URL.format(url=self.pro_uri(url_key.decode())))
            if re.match(settings.REGEX_URL.format(url=self.pro_uri(url_key.decode())), request_url):
                redis_key = url_key.decode()
                break
        else:
            print('11111111111111111111')
            return True # 匹配不到代表没有做权限限制，放行
        # Step 3 redis权限验证
        permissions = json.loads(conn.hget('user_permissions_manage', redis_key).decode())
        # 返回匹配到的权限key值 对应的values [{},{}...]
        # method_hit = False  # 同一接口配置不同权限验证
        for permission in permissions:
            if permission.get('method') == request_method:
                # method_hit = True
                if permission.get('sign') in user_permissions: # 如果权限标识 在 获取到的用户权限表中放行
                    print('222222222222222222')
                    return True
            print('结束权限判断')
        # else:
        #     if method_hit:
        #         print('33333333333333333')
        #         return False
        #     else:
        #         print('finally')
        #         return True
