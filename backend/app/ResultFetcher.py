# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# your imports, e.g. Django models
from .models import Student, Result

import time
import cv2
import csv
import os
import urllib.request
from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import app.object_detection_image as od
# from .models import Student, Result

# xpath
main_xpath = {
    "BE": '//*[@id="ctl00_ContentPlaceHolder1_radlstProgram_0"]',
    "MCA": '//*[@id="ctl00_ContentPlaceHolder1_radlstProgram_1"]',
    "ME": '//*[@id="ctl00_ContentPlaceHolder1_radlstProgram_2"]',
    "MTECH": '//*[@id="ctl00_ContentPlaceHolder1_radlstProgram_3"]',
    "BTECH": '//*[@id="ctl00_ContentPlaceHolder1_radlstProgram_4"]',
}
reval_xpath = {
    "BE": '//*[@id="ctl00_ContentPlaceHolder1_radlstRevalProg_0"]',
    "MCA": '//*[@id="ctl00_ContentPlaceHolder1_radlstRevalProg_1"]',
    "ME": '//*[@id="ctl00_ContentPlaceHolder1_radlstRevalProg_2"]',
    "MTECH": '//*[@id="ctl00_ContentPlaceHolder1_radlstRevalProg_3"]',
    "BTECH": '//*[@id="ctl00_ContentPlaceHolder1_radlstRevalProg_4"]',
}
rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtrollno"]'
sem_xpath = '//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]'
captcha_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/img'
captcha_field_xpath = '//*[@id="ctl00_ContentPlaceHolder1_TextBox1"]'
submit_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnviewresult"]'
reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
st_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblNameGrading"]'
st_rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblRollNoGrading"]'
st_branch_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblBranchGrading"]'
st_sgpa_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblSGPA"]'
st_status_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblStatusGrading"]'
st_res_des_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblResultNewGrading"]'
reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'

# Key variables
COURSE = 'BTech'
CLG_CODE = '0101'
BRANCH = 'CS'
ROLL_START = 171001
ROLL_END = 1710010  # 171117
SEM = '5'
IMG_DLD = 'img_download'
# chrome_driver = 'C:\chromedriver_win32\chromedriver.exe'
url = 'http://www.uitrgpv.ac.in/Exam/ProgramSelect.aspx'
# keep_alive = False
headless = False


class Student_Local:
    name = ''
    rollno = ''
    branch = ''
    course = ''
    sem = ''
    sgpa = ''
    status = ''
    res_des = ''

    def display(self):
        print('name: ', self.name)
        print('rollno: ', self.rollno)
        print('branch: ', self.branch)
        print('course: ', self.course)
        print('sem: ', self.sem)
        print('sgpa: ', self.sgpa)
        print('status: ', self.status)
        print('res_des: ', self.res_des)


def write_row(stud):
    with open('csv/resultcse.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([stud.rollno, stud.name, stud.sgpa,
                         stud.sem, stud.branch, stud.course])


# request comment
    # res_type= M, R
    # course = BE, MCA, ME, MTECH, BTECH
    # sem = 1, 2, 3, 4, 5, 6, 7, 8
    # roll_no = 0101CS171001
    # no = 3

