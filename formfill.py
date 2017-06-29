#========================================
# Auto Denison Scheduler
#========================================

import re
import mechanize
import datetime

mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 1

#========================================
# Passwords and Pins
#========================================

student_id = "D********"
pin = "********"
alt_pin = "******"

#========================================
# Classes
#========================================

crn_1 = "*****"
crn_2 = "*****"
crn_3 = "*****"
crn_4 = "*****"
# *****
# Women's Studies - 40719
# Wicked Problems - 41110
# Operating Systems - 41012
# Cyber Ethics - 41190
# Ancient Rome - 41041
# Early British Literature - 40241
# ****

#========================================
# Scheduling Times
#========================================

time_1 = "20:00:01"
time_2 = "21:30:01"

#========================================

def main():
    while True:
        timestring = (datetime.datetime.now() + datetime.timedelta(seconds=30)).strftime("%H:%M:%S")
        if timestring == time_1:
            print "\n=========== Round 1 (" + time_1 + ") ===========\n"
            registerCourse(crn_1, crn_2, time_1)
            print "\n             *** SUCCESS ***"
        elif timestring == time_2:
            print "\n=========== Round 2 (" + time_2 + ") ===========\n"
            registerCourse(crn_3, crn_4, time_2)
            print "\n             *** SUCCESS ***\n"
            break
            
#========================================
# A Function To Register Denison Courses
#========================================
def registerCourse(course1, course2, time):
    print "Enter SSB:                ", datetime.datetime.now().strftime("%H:%M:%S.%f")
    
    br = mechanize.Browser()
    br.open("https://web4prod.denison.edu/pls/web4prod/bwskfreg.P_CheckAltPin")
    # follow second link with element text matching regular expression
    assert br.viewing_html()

    # Login Page
    br.select_form(name="loginform")
    br.form["sid"] = student_id
    br.form["PIN"] = pin
    br.submit()

    # Main Menu
    for link in br.links():
        if link.text == "Student Services":
            br.follow_link(link)
            break
            
    # Student Services
    for link in br.links():
        if link.text == "Registration":
            br.follow_link(link)
            break

    # Registration
    for link in br.links():
        if link.text == "Add or Drop Classes":
            br.follow_link(link)
            break

    # Select Term
    br.form = list(br.forms())[1]
    br.submit()

    print "Wait Before Alt Pin:      ", datetime.datetime.now().strftime("%H:%M:%S.%f")


    while True:
        if str(datetime.datetime.now().strftime("%H:%M:%S")) == time and int(datetime.datetime.now().microsecond) > 100000:
            print "Enter Alt Pin:            ", datetime.datetime.now().strftime("%H:%M:%S.%f")

            # Enter Alt Pin
            br.form = list(br.forms())[1]
            br.form['pin'] = alt_pin
            br.submit()
            
            try:
                # Enter CRNs
                print "Enter CRNs:               ", datetime.datetime.now().strftime("%H:%M:%S.%f")
                br.form = list(br.forms())[1]
                for control in br.form.controls:
                    if str(control.id) == "crn_id1":
                        control.value = course1
                    elif str(control.id) == "crn_id2":
                        control.value = course2
                br.submit()
                break
            except:
                print "Enter CRNs Failure:       ", datetime.datetime.now().strftime("%H:%M:%S.%f")
                br.follow_link("https://web4prod.denison.edu/pls/web4prod/bwskfreg.P_CheckAltPin")
                
                # Enter Alt Pin
                br.form = list(br.forms())[1]
                br.form['pin'] = alt_pin
                br.submit()
                
                br.form = list(br.forms())[1]
                for control in br.form.controls:
                    if str(control.id) == "crn_id1":
                        control.value = course1
                    elif str(control.id) == "crn_id2":
                        control.value = course2
                br.submit()
                break

    br.close()

    print "End:                      ", datetime.datetime.now().strftime("%H:%M:%S.%f")
    
main()
