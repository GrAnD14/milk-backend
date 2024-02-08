import psycopg2
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Service, Order
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'service_list.html', {'services': services})


def findByName(request):
    name_to_search = request.GET.get('name_to_search')
    product = Service.objects.filter(is_active=True, name__contains=name_to_search)
    return render(request, 'service_list.html', {'services': product, 'name_to_search': name_to_search})


def deactivateService(request):
    pass
    service_id = request.GET.get('service_id')
    name_to_search = request.GET.get('name_to_search')



    conn = psycopg2.connect(dbname=settings['default']['NAME'],
                            host=settings['default']['HOST'],
                            user=settings['default']['USER'],
                            password=settings['default']['PASSWORD'],
                            port=settings['default']['PORT'])

    cursor = conn.cursor()
    cursor.execute(f"UPDATE milkapp_service set is_active=False where id={service_id}")
    conn.commit()
    cursor.close()
    conn.close()

    services = Service.objects.filter(is_active=True, name__contains=name_to_search)
    return render(request, 'service_list.html', {'services': services, 'name_to_search': name_to_search})

#k
def service_detail(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, 'service_detail.html', {'service': service})


def orders(request):
    all_orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': all_orders})


def create_order(request):
    if request.method == 'POST':
        parent_name = request.POST['parent_name']
        service_id = request.POST['service_id']
        order = Order(parent_name=parent_name, service_id=service_id)
        order.save()
        return redirect(reverse('service_detail', args=[service_id]))


def new_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']

        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)

            new_service = Service(name=name, price=price, image=filename)
            new_service.save()

            return redirect(reverse('service_list'))

    return render(request, 'new_service.html')
