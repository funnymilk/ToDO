import json
from confluent_kafka import Consumer, KafkaException
import os
import smtplib
from email.mime.text import MIMEText

yandex_user = 'redisgame@yandex.ru'
yandex_password = 'wpcuomeiqpbkewcw'
# 1 wpcuomeiqpbkewcw This user does not have access rights to this service
# 2 nxrkglazckhnivox This user does not have access rights to this service

def send_email_yandex(to_email, subject, body):
    print("SMTP отправка на:", to_email)
    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = yandex_user
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(yandex_user, yandex_password)
        smtp.sendmail(yandex_user, [to_email], msg.as_string())


# пример использования
#send_email_yandex('recipient@example.com', 'Тестовая тема', 'Пример отправки через Яндекс SMTP')

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'todo-email-group',
    'auto.offset.reset': 'earliest'  # считаем только новые сообщения
}

consumer = Consumer(conf)
topic = "todo-email-kafka"
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        data = json.loads(msg.value().decode('utf-8'))
        print("Parsed data:", data)
        try:
            send_email_yandex(data['email'], data['subject'], data['body'])
        except Exception as e:
            print('Ошибка отправки письма:', e)
        consumer.commit(msg)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    consumer.close()
