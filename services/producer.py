from confluent_kafka import Producer
import json

# Конфигурация Kafka Producer

conf = {
    'bootstrap.servers': 'kafka:9092',  # адрес Kafka broker
    'client.id': 'todo-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    """Callback для подтверждения доставки сообщения"""
    if err is not None:
        print(f'Ошибка доставки сообщения: {err}')
    else:
        print(f'Сообщение доставлено в {msg.topic()} [{msg.partition()}] по offset {msg.offset()}')

def send_task_email(topic, name: str, user_email: str):
    """Функция отправки события с задачей для email в Kafka"""
    #topic = 'todo-email-kafka'
    message = {
        'task_name': name,
        'email': user_email,
        'subject': 'Уведомление о регистрации',
        'body': f'Пользователь с почтовым адресом {user_email} успешно создан!'
    }
    for i in range(1):
        producer.produce(
        topic=topic,
        value=json.dumps(message),
        on_delivery=delivery_report
    )
        producer.flush()  # Гарантируем отправку перед завершением функции

