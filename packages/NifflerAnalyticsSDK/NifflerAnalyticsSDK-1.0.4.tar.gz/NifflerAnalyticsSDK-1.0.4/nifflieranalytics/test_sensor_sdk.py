from sdk import *


def test_sensor_track():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/sensor.log"
    consumer = ConcurrentLoggingConsumer(log_name, encoding='utf-8')
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production', sensor_project_name="production")
    properties = {
        'name': 'test_sensor_track',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.sensor_track(distinct_id, event_name, properties, is_login_id=False)
    niffer.close()


if __name__ == '__main__':
    test_sensor_track()
