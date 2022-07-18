from social.models import *
from accounts.models import *

class ConnectionService(object):
    def __init__(self, id):
        self.id=id

    def get_connection_count(self):
        count=Connections.objects.view_friends(id=self.id).count()
        return count
    
    def get_connection_details(self):
        connection_ids=Connections.objects.view_friends(id=self.id).values()
        id_list=[]
        for connection_id in connection_ids:
            if connection_id['sender_seeker_id']!=self.id:
                id_list.append(connection_id['sender_seeker_id'])
            elif connection_id['receiver_seeker_id']!=self.id:
                id_list.append(connection_id['receiver_seeker_id'])
        response=[]
        for seeker_id in id_list:
            seeker=Seeker.objects.get(id=seeker_id)
            response.append({
                "id":seeker.id,
                "name":seeker.name,
                "ratings":seeker.rating
            })
        return response