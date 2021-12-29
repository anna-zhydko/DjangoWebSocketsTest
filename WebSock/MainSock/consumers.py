import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WidgetConsumer(WebsocketConsumer):

    def connect(self):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self.scope['user'])
        self.group_name = self.scope['url_route']['kwargs']['widget_id']

        # Close connection if widget isn`t in DB
        # try:
        # WidgetCustomization.objects.get(id=self.group_name)
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        # except:
        #     self.close()

    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive widget properties from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        properties = text_data_json['properties']

        # Send widget properties to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'group_mailing',
                'properties': properties,
                'sender_channel_name': self.channel_name
            }
        )

    # Receive properties from group
    def group_mailing(self, event):
        properties = event['properties']
        print('group_mailing')
        if self.channel_name != event['sender_channel_name']:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'properties': properties
            }))
