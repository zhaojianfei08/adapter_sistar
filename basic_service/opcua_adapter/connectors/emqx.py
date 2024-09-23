import paho.mqtt.client as mqtt
import time

from basic_service.opcua_adapter.config import emqx_connection_params
from get_logger import logger


class MQTTClient:
    def __init__(self, broker, port, client_id, keep_alive_interval, password=None, username=None, topic_sub=None,
                 topic_pub=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.keep_alive_interval = keep_alive_interval
        self.topic_sub = topic_sub
        self.topic_pub = topic_pub
        self.password = password
        self.username = username
        # 创建 MQTT 客户端
        self.client = mqtt.Client(client_id=self.client_id)
        if self.username and self.password:
            self.client.username_pw_set(username=self.username, password=self.password)  # 如果有需要设置用户名密码
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.connect()
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT Broker! Returned code={rc}")
            if self.topic_sub:
                client.subscribe(self.topic_sub)  # 连接成功后，订阅主题
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.info("Disconnected from MQTT Broker with code: " + str(rc))
        # 这里可以实现重连逻辑
        self.reconnect()

    def on_message(self, client, userdata, msg):
        # logger.info(f"Received message: {msg.topic} -> {msg.payload.decode()}")
        pass

    def on_publish(self, client, userdata, mid):
        # print(f"Message {mid} has been published.")
        pass

    # 重连机制
    def reconnect(self):
        try:
            logger.error("Attempting to reconnect...")
            self.client.reconnect()  # 尝试重连
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            time.sleep(5)  # 延时后再尝试

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, self.keep_alive_interval)
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.reconnect()


get_emqx_connection = MQTTClient(**emqx_connection_params)

# 主循环发布消息
# try:
#     while True:
#         message = "Hello MQTT"
#         result = mqtt_client.client.publish('/test', message, qos=0)
#         status = result[0]
#         if status == 0:
#             print(f"Sent `{message}` to topic /test")
#         else:
#             print(f"Failed to send message to topic /test")
#         time.sleep(10)  # 每10秒发布一次
# except KeyboardInterrupt:
#     print("Interrupted by user, stopping...")
# finally:
#     mqtt_client.client.loop_stop()
#     mqtt_client.client.disconnect()