def generate_result(_res_type, _course, _sem, _roll_no, _no):

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    # remove
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--disable-extensions')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    chrome_driver = dir_path + "/chromedriver"
    os.environ['webdriver.chrome.driver'] = chrome_driver

    # driver = webdriver.Chrome(chrome_driver, keep_alive=keep_alive, chrome_options=chrome_options)
    driver = webdriver.Chrome(
        executable_path=chrome_driver, chrome_options=chrome_options)
    driver.get(url)

    course_xpath = ''
    if _res_type == 'M':
        course_xpath = main_xpath[_course]
    elif _res_type == 'R':
        course_xpath = reval_xpath[_course]

    course = driver.find_element_by_xpath(course_xpath)
    course.click()

    count = 0
    cur_roll_no = _roll_no.upper()
    roll_no_part1 = cur_roll_no[0:6]

    while count < int(_no):

        count = count + 1
        captcha_decoded = False
        # find cur_roll_no exist in Student

        stud = Student.objects.filter(roll_no__exact=cur_roll_no)

        # if cur_roll_no don't exist in student
        if stud.count() == 0:
            # create a student
            stud = Student(name="ENROLLMENT DON'T EXIST",
                           roll_no=cur_roll_no, course=_course)
            stud.save()
        else:
            stud = stud[0]
        # if result don't exist for cur_roll_no
        result = Result.objects.filter(
            student__exact=4, sem__exact=_sem, res_type__exact=_res_type)

        if result.count() == 0:
            # find result for cur_roll_no and save
            while not captcha_decoded:

                try:
                    rollno = driver.find_element_by_xpath(rollno_xpath)
                    rollno.send_keys(cur_roll_no)

                    sem = Select(driver.find_element_by_xpath(sem_xpath))
                    sem.select_by_visible_text(_sem)

                    # download captcha image
                    captcha = driver.find_element_by_xpath(captcha_xpath)

                    captcha_src = captcha.get_attribute('src')

                    img_name = '{}/captcha{}.png'.format(IMG_DLD, cur_roll_no)

                    urllib.request.urlretrieve(
                        captcha_src, img_name)

                    captcha_text = od.Captcha_detection(img_name)

                    # delete img after use
                    os.remove(img_name)

                    captcha_text = captcha_text if captcha_text is not None else 'EMPTY'
                    print(captcha_text)
                    captcha_field = driver.find_element_by_xpath(
                        captcha_field_xpath)
                    captcha_field.clear()
                    captcha_field.send_keys(captcha_text)

                    # click submit button
                    submit = driver.find_element_by_xpath(submit_xpath)
                    
                    #wait for 1 seconds
                    time.sleep(0.6)

                    submit.click()

                except:
                    # switch back to old window
                    driver.switch_to.window(driver.window_handles[0])

                    try:
                        reset = driver.find_element_by_xpath(reset_xpath)
                        if reset:
                            reset.click()
                        captcha_decoded = True
                    except:
                        # switch back to old window
                        driver.switch_to.window(driver.window_handles[0])

                try:
                    student = Student_Local()

                    # finding student details

                    st_name = driver.find_element_by_xpath(st_name_xpath)
                    student.name = st_name.text if st_name.text is not None else ''

                    st_rollno = driver.find_element_by_xpath(
                        st_rollno_xpath)
                    student.rollno = st_rollno.text if st_rollno.text is not None else ''

                    st_branch = driver.find_element_by_xpath(
                        st_branch_xpath)
                    student.branch = st_branch.text if st_branch.text is not None else ''

                    st_status = driver.find_element_by_xpath(
                        st_status_xpath)
                    student.status = st_status.text if st_status.text is not None else ''

                    st_res_des = driver.find_element_by_xpath(
                        st_res_des_xpath)
                    student.res_des = st_res_des.text if st_res_des.text is not None else ''

                    student.course = COURSE
                    student.sem = SEM

                    st_sgpa = driver.find_element_by_xpath(st_sgpa_xpath)
                    student.sgpa = st_sgpa.text if st_sgpa.text is not None else ''

                    student.display()

                    # save student in Student & Result
                    stud.name = student.name
                    stud.save()
                    res = Result(student=stud, sem=_sem, branch=student.branch, status=student.status,
                                 res_des=student.res_des, sgpa=student.sgpa, res_type=_res_type)
                    res.save()
                    captcha_decoded = True

                    # reset form

                    reset = driver.find_element_by_xpath(reset_xpath)
                    reset.click()

                except:
                    # switch back to old window
                    driver.switch_to.window(driver.window_handles[0])
                    pass

        cur_roll_no = roll_no_part1 + str(int(cur_roll_no[6:]) + 1).upper()
    driver.quit()

# launch instance of firefox
# binary = FirefoxBinary('/etc/firefox/firefox') # for linux


def find_result(COURSE, CLG_CODE, BRANCH, ROLL_START, ROLL_END, SEM, IMG_DLD):
    driver = webdriver.Chrome(chrome_driver)
    driver.get(url)

    # select course
    btech_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]/label'
    btech = driver.find_element_by_xpath(btech_xpath)
    btech.click()

    for number in range(ROLL_START, ROLL_END + 1):

        captcha_decoded = False

        while not captcha_decoded:

            try:
                studentNo = CLG_CODE + BRANCH + str(number)

                rollno = driver.find_element_by_xpath(rollno_xpath)
                rollno.send_keys(studentNo)

                sem = Select(driver.find_element_by_xpath(sem_xpath))
                sem.select_by_visible_text(SEM)

                # download captcha image
                captcha = driver.find_element_by_xpath(captcha_xpath)

                captcha_src = captcha.get_attribute('src')
                urllib.request.urlretrieve(
                    captcha_src, '{}/captcha'.format(IMG_DLD) + studentNo + '.png')

                captcha_text = od.Captcha_detection(
                    '{}/captcha{}.png'.format(IMG_DLD, studentNo))

                captcha_text = captcha_text if captcha_text is not None else 'EMPTY'
                print(captcha_text)

                # time.sleep(2)

                # fill captcha

                captcha_field = driver.find_element_by_xpath(
                    captcha_field_xpath)
                captcha_field.clear()
                captcha_field.send_keys(captcha_text)

                if captcha_text == '':
                    print("EMPTY CAPTCHA")

                # click submit button

                submit = driver.find_element_by_xpath(submit_xpath)
                submit.click()

            except:
                # time.sleep(2)
                # reset form

                reset = driver.find_element_by_xpath(reset_xpath)
                if reset:
                    reset.click()
                captcha_decoded = True

            try:
                student = Student()

                # finding student details

                st_name = driver.find_element_by_xpath(st_name_xpath)
                student.name = st_name.text if st_name.text is not None else ''

                st_rollno = driver.find_element_by_xpath(st_rollno_xpath)
                student.rollno = st_rollno.text if st_rollno.text is not None else ''

                st_branch = driver.find_element_by_xpath(st_branch_xpath)
                student.branch = st_branch.text if st_branch.text is not None else ''

                student.course = COURSE
                student.sem = SEM

                st_sgpa = driver.find_element_by_xpath(st_sgpa_xpath)
                student.sgpa = st_sgpa.text if st_sgpa.text is not None else ''

                student.display()

                # write_row(student)

                captcha_decoded = True

                # reset form

                reset = driver.find_element_by_xpath(reset_xpath)
                reset.click()

            except:
                pass


if __name__ == "__main__":
    # find_result(COURSE, CLG_CODE, BRANCH, ROLL_START, ROLL_END, SEM, IMG_DLD)
    generate_result("M", "BTECH", "5", "0101CS171055", "2")
