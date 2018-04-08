import logging
import django
from rest_framework import exceptions
from rest_framework.permissions import BasePermission

from user_management import strings



log = logging.getLogger(__name__)
############################################################################################################################
# PERMISSION CLASSES

# Permission classes for all requests
# Delete, list, create, retrive, update, partialupdate

class IsDeleteRequest(BasePermission):
    """
    Returns true if it is a DELETE request.
    """
    def has_permission(self, request, view):
        flag = False
        if (request.method == "DELETE"):
            flag = True
        return flag

class IsListRequest(BasePermission):
    """
    Returns true if it is a list request.
    """
    def has_permission(self, request, view):

        flag = False
        if (view.action == "list"):
            flag = True
        # print "view.action" , view.action
        return flag

class IsCreateRequest(BasePermission):
    """
    Returns true if it is a create request.
    """
    def has_permission(self, request, view):
        print "view.action" , view.action
        flag = False
        if (view.action == "create"):
            flag = True

        # print "\create request."       
        # print "flag:"  , flag
        return flag

class IsRetrieveRequest(BasePermission):
    """
    Returns true if it is a retrieve request.
    """
    def has_permission(self, request, view):

        flag = False
        if (view.action == "retrieve"):
            flag = True

        #print "\nretrieve request."       
        #print "flag:"  , flag
        #print "view.action:" , view.action
        return flag

class IsUpdateRequest(BasePermission):
    """
    Returns true if it is a update request.
    """
    def has_permission(self, request, view):

        flag = False
        if (view.action == "update"):
            flag = True

        # print "\nupdate request."       
        # print "flag:"  , flag
        return flag

class IsPartialupdateRequest(BasePermission):
    """
    Returns true if it is a partial_update request.
    """
    def has_permission(self, request, view):

        flag = False
        if (view.action == "partial_update"):
            flag = True

        #print "\n partial update request."       
        #print "flag:"  , flag
        return flag  

class IsAdmin(BasePermission):
    """
    Returns true if user is a super_user or admin.
    """
    def has_permission(self, request, view):
        flag = False
        designation = request.user.designation
        if (designation == strings.ADMIN):
            flag = True
        else:
            # Raising exceptions here to override default message "You do not have permission to perform this action."
            raise exceptions.PermissionDenied(detail= strings.ACCESS_DENIED_GROUP)
        log.debug("IsAdmin Class: Flag:" + str(flag))
        return request.user and flag

class IsAuthenticated(BasePermission):
    """
    Returns true if user exist and authenticated properly.
    """
    def has_permission(self, request, view):

        #Check for authenticated user
        flag = False
        if django.VERSION < (1, 10):
            flag = request.user.is_authenticated()
        else:
            flag = request.user.is_authenticated

        if (flag and request.user.is_active == False):
            raise exceptions.PermissionDenied(detail= strings.USER_INACTIVATED)

        return request.user and flag
############################################################################################################################