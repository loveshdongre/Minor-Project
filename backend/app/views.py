from .models import Student, Result, ResType
from .serializers import StudentSerializer, ResultSerializer, ResTypeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# import object_detection_image as od
import ResultFetcher as rf


@api_view(['POST'])
def StudentView(request):
    # {'res_type': '1', 'course': 'btech', 'sem': '5', 'roll_no': '0101CS171015', 'no': '10'}
    data = request.data
    no = int(data['no'])
    list = []
    count = 0
    position = 1
    cur_roll_no = data['roll_no']
    roll_no_part1 = cur_roll_no[0:6]
    while count < no:
        count = count + 1

        # if Student and result exist
        stud = Student.objects.all().filter(roll_no__exact=cur_roll_no)

        if stud.count() > 0:
            result = Result.objects.filter(
                student__exact=stud[0].id, sem__exact=data['sem'], res_type__exact=data['res_type'])
            if result != None:
                resType = ResType(
                    position, stud[0].roll_no, stud[0].name, result[0].sgpa, result[0].res_des, result[0].status)
                position = position + 1
                list.append(resType)

        cur_roll_no = roll_no_part1 + str(int(cur_roll_no[6:]) + 1)

    serializer = ResTypeSerializer(list, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def Generate(request, format=None):
    data = request.data

    
    # captcha_text = od.Captcha_detection(
    #     '{}/captcha{}.png'.format('img_download', '0101CS171001'))

    content = {
        'status': 'request permitted'
    }

    return Response(content)
