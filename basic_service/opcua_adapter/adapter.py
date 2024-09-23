import datetime
import json
import os
import queue
import threading
import time
from threading import Thread
from typing import List, Any
import opcua.client.client
import psutil as psutil
from opcua.client.client import Client
from opcua.common.node import Node
from opcua.ua import UaStatusCodeError
from config import opcua_adapter_params
from connectors._redis import get_redis_connection
from connectors.emqx import get_emqx_connection
from connectors.mysql import get_mysql_connection
from connectors.tdengine import get_tdengine_connection
from get_logger import logger
from sqlalchemy import text

emqx_connection = get_emqx_connection.client


class OPCUAAdapter(object):
    """
    OPCUA数据采集类
    """

    def __init__(self, device_info, tag_id_to_node_id_map, tag_id_to_detail_map, use_subscribe=True):
        self.url: str = device_info.get('device_url')
        self._ua: opcua.client.client.Client = Client(url=self.url, timeout=5)
        self.connected: bool = False
        self.thread_list: List[Thread] = []
        self.raw_dict = {}
        self.tag_id_to_node_id_map = tag_id_to_node_id_map
        self.tag_id_to_detail_map = tag_id_to_detail_map
        self.device_info = device_info
        self.alarm_consumer_queue = queue.Queue(maxsize=opcua_adapter_params['alarm_consumer_queue_length'])
        self.archive_consumer_queue = queue.Queue(maxsize=opcua_adapter_params['archive_consumer_queue_length'])
        self.emqx_consumer_queue = queue.Queue(maxsize=opcua_adapter_params['emqx_consumer_queue_length'])

    def connect(self):
        """
        连接函数
        :return:
        """
        try:
            if self.connected:
                return
            else:
                self._ua.connect()
                self.connected = True
                logger.info(f"初次连接{self.url}成功！")
                return
        except Exception as e:
            self.disconnect()
            self.connected = False
            logger.error("初次连接失败,失败原因：", str(e))
            # 开始重连
            self.reconnect()

    def disconnect(self):
        """
        断开连接
        :return:
        """
        try:
            if self._ua and self.connected:
                self._ua.disconnect()
                self.connected = False
                logger.info("主动断开连接成功")
        except Exception as e:
            logger.error("主动断开连接失败，失败原因：", str(e))

    def reconnect(self):
        """
        重连
        :return:
        """
        index = 0
        while True:
            try:
                self._ua.connect()
                self.connected = True
                index = 0
                logger.info(f"重连{self.url}成功!")
                return
            except AttributeError as e:
                index += 1
                logger.error(f"第{index}次重连失败,失败原因：{str(e)}!")
                self.connected = False
                time.sleep(index * 1)
                continue
            except ConnectionRefusedError as e:
                index += 1
                logger.error(f"第{index}次重连失败,失败原因：{str(e)}!")
                self.connected = False
                time.sleep(index * 1)
                continue
            except OSError as e:
                index += 1
                logger.error(f"与OPCUA服务器未能建立连接,失败原因:{str(e)}!")
                self.connected = False
                time.sleep(index * 1)
                continue
            except Exception as e:
                index += 1
                logger.error(f"第{index}次重连失败,失败原因：{str(e)}!")
                self.connected = False
                time.sleep(index * 1)
                continue

    def interval_read(self, interval: int) -> None:
        """
        按照采集频率定时去采集
        :param interval:
        :return:
        """
        connection = get_redis_connection()
        thread_name = threading.current_thread().name
        nodes = []
        while True:
            # 每分钟采集多少次，采集超时多少次，采集node数量，多少个node是None
            start_time = time.time()
            if not self.connected:
                # 如果没有连接成功，开启重连
                self.reconnect()
            else:
                try:
                    nodes_str_list = self.tag_id_to_node_id_map.keys()
                    nodes = [self._ua.get_node(node) for node in nodes_str_list]
                    values = self._ua.get_values(nodes)
                    self.raw_dict = dict(zip(nodes_str_list, values))
                except AttributeError as e:
                    logger.error(f"属性读取错误:{str(e)}!")
                except TimeoutError:
                    logger.error(f"接收服务端报文超时")
                except ConnectionRefusedError as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f"数据获取失败,失败原因:{str(e)}!")
                except ConnectionAbortedError as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f"数据获取失败,失败原因:{str(e)}!")
                except UaStatusCodeError as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f"数据获取失败,失败原因:{str(e)}!")
                except OSError as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f"数据获取失败,失败原因:{str(e)}!")
                except RuntimeError as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f'运行错误,失败原因:{str(e)}')
                except Exception as e:
                    self.disconnect()
                    self.reconnect()
                    logger.error(f"未捕获到的异常：{str(e)}")
                finally:
                    end_time = time.time()
                    try:
                        connection.hmset('performance',
                                         mapping={'nodes': len(nodes), f'{thread_name}_use_time': f'{(end_time - start_time):.2f}'})
                    except Exception:
                        if connection:
                            connection.close()
                            connection = get_redis_connection()
                    time.sleep(interval)

    def node_write(self, nodes: List[Node], values: List[Any]):
        """
        写入node
        :param nodes:
        :param values:
        :return:
        """
        try:
            self._ua.set_values(nodes, values)
        except Exception as e:
            logger.error(f"数据写入失败,失败原因：{str(e)}")

    def monitor_thread(self):
        """
        监视线程
        :return:
        """
        redis_connection = get_redis_connection()
        while True:
            try:
                current_process_id = os.getpid()
                process = psutil.Process(current_process_id)
                # 获取进程的基本信息
                process_name = process.name()
                cpu_usage = process.cpu_percent(interval=1)  # 进程的 CPU 使用率，间隔 1 秒
                memory_info = process.memory_info()  # 进程的内存使用情况
                io_counters = process.io_counters()  # 进程的 IO 计数
                disk_usage = psutil.disk_usage('/')  # 获取根目录的磁盘使用情况
                thread_list = []

                for thread in threading.enumerate():
                    thread_list.append((thread.ident, thread.name, thread.is_alive()))
                    if thread.name == 'continuous_thread' and thread.is_alive() == False:
                        logger.error(f'读取线程出错，请尽快联系管理员处理！')
                redis_connection.hmset(name='performance',
                                       mapping={'process_name': process_name, 'cpu_usage': cpu_usage,
                                                'memory_info_RSS': f'{memory_info.rss / (1024 * 1024):.2f} MB',
                                                'memory_info_VMS': f'{memory_info.vms / (1024 * 1024): .2f} MB',
                                                'io_read': f"{io_counters.read_bytes / (1024 * 1024):.2f} MB",
                                                'io_write': f"{io_counters.write_bytes / (1024 * 1024):.2f} MB",
                                                'disk_usage': f'{disk_usage.percent}%',
                                                'threads': json.dumps(thread_list),
                                                'pid': current_process_id,
                                                'archive_consumer_length': self.archive_consumer_queue.qsize(),
                                                'alarm_consumer_length': self.alarm_consumer_queue.qsize(),
                                                'emqx_consumer_length': self.emqx_consumer_queue.qsize(),
                                                })

            except Exception as e:
                logger.error(f'监控子线程出错:{str(e)}')
                if redis_connection:
                    redis_connection.close()
                    redis_connection = get_redis_connection()
            finally:
                time.sleep(int(opcua_adapter_params['monitor_frequency']))

    def change_data_notifier(self, timestamp, node_id, new_data, old_data):
        """
        :param timestamp:
        :param node:
        :param new_data:
        :param old_data:
        :return:
        """
        try:
            tag_id = self.tag_id_to_node_id_map[node_id]
        except KeyError:
            pass
        else:
            content = {
                'timestamp': timestamp,
                'tag_id': tag_id,
                'new_data': new_data,
                'old_data': old_data
            }
            self.alarm_consumer_queue.put(content)
            self.emqx_consumer_queue.put(content)
            self.archive_consumer_queue.put(content)

    def consumer_alarm_info(self):
        """
        处理报警信息
        :return:
        """
        redis_connection = get_redis_connection()
        alarm_table_name = opcua_adapter_params['alarm_table_name']
        connection = get_mysql_connection()
        thread_name = threading.current_thread().name
        alarm_count = 0
        while True:
            try:
                start_time = time.time()
                content = self.alarm_consumer_queue.get()
                tag_detail = self.tag_id_to_detail_map.get(content['tag_id'])
                active_alarm = tag_detail.get('active_alarm')
                if active_alarm:
                    up_limit = tag_detail.get('alarm_up')
                    down_limit = tag_detail.get('alarm_down')
                    if float(content['new_data']) > float(up_limit):
                        sql = f"""insert into {alarm_table_name} (device_name, tag_uuid, tag_name,alarm_message,alarm_limit,value) values ("{self.device_info['device_name']}","{content["tag_id"]}", "{tag_detail.get("comments")}", "{tag_detail.get("alarm_up_info")}", "{tag_detail.get("alarm_up")}", "{content["new_data"]}")"""
                        try:
                            connection.execute(text(sql))
                            connection.commit()
                            alarm_count += 1
                        except Exception as e:
                            logger.error(f'数据插入错误,错误原因:{str(e)}!')
                            connection.rollback()
                    elif float(content['new_data']) < float(down_limit):
                        sql = f"""insert into {alarm_table_name} (device_name, tag_uuid, tag_name,alarm_message,alarm_limit,value) values ("{self.device_info['device_name']}","{content["tag_id"]}", "{tag_detail.get("comments")}", "{tag_detail.get("alarm_down_info")}", "{tag_detail.get("alarm_down")}", "{content["new_data"]}")"""
                        try:
                            connection.execute(text(sql))
                            connection.commit()
                            alarm_count += 1
                        except Exception as e:
                            logger.error(f'数据插入错误,错误原因:{str(e)}!')
                            connection.rollback()
            except Exception as e:
                logger.error(str(e))
                if connection:
                    connection.close()
                    connection = get_mysql_connection()
            finally:
                end_time = time.time()
                try:
                    redis_connection.hmset('performance',
                                           mapping={f'{thread_name}_use_time': f'{(end_time - start_time):.2f}',
                                                    'alarm_count': alarm_count})
                except Exception:
                    if redis_connection:
                        redis_connection.close()
                        redis_connection = get_redis_connection()
                time.sleep(2)

    def consumer_archive_info(self):
        thread_name = threading.current_thread().name
        redis_connection = get_redis_connection()
        connection = get_tdengine_connection()
        exception_buffer = {}
        buffer = {}
        db_name = opcua_adapter_params['archive_table_name']
        exception_time = 0
        total_time = 0
        for k in self.tag_id_to_node_id_map.values():
            buffer.setdefault(k, [])
            # 异常buffer，当数据没有被正常插入时，数据不被丢弃，放到异常队列中，一旦恢复了连接，先将异常队列中的数据恢复
            exception_buffer.setdefault(k, [])
        while True:
            try:
                start_time = time.time()
                for k, v in exception_buffer.items():
                    if len(v) > 0:
                        sql = f"""INSERT INTO {db_name}.{k} VALUES {str(v).replace('[', '').replace(']', '')}"""
                        try:
                            connection.execute(sql)
                            connection.commit()
                            exception_buffer.setdefault(k, [])
                        except Exception:
                            exception_time += 1
                            connection.rollback()
                content = self.archive_consumer_queue.get()
                tag_detail = self.tag_id_to_detail_map.get(content['tag_id'])
                if tag_detail.get('active_archive'):
                    timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    try:
                        data = float(content['new_data'])
                    except ValueError:
                        data = 0.0
                    except TypeError:
                        data = 0.0
                    except Exception:
                        data = 0.0
                    if len(buffer[content['tag_id']]) < 100:
                        buffer[content['tag_id']].append((timestamp, data))
                    else:
                        sql = f"""INSERT INTO {db_name}.{content['tag_id']} VALUES {str(buffer[content["tag_id"]]).replace('[', '').replace(']', '')};"""
                        try:
                            connection.execute(text(sql))
                            connection.commit()
                            buffer[content['tag_id']] = []
                        except Exception:
                            logger.error(f'insert error:{sql}')
                            connection.rollback()
                            exception_time += 1
                            if len(exception_buffer) < 10000:
                                exception_buffer[content['tag_id']].extend(buffer[content['tag_id']])
                                buffer[content['tag_id']] = []
                            else:
                                # 如果超过设定的缓存值滞后，将旧值丢弃掉
                                exception_buffer[content['tag_id']] = exception_buffer[content['tag_id']][100:]
                total_time += 1
            except Exception as e:
                logger.error(str(e))
                exception_time += 1
                if connection:
                    connection.close()
                    connection = get_tdengine_connection()
            finally:
                end_time = time.time()
                try:
                    redis_connection.hmset('performance',
                                           mapping={'buffer': len(buffer), 'exception_buffer': len(exception_buffer),
                                                    f'{thread_name}_use_time': f'{(end_time - start_time):.2f}',
                                                    'total_time': total_time,
                                                    'exception_time': exception_time})
                except Exception:
                    if redis_connection:
                        redis_connection.close()
                        redis_connection = get_redis_connection()
                time.sleep(2)

    def consumer_emqx_info(self):
        while True:
            try:
                content = self.emqx_consumer_queue.get()
                tag_detail = self.tag_id_to_detail_map.get(content['tag_id'])
                mqtt_topic_str = tag_detail.get('mqtt_topic_name')
                topic_list = []
                for topic in mqtt_topic_str.split(';'):
                    topic_name, qos = topic.split(',')
                    topic_list.append({'topic_name': topic_name.split(':')[1].strip().replace('\n', ''),
                                       'qos': qos.split(':')[1].strip().replace('\n', '')})
                payload = json.dumps({content['tag_id']: content['new_data']})
                for topic in topic_list:
                    emqx_connection.publish(topic=topic['topic_name'], payload=payload, qos=int(topic['qos']))
            except Exception as e:
                logger.error(str(e))

    def subscribe_data_change(self):

        copy_raw_dict = self.raw_dict.copy()
        flag = False
        while True:
            d1_keys = self.raw_dict.keys()
            d2_keys = copy_raw_dict.keys()

            if _ := d1_keys - d2_keys:
                flag = True
                for k in list(_):
                    self.change_data_notifier(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), k,
                                              self.raw_dict[k],
                                              0)
            if _ := d2_keys - d1_keys:
                flag = True
                for k in list(_):
                    self.change_data_notifier(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), k, 0,
                                              self.raw_dict[k])

            commen_keys = d1_keys & d2_keys

            for key in commen_keys:
                if copy_raw_dict[key] != self.raw_dict[key]:
                    self.change_data_notifier(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), key,
                                              copy_raw_dict[key], self.raw_dict[key])
                    flag = True
            if flag:
                copy_raw_dict = self.raw_dict.copy()
                flag = False
            time.sleep(0.5)

    def run(self):
        """
        启动服务
        :return:
        """
        try:
            self.connect()
            interval_acqusition_task = Thread(target=self.interval_read, name='continuous_thread', args=(1,))
            monitor_thread_task = Thread(target=self.monitor_thread, name='monitor_thread')
            subscribe_thread_task = Thread(target=self.subscribe_data_change, name='subscribe_thread')
            for i in range(opcua_adapter_params['alarm_worker']):
                consumer_alarm_info_task = Thread(target=self.consumer_alarm_info, name=f'consumer_alarm_info_{i+1}')
                self.thread_list.append(consumer_alarm_info_task)
            for i in range(opcua_adapter_params['archive_worker']):
                consumer_archive_info_task = Thread(target=self.consumer_archive_info, name=f'consumer_archive_info_{i+1}')
                self.thread_list.append(consumer_archive_info_task)
            for i in range(opcua_adapter_params['emqx_worker']):
                consumer_emqx_info_task = Thread(target=self.consumer_emqx_info, name=f'consumer_emqx_info_{i+1}')
                self.thread_list.append(consumer_emqx_info_task)
            self.thread_list.append(interval_acqusition_task)
            self.thread_list.append(monitor_thread_task)
            self.thread_list.append(subscribe_thread_task)
            for th in self.thread_list:
                th.start()
            for th in self.thread_list:
                th.join()
        except Exception as e:
            logger.error(str(e))
        finally:
            get_emqx_connection.client.loop_stop()
            get_emqx_connection.client.disconnect()


def init():
    conn = get_redis_connection()
    while True:
        try:
            device_info = json.loads(conn.get('device_info'))
            tag_id_to_node_id_map = json.loads(conn.get('tag_id_to_node_id_map'))
            tag_id_to_detail_map = json.loads(conn.get('tag_id_to_detail_map'))
            if device_info and tag_id_to_detail_map and tag_id_to_node_id_map:
                return device_info, tag_id_to_node_id_map, tag_id_to_detail_map
            else:
                logger.error('init error')
                time.sleep(3)
                continue
        except Exception:
            logger.error('Init Failed!')
            time.sleep(3)
            continue


def main():
    device_info, tag_id_to_node_id_map, tag_id_to_detail_map = init()
    opcua_adapter = OPCUAAdapter(device_info=device_info, tag_id_to_node_id_map=tag_id_to_node_id_map,
                                 tag_id_to_detail_map=tag_id_to_detail_map)
    opcua_adapter.run()


if __name__ == '__main__':
    main()
