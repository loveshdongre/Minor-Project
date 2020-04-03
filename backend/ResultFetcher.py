import time
import cv2
import csv
import urllib.request
# from pytesseract import image_to_string
from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
# import ImageTweaker as io2
import object_detection_image as od

# Key variables
COURSE = 'BTech'
CLG_CODE = '0101'
BRANCH = 'CS'
ROLL_START = 171001
ROLL_END = 1710010  # 171117
SEM = '5'
IMG_DLD = 'img_download'


class Student:
    name = ''
    rollno = ''
    branch = ''
    course = ''
    sem = ''
    sgpa = ''

    def display(self):
        print('name:', self.name)
        print('rollno:', self.rollno)
        print('branch:', self.branch)
        print('course:', self.course)
        print('sem:', self.sem)
        print('sgpa:', self.sgpa)


def write_row(stud):
    with open('csv/resultcse.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([stud.rollno, stud.name, stud.sgpa,
                         stud.sem, stud.branch, stud.course])


# launch instance of firefox
# binary = FirefoxBinary('/etc/firefox/firefox') # for linux
def find_result(COURSE, CLG_CODE, BRANCH, ROLL_START, ROLL_END, SEM, IMG_DLD):
    driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    driver.get('http://www.uitrgpv.ac.in/Exam/ProgramSelect.aspx')

    # select course
    btech_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[5]/label'
    btech = driver.find_element_by_xpath(btech_xpath)
    btech.click()

    for number in range(ROLL_START, ROLL_END + 1):

        captcha_decoded = False

        while not captcha_decoded:

            try:
                studentNo = CLG_CODE + BRANCH + str(number)

                rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtrollno"]'
                rollno = driver.find_element_by_xpath(rollno_xpath)
                rollno.send_keys(studentNo)

                sem_xpath = '//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]'
                sem = Select(driver.find_element_by_xpath(sem_xpath))
                sem.select_by_visible_text(SEM)

                # download captcha image
                captcha_xpath = '/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr[1]/td/div/img'
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
                captcha_field_xpath = '//*[@id="ctl00_ContentPlaceHolder1_TextBox1"]'
                captcha_field = driver.find_element_by_xpath(
                    captcha_field_xpath)
                captcha_field.clear()
                captcha_field.send_keys(captcha_text)

                if captcha_text == '':
                    print("EMPTY CAPTCHA")

                # click submit button
                submit_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnviewresult"]'
                submit = driver.find_element_by_xpath(submit_xpath)
                submit.click()

            except:
                # time.sleep(2)
                # reset form
                reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
                reset = driver.find_element_by_xpath(reset_xpath)
                if reset:
                    reset.click()
                captcha_decoded = True

            try:
                student = Student()

                # finding student details
                st_name_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblNameGrading"]'
                st_name = driver.find_element_by_xpath(st_name_xpath)
                student.name = st_name.text if st_name.text is not None else ''

                st_rollno_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblRollNoGrading"]'
                st_rollno = driver.find_element_by_xpath(st_rollno_xpath)
                student.rollno = st_rollno.text if st_rollno.text is not None else ''

                st_branch_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblBranchGrading"]'
                st_branch = driver.find_element_by_xpath(st_branch_xpath)
                student.branch = st_branch.text if st_branch.text is not None else ''

                student.course = COURSE
                student.sem = SEM

                st_sgpa_xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblSGPA"]'
                st_sgpa = driver.find_element_by_xpath(st_sgpa_xpath)
                student.sgpa = st_sgpa.text if st_sgpa.text is not None else ''

                student.display()

                # write_row(student)

                captcha_decoded = True

                # reset form
                reset_xpath = '//*[@id="ctl00_ContentPlaceHolder1_btnReset"]'
                reset = driver.find_element_by_xpath(reset_xpath)
                reset.click()

            except:
                pass


if __name__ == "__main__":
    find_result(COURSE, CLG_CODE, BRANCH, ROLL_START, ROLL_END, SEM, IMG_DLD)
