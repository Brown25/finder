# src/tracking.py
from datetime import datetime
class Package:
    def __init__(self, tracking_number, tracking_url, support_phone_numbers):
        self.delivered_date = None
        self.promised_date = None
        self.tracking_number = tracking_number
        self.tracking_url = tracking_url
        self.support_phone_numbers = support_phone_numbers
        self.transit_events = []
        self.create_date = None
        self.pickup_date = None
        self.can_reschedule = False

    def add_transit_event(self, timestamp, location):
        self.transit_events.append({
            'timestamp': timestamp,
            'location': location
        })

    def set_delivered_date(self, delivered_date):
        self.delivered_date = delivered_date

    def set_promised_date(self, promised_date):
        self.promised_date = promised_date

    def set_create_date(self, create_date):
        self.create_date = create_date

    def set_pickup_date(self, pickup_date):
        self.pickup_date = pickup_date

    def set_can_reschedule(self, can_reschedule):
        self.can_reschedule = can_reschedule

    def get_info(self):
        return {
            'DeliveredDate': self.delivered_date,
            'PromisedDate': self.promised_date,
            'TrackingNumber': self.tracking_number,
            'TrackingURL': self.tracking_url,
            'SupportPhoneNumbers': self.support_phone_numbers,
            'TransitEvents': self.transit_events,
            'CreateDate': self.create_date,
            'PickupDate': self.pickup_date,
            'CanReschedule': self.can_reschedule
        }


class Label:
    def __init__(self, tracking_number, sender, recipient, address):
        self.tracking_number = tracking_number
        self.sender = sender
        self.recipient = recipient
        self.address = address
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_label_info(self):
        return {
            "tracking_number": self.tracking_number,
            "sender": self.sender,
            "recipient": self.recipient,
            "address": self.address,
            "creation_date": self.creation_date
        }
