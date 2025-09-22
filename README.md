## Real Estate Backend(Django+DRF)
Features:
(Product)مدیریت محصولات
(Order)مدیریت سفارش ها
(Payment)مدیریت پرداخت ها
JWT (Login/Register) احراز هویت
API  (Swagger and Redoc) ساده و آماده برای توسعه

## clone the project
git clone 
https://github.com/Elid1993/Django-online-shop

## create a virtual environment
python -m venv venv  
venv\scripts\activate  #windows
source venv/bin/activate  #linux/mac

## install requirement
pip install -r requirements.txt

## database migration
python manage.py makemigrations
python manage.py migrate

## create admin 
python manage.py createsuperuser

## run project
python manage.py runserver

## API
Swagger UI: http://localhost:8000/api/swagger-ui/
Redoc:http://localhost:8000/api/redoc/
schema(openAPI):http://localhost:8000/api/schema/

## Models & Fields
Product 
name: اسم محصول
description:توضیحات محصول
price:قیمت محصول
stoc:موجودی

## order
product:محصول سفارش داده شده
quantity:تعداد
total_price:جمع کل سفارش
status: وضعیت سفارش( pending,paid,canceled)

## Payment 
order : سفارش مربوطه
amount:مبلغ پرداخت
status:وضعیت پرداخت (paid,pending,canceled)
payment_method:روش پرداخت (زرین پال)