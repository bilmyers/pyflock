import json
import jwt
from token_verifier_filter import TokenVerifierFilter
from utils import send_200_response, send_403_response, send_404_response


class Event(object):
    def __init__(self, dictionary):
        self.__dict__ = json.loads(dictionary)


class EventHandlerClient(object):
    def __init__(self, app_secret, app_id):
        self.app_secret = app_secret
        self.app_id = app_id
        self.defineEventHandlers()

    def defineEventHandlers(self):
        self.on_app_install = None
        self.on_app_uninstall = None
        self.on_chat_generate_url_preview = None
        self.on_chat_receive_message = None
        self.on_client_flockml_action = None
        self.on_client_open_attachment_widget = None
        self.on_client_press_button = None
        self.on_client_slash_command = None
        self.on_client_widget_action = None

    @staticmethod
    def send_response(handler, event, start_response):
        if handler is not None:
            try:
                body = handler(event)
                send_200_response(start_response)
                return body
            except:
                send_403_response(start_response)
                return {}
        else:
            send_404_response(start_response)
            return {}

    def handle(self, environ, start_response):

        if 'event_token_payload' not in environ:
            try:
                payload, event_json = TokenVerifierFilter.decode_and_verify_request(environ,
                                                                                    self.app_secret,
                                                                                    self.app_id)
                event = Event(event_json)
            except jwt.DecodeError:
                send_403_response(start_response)
                return {}
        else:
            payload, event = environ['event_token_payload'], Event(environ['request_body'])

        if event.name == "app.install":
            return EventHandlerClient.send_response(self.on_app_install, event, start_response)
        elif event.name == "app.uninstall":
            return EventHandlerClient.send_response(self.on_app_uninstall, event, start_response)
        elif event.name == "chat.generateUrlPreview":
            return EventHandlerClient.send_response(self.on_chat_generate_url_preview, event, start_response)
        elif event.name == "chat.receiveMessage":
            return EventHandlerClient.send_response(self.on_chat_receive_message, event, start_response)
        elif event.name == "client.flockmlAction":
            return EventHandlerClient.send_response(self.on_client_flockml_action, event, start_response)
        elif event.name == "client.openAttachmentWidget":
            return EventHandlerClient.send_response(self.on_client_open_attachment_widget, event, start_response)
        elif event.name == "client.pressButton":
            return EventHandlerClient.send_response(self.on_client_press_button, event, start_response)
        elif event.name == "client.slashCommand":
            return EventHandlerClient.send_response(self.on_client_slash_command, event, start_response)
        elif event.name == "client.widgetAction":
            return EventHandlerClient.send_response(self.on_client_widget_action, event, start_response)
        else:
            raise Exception("Unknown event encountered" + event.name)
