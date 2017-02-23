import logging
from landport.core.dispatch import ClientDispatchManager, CenterDispatchManager
from landport.core.user import UserConnectManager
logger = logging.getLogger('simple')


class MyCenterMessageDispatcher(CenterDispatchManager):
    def hello(self, data):
        logger.info('hello messagetype ...%s',data)
        UserConnectManager.broadcast(data)

    def hey(self, data):
    	logger.info('hey messagetype ...%s', data)



class MyClientMessageDispatcher(ClientDispatchManager):
    def hello(self, handler, data):
        logger.info('hello messagetype ...')
        handler.write_message('good bye')
