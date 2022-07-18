from rest_framework import serializers
from invest.models import IdeasConnection,savedIdeas

class IdeasSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeasConnection
        # fields = [
        #     'id',
        #     'title',
        #     'description',
        #     'open_invester',
        #     'open_collaboration',
        #     'department_types',
        #     'patent_no',
        #     'serial_no',
        #     'timestamp',
        # ]
        fields = '__all__'

class SavedIdeasSerializers(serializers.ModelSerializer):
    class Meta:
        model=savedIdeas
        fields='__all__'
