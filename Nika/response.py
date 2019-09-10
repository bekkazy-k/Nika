import json

'''
| 1  | TRANSACTION_NAME       | Transaction type is profile created               | String     | Yes |
| 2  | EVENT_ID               | Transaction ID                                    | Number     | Yes |
| 3  | MSISDN                 | MSISDN                                            | String     | Yes |
| 4  | EVENT_TIMESTAMP        | Date and time of the event as created in DMP      | Datetime   | Yes |
| 5  | SOURCE_EVENT_TIMESTAMP | Date and time of the event in the source system   | Datetime   | Yes |
| 6  | SOURCE                 | The source of event                               | String     | Yes |
| 7  | SUBS_KEY/BAN           | The customer number in DWH/DMP                    | Number     | No  |
| 8  | VEON_ID                | The customer id in VEON                           | String(24) | No  |
| 9  | P1                     | Free number parameter                             | Integer    | No  |
| 10 | P2                     | Free numeric parameters                           | Integer    | No  |
| 11 | P3                     | Free string parameter                             | String     | No  |
| 12 | P4                     | Free string parameter                             | String     | No  |
| 13 | P5                     | Free string parameter                             | String     | No  |
| 14 | P6                     | Free string parameter                             | String     | No  |
| 15 | P7                     | Free datetime parameter                           | Datetime   | No  |
| 16 | P8                     | Free numeric parameters                           | numeric    | No  |
| 17 | P9                     | Free numeric parameters                           | numeric    | No  |
| 18 | P10                    | Free datetime parameters                          | Datetime   | No  |
| 19 | Main Balance           | Free numeric parameters                           | numeric    | No  |
| 20 | B1                     | Free numeric parameters                           | numeric    | No  |
| 21 | B2                     | Free numeric parameters                           | numeric    | No  |
| 22 | B3                     | Free numeric parameters                           | numeric    | No  |
| 23 | B4                     | Free numeric parameters                           | numeric    | No  |


{
    "MSISDN": "xxxxxxxxx",
    "TRANSACTION_NAME": "TRIGGER_NAME",
    "EVENT_ID": "1234567890",
    "EVENT_TIMESTAMP": "2018-09-24T13:54:45",
    "SOURCE": "SAMPLE_DATA",
    "SOURCE_EVENT_TIMESTAMP": "2018-09-18T13:30:40",
    "BAN": "xxxxxxxxxxxxx",
    "VEON_ID": "xxxxxxxx",
    "P1": 0,
    "P2": 0,
    "P3": "",
    "P4": "",
    "P5": "",
    "P6": "",
    "P7": "2019-03-07T13:00:00",
    "P8": 0.0,
    "P9": 0.0,
    "P10": "2019-03-10T13:00:00",
    "MAIN_BALANCE": 0.0,
    "B1": 0.0,
    "B2": 0.0,
    "B3": 0.0,
    "B4": 0.0
}

'''


# "SUBS_KEY/BAN": "",  - will be created when create new instance of Responce
class Response:
    def __init__(self, transaction_name=None, event_id=None, msisdn=None, event_timestamp=None,
                 source_event_timestamp=None, source=None, resp_type='ban', resp_val=0):

        if transaction_name is None:
            raise AttributeError("TRANSACTION_NAME are not filled")
        if event_id is None:
            raise AttributeError("EVENT_ID are not filled")
        if msisdn is None:
            raise AttributeError("MSISDN are not filled")
        if event_timestamp is None:
            raise AttributeError("EVENT_TIMESTAMP are not filled")
        if source_event_timestamp is None:
            raise AttributeError("SOURCE_EVENT_TIMESTAMP are not filled")
        if source is None:
            raise AttributeError("SOURCE are not filled")

        # Написано так для сохранения последовательности из примера
        self.responce = {}
        self.responce['TRANSACTION_NAME'] = transaction_name
        self.responce['EVENT_ID'] = event_id
        self.responce['MSISDN'] = msisdn
        self.responce['EVENT_TIMESTAMP'] = event_timestamp
        self.responce['SOURCE_EVENT_TIMESTAMP'] = source_event_timestamp
        self.responce['SOURCE'] = source
        if resp_type == 'ban':
            self.responce['BAN'] = resp_val
        else:
            self.responce['SUBS_KEY'] = resp_val
        self.responce['VEON_ID'] = ""
        self.responce['P1'] = 0
        self.responce['P2'] = 0
        self.responce['P3'] = ""
        self.responce['P4'] = ""
        self.responce['P5'] = ""
        self.responce['P6'] = ""
        self.responce['P7'] = ""  # date
        self.responce['P8'] = 0.0
        self.responce['P9'] = 0.0
        self.responce['P10'] = ""  # date
        self.responce['MAIN_BALANCE'] = 0.0
        self.responce['B1'] = 0.0
        self.responce['B2'] = 0.0
        self.responce['B3'] = 0.0
        self.responce['B4'] = 0.0

    def set_param(self, key, val):
        self.responce[key] = val

    def set(self, key, val):
        try:
            if key not in ('SOURCE', 'BAN', 'SUBS_KEY', 'VEON_ID', 'P1', 'P2', 'P3', 'P4', 'P5',
                           'P6', 'P7', 'P8', 'P9', 'P10', 'MAIN_BALANCE', 'B1', 'B2', 'B3', 'B4'):
                raise NameError("Incorrect parameter for response")

            # String 11
            if key in ('SOURCE', 'SUBS_KEY', 'BAN', 'VEON_ID', 'P3', 'P4', 'P5', 'P6'):
                self.responce[key] = self.nvl(val, '')

            # Integer
            elif key in ('P1', 'P2'):
                self.responce[key] = int(self.nvl(val, 0))

            # Float 7
            elif key in ('P8', 'P9', 'MAIN_BALANCE', 'B1', 'B2', 'B3', 'B4'):
                self.responce[key] = float(self.nvl(val, 0.0))

            # Datetime 4
            elif key in ('P7', 'P10'):
                self.responce[key] = self.nvl(val, '')

        except TypeError as t_err:
            raise TypeError(f'Incorrect type in field. Key: {key} value: {val}.Err: {str(t_err)}')
        except BaseException as b_err:
            raise Exception(f'Cannot set value on response. Key: {key} value: {val}.Err: {str(b_err)}')

    def get_response_obj(self):
        return self.responce

    def get_response_str(self):
        str_res = json.dumps(self.responce, ensure_ascii=False)
        return str_res

    @staticmethod
    def nvl(msg, replace):
        if msg is None:
            return replace
        return msg