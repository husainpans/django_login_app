import logging
from rest_framework import serializers

from user_management.models import Users

log = logging.getLogger(__name__)

class UsersSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id','password','username','email','firstname','lastname')

    def create(self,validated_data):

        try:        
            my_user = Users.objects.create(**validated_data)
            log.debug("validated_data: " + str(validated_data))        
            my_user.set_password(validated_data['password'])            
            my_user.save()
            return my_user
        except Exception as e:
            my_user.delete()
            log.error(str(e))

class UsersSerializerList(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id','username','email','firstname','lastname','designation',)

class UsersSerializerUpdate(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('email','firstname','lastname')
