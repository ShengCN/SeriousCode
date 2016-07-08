
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger

class EffertMsgDispatcher(DirectObject):

    def __init__(self):

        DirectObject.__init__(self)

        self.__eventMessageMap = dict()

    def accept_msg(self, event):

        message = self.__convert_event_to_msg(event)

        if self.__eventMessageMap.has_key(event) is False:

            self.__eventMessageMap[event] = []

        self.__eventMessageMap[event].append(message)

        self.accept(event, self.dispatch_message, [event])

        event += "-up"

        message = self.__convert_event_to_msg(event)

        if self.__eventMessageMap.has_key(event) is False:
            self.__eventMessageMap[event] = []

        self.__eventMessageMap[event].append(message)

        self.accept(event, self.dispatch_message, [event])

        print self.__eventMessageMap

    def dispatch_message(self, event, partMessage = None):

        if self.__eventMessageMap.has_key(event) is False:

            return

        msgs = self.__eventMessageMap[event]

        if partMessage == None:

            for msg in msgs:

                messenger.send(msg)

        else:

            for msg in partMessage:

                if msg in msgs:

                    messenger.send(msg)

    def __convert_event_to_msg(self, event):

        if event.endswith("-up"):

            return event[:(len(event)-3)] + "_effert_end"

        else:

            return event + "_effert"

    def get_eventMessageMap(self):

        return self.__eventMessageMap

