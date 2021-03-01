import pika
import json
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()
from products.models import Product

params = pika.URLParameters(
    '')
connection = pika.BlockingConnection(params)
chanel = connection.channel()


chanel.queue_declare(queue='admin')


def callback(chanel, method, properties, body):
    print('Recived in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


chanel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

chanel.start_consuming()
chanel.close()
