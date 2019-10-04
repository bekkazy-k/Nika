from Nika import nika, util


class Handler(nika.Nika):

    def pre_process_data(self, message):
        return util.marshall(message)

    def post_process_data(self, message):
        for i in message:
            # Some action
            print(i)
        return message
