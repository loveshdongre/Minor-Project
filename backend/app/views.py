from .models import Student, Result, ResType
from .serializers import StudentSerializer, ResultSerializer, ResTypeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def StudentView(request):
    # {'res_type': '1', 'course': 'btech', 'sem': '5', 'roll_no': '0101CS171015', 'no': '10'}
    data = request.data
    list = []
    count = 0
    students = Student.objects.filter(roll_no__gte = data['roll_no'], course__exact = data['course'])
    for stud in students:
        
        count = count + 1
        
        if count > int(data['no']):
            break

        result = Result.objects.filter(student__exact = stud.id, sem__exact = data['sem'], res_type__exact = data['res_type'])
        resType = ResType(count, stud.roll_no, stud.name, result[0].sgpa, result[0].res_des, result[0].status)
        list.append(resType)

    serializer = ResTypeSerializer(list, many = True)  

    return Response(data=serializer.data, status = status.HTTP_200_OK)

