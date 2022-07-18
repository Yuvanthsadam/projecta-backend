from social.models import *
from accounts.models import *


class MutualConnectionService(object):
    def __init__(self, seeker_id, receiver_id):
        self.seeker_id=seeker_id
        self.receiver_id=receiver_id

    def get_friend_list(self, id):
        connection_ids=Connections.objects.view_friends(id=id).values()
        id_list=[]
        for connection_id in connection_ids:
            if connection_id['sender_seeker_id']!=id:
                id_list.append(connection_id['sender_seeker_id'])
            elif connection_id['receiver_seeker_id']!=id:
                id_list.append(connection_id['receiver_seeker_id'])
        return id_list

    def get_mutual_count(self):
        my_list=self.get_friend_list(self.seeker_id)
        receiver_seeker_list=self.get_friend_list(self.receiver_id)
        return len(set(my_list).intersection(set(receiver_seeker_list)))

    def get_mutual_connection_details(self):
        response=[]
        my_list=self.get_friend_list(self.seeker_id)
        receiver_seeker_list=self.get_friend_list(self.receiver_id)
        for id in set(my_list).intersection(set(receiver_seeker_list)):
            seeker=Seeker.objects.get(id=self.seeker_id)
            response.append({
                "id":seeker.id,
                "name":seeker.name,
                "ratings":seeker.rating
            })
        return response
