from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.http import HttpResponse
import csv

from .models import Record, Status, User
from .serializers import RecordSerializer, RecordInitialSerializer, StatusSerializer


# TEST Task
def loginToRecord(email, pwd):
    username = email
    password = pwd
    try:
        user = authenticate(username=username, password=password)
    except User.DoesNotExist as e:
        return Response({"login status":"failed"})
    if user is not None:
        user = User.objects.only('id').get(username=email)
    return user

@api_view(['GET', 'POST'])
def export(request, email, pwd):
    user = loginToRecord(email,pwd)
    
    if type(user) is User:
        response = HttpResponse(content_type = 'text/csv')
        writer = csv.writer(response)
        writer.writerow(['pk','created_at','description','phone','status_title'])
        for rec in Record.objects.all().values_list('id','created_at','description','phone','status_id').filter(user_id=user.id):
            temp = list(rec)
            temp[3] = temp[3][:-3] + "***"
            temp[4] = Status.objects.get(id=temp[4])
            rec = tuple(temp)
            writer.writerow(rec)
        filename = str(user.id) + "_" + user.first_name + ".csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    else:
        return Response({"login status":"failed"})
@api_view(['GET', 'POST'])
def records_list(request, email, pwd):
    user = loginToRecord(email,pwd)
    
    if type(user) is User:
        if request.method == 'GET':
                login(request,user)
                records = Record.objects.filter(user_id=user.id)
                serializer = RecordSerializer(records, many=True)
                return Response(serializer.data)
            
        elif request.method == 'POST':
            serializer = RecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"login status":"failed"})

@api_view(['GET', 'PUT', 'DELETE'])
def record_detail(request, email,pwd,record_id):
    user = loginToRecord(email,pwd)
    
    if type(user) is User:
        try:
            record = Record.objects.filter(user_id=user.id).get(id=record_id)
        except Record.DoesNotExist as e:
            return Response({'error': str(e)})

        if request.method == 'GET':
            serializer = RecordSerializer(record)
            return Response(serializer.data)
        elif request.method == 'PUT':
            status = Status.objects.only('id').get(id=request.data['status_id'])
            user = User.objects.only('id').get(id=request.data['user_id'])

            request.data.update({"status_id": status})
            request.data.update({"user_id": user})
            serializer = RecordInitialSerializer(instance=record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.update(serializer.instance, request.data)
                return Response(serializer.data)
            return Response({'error': serializer.errors})
        elif request.method == 'DELETE':
            record.delete()

            return Response({'deleted': True})
    else:
        return Response({"login status":"failed"})




@api_view(['GET', 'POST'])
def status_list(request):
    if request.method == 'GET':
        statusList = Status.objects.all()
        serializer = StatusSerializer(statusList, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def status_detail(request, status_id):
    try:
        statusType = Status.objects.get(id=status_id)
    except Record.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = StatusSerializer(statusType)
        return Response(serializer.data)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










# OLD PROJECT VIEWS
# class User2ListAPIView(APIView):
#     def get(self, request):
#         users = User2.objects.all()
#         serializer = User2Serializer(users, many=True)
#         return Response(serializer.data)


#     def post(self, request):
#         serializer = User2Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class User2DetailAPIView(APIView):
#     def get_object(self, user_id):
#         try:
#             return User2.objects.get(id=user_id)
#         except User2.DoesNotExist as e:
#             return Response({'error': str(e)})

#     def get(self, request, user_id):
#         user = self.get_object(user_id)
#         serializer = User2Serializer(user)
#         return Response(serializer.data)

#     def put(self, request, user_id):
#         user = self.get_object(user_id)
#         serializer = User2Serializer(instance=user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({'error': serializer.data})

#     def delete(self, request, user_id):
#         user = self.get_object(user_id)
#         user.delete()

#         return Response({'deleted': True})
















# ---------------PRODUCT FBV---------------
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist as e:
#         return Response({'error': str(e)})

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         # post = request.POST.copy()
#         # # request.POST.get("category_id")
#         # post['category_id'] = category
#         # request.POST = post

#         category = Category.objects.only('id').get(id=request.data['category_id'])

#         request.data.update({"category_id": category})
#         serializer = Product2Serializer(instance=product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.update(serializer.instance, request.data)
#             return Response(serializer.data)
#         return Response({'error': serializer.errors})
#     elif request.method == 'DELETE':
#         product.delete()

#         return Response({'deleted': True})

# @api_view(['GET'])
# def products_by_categoryId(request, category_id):
#     if request.method == 'GET':
#         products = Product.objects.filter(category_id=category_id)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

# @api_view(['GET'])
# def top_ten_products(request):
#     if request.method == 'GET':
#         top_ten = Product.objects.get_top_ten_products()
#         serializer = ProductSerializer(top_ten, many=True)
#         return Response(serializer.data)                    #TODO
# # -----------------------------------------
# # ---------------COMMENT FBV---------------

# @api_view(['GET', 'POST'])
# def comment_list(request):
#     if request.method == 'GET':
#         comments = Comment.objects.all()
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(['GET', 'PUT', 'DELETE'])
# def comment_detail(request, comment_id):
#     try:
#         comment = Comment.objects.get(id=comment_id)
#     except Product.DoesNotExist as e:
#         return Response({'error': str(e)})

#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.update(serializer.instance, request.data)
#             return Response(serializer.data)
#         return Response({'error': serializer.errors})
#     elif request.method == 'DELETE':
#         comment.delete()

#         return Response({'deleted': True})

# @api_view(['GET'])
# def comments_by_productId(request, product_id):
#     if request.method == 'GET':
#         comments = Comment.objects.filter(product_id=product_id)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
# # -----------------------------------------


# @api_view(['GET', 'PUT', 'DELETE'])
# def company_detail(request, company_id):
#     try:
#         company = Company.objects.get(id=company_id)
#     except Company.DoesNotExist as e:
#         return Response({'error': str(e)})

#     if request.method == 'GET':
#         serializer = CompanySerializer(company)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CompanySerializer(instance=company, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.update(serializer.instance, request.data)
#             return Response(serializer.data)
#         return Response({'error': serializer.errors})
#     elif request.method == 'DELETE':
#         company.delete()

#         return Response({'deleted': True})


# @api_view(['GET'])
# def vacancy_by_companyId(request, company_id):
#     if request.method == 'GET':
#         vacancies = Vacancy.objects.filter(company=company_id)
#         serializer = VacancySerializer(vacancies, many=True)
#         return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def vacancies_list(request):
#     if request.method == 'GET':
#         vacancies = Vacancy.objects.all()
#         serializer = VacancySerializer(vacancies, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = VacancySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def vacancy_detail(request, vacancy_id):
#     try:
#         vacancy = Vacancy.objects.get(id=vacancy_id)
#     except Vacancy.DoesNotExist as e:
#         return Response({'error': str(e)})

#     if request.method == 'GET':
#         serializer = VacancySerializer(vacancy)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = VacancySerializer(instance=vacancy, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({'error': serializer.errors})

#     elif request.method == 'DELETE':
#         vacancy.delete()
#         return Response({'deleted': True})


# @api_view(['GET'])
# def top_ten_vacancies(request):
#     if request.method == 'GET':
#         top_ten = Vacancy.objects.order_by('-salary')[:10]
#         serializer = VacancySerializer(top_ten, many=True)
#         return Response(serializer.data)