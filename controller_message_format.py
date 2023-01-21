import json


class ControllerMessageFormat:
    def __init__(
        self,
        action="",
        data={},
    ):
        self.action = action
        self.data = data
        self.msg = None

    def convertToString(self):
        self.msg = {"action": self.action, "data": self.data}
        self.msg = json.dumps(self.msg)

    def convertToJson(self, messageStr):
        if len(messageStr) > 0:
            self.msg = json.loads(str(messageStr))
            self.action = self.msg["action"]
            self.data = self.msg["data"]
