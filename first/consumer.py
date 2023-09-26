import math
from api import api_call
from api import PAGE_SIZE


class ApiConsumer:
    def __init__(self):
        self.last_item = 0
        self.last_request_page = 0

    def fetch(self, total_items):
        if total_items == 0:
            return []

        data = []

        # Continue fetching data while there are more items to retrieve
        while total_items > 0:
            # Calculate the current page and offset based on the last_item index
            page = self.last_item // PAGE_SIZE
            offset = self.last_item % PAGE_SIZE
            page_data = api_call(page)

            # Check if the page_data is empty or if offset is beyond the length of the page_data
            if not page_data or offset >= len(page_data):
                break

            # Calculate how many items can be retrieved from the current page
            remaining_items = total_items if total_items < len(page_data) - offset else len(page_data) - offset
            data.extend(page_data[offset:offset + remaining_items])
            total_items -= remaining_items
            self.last_item += remaining_items

        return data
    

