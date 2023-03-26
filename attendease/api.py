import frappe
import base64
from frappe.utils import flt, get_files_path, get_site_name, now, add_to_date, get_datetime, add_to_date, validate_email_address
from frappe.core.doctype.user.user import test_password_strength
import re

@frappe.whitelist(allow_guest=True)
def generate_otp(mobile_no):
    if not mobile_no :
        frappe.local.response["message"] = {
            "status": False,
            "message": "Invalid Mobile Number"
        }
        return
    
    user_email = frappe.db.get_all('User', filters={'mobile_no': mobile_no}, fields=['email'])
    if not user_email:
        frappe.local.response["message"] = {
            "status": False,
            "message": "User does not exits"
        }
        return 

    try:
        otp = "1234"
        # otp = str(random.randint(1000,9999))
        # msisdn = mobile_no #frappe.generate_hash("", 10)
        # text = f"You OTP {otp}"

        # callback_url = frappe.db.get_single_value("Geo Settings", "sms_call_back_url")
        # url = frappe.db.get_single_value("Geo Settings", "sms_base_url")
        # app_id = frappe.db.get_single_value("Geo Settings", "sms_app_id")
        # app_key = frappe.db.get_single_value("Geo Settings", "sms_app_key")

        # sms_payload = {
        #     "msisdn": msisdn,
        #     "text": text,
        #     "callback_url": callback_url,
        #     "premium": True
        # }
        # sms_headers = {
        #     "accept": "application/json",
        #     "App-ID": app_id,
        #     "API-Key": app_key,
        #     "content-type": "application/json"
        # }
        # r = requests.post(url, json=sms_payload, headers=sms_headers)

        # if r.status_code != 201:
        #     frappe.local.response["message"] = {
        #         "status": False,
        #         "message": json.loads(r.text)["message"]
        #     }
        #     return
        doc = frappe.get_doc({
            "doctype": "OTP Auth",
            "mobile_number": mobile_no,
            "otp": otp,
        })

        doc.insert(ignore_permissions=True)
        doc.save()
        frappe.db.commit()
        
        frappe.local.response["message"] = {
        "status": True,
        "message": 'OTP SENT'
        }

        return

    except Exception as e:
        return e

@frappe.whitelist(allow_guest=True)
def validate_otp(mobile_no, otp):

    if not mobile_no or not otp:
        frappe.local.response["message"] = {
            "status": False,
            "message": "invalid inputs"
        }
        return
    
    x_user = frappe.get_all('OTP Auth', filters={'mobile_number': mobile_no, 'otp': otp}, fields=["*"], order_by= 'creation desc')

    # if x_user[0].otp != otp:
    #     frappe.local.response["message"] = {
    #         "status": False,
    #         "message": "Invalid OTP"
    #     }
    #     return

    if x_user:
        otp_valid_upto = frappe.db.get_single_value('Attendease Settings', 'otp_valid_upto')
        expiry_time = add_to_date(x_user[0].creation, seconds=flt(otp_valid_upto))

        if get_datetime(now()) > get_datetime(expiry_time):
            frappe.local.response["message"] = {
                "status": False,
                "message": "Time Out, Your OTP Expired"
            }
            return

    if not x_user:
        frappe.local.response["message"] = {
            "status": False,
            "message": "Invalid Otp, Please try again with correct otp"
        }
        return

    user_email = ""
    
    if x_user[0].otp == otp:

        user_exist = frappe.db.count("User",{'mobile_no': mobile_no})

        if user_exist > 0:

            userm = frappe.db.get_all('User', filters={'mobile_no': mobile_no}, fields=['*'])
            user_email = userm[0].name

            user_image = get_doctype_images('User', user_email, 1)
            _user_image =[]
            
            if user_image:
                _user_image = user_image[0]['image']
                userm[0].images = _user_image

            api_key, api_secret = generate_keys(user_email)
            frappe.local.response["message"] = {
                "status": True,
                "message": "User Already Exists",
                "data":{
                "api_key": api_key,
                "api_secret": api_secret,
                "first_name": userm[0].first_name,
                "last_name": userm[0].last_name,
                "mobile_no": userm[0].mobile_no,
                "email_id": userm[0].email,
                "role": userm[0].user_type,
                "image": _user_image
            }
            }
            return
            

        frappe.local.response["message"] = {
            "status": False,
            "message": "User Not Exists",
        }

@frappe.whitelist(allow_guest=True)
def reset_otp(mobile_no):
    generate_otp(mobile_no)

@frappe.whitelist()
def get_user_info(api_key, api_sec):
    # api_key  = frappe.request.headers.get("Authorization")[6:21]
    # api_sec  = frappe.request.headers.get("Authorization")[22:]
    doc = frappe.db.get_value(
        doctype='User',
        filters={"api_key": api_key},
        fieldname=["name"]
    )

    doc_secret = frappe.utils.password.get_decrypted_password('User', doc, fieldname='api_secret')

    if api_sec == doc_secret:
        user = frappe.db.get_value(
            doctype="User",
            filters={"api_key": api_key},
            fieldname=["name"]
        )
        return user
    else:
        return "API Mismatch"

@frappe.whitelist(allow_guest=True)
def generate_keys(user):
    user_details = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length=15)
    
    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    
    user_details.api_secret = api_secret

    user_details.flags.ignore_permissions = True
    user_details.save(ignore_permissions = True)
    frappe.db.commit()
    
    return user_details.api_key, api_secret

def get_doctype_images(doctype, docname, is_private):
    attachments = frappe.db.get_all("File",
        fields=["attached_to_name", "file_name", "file_url", "is_private"],
        filters={"attached_to_name": docname, "attached_to_doctype": doctype}
    )
    resp = []
    for attachment in attachments:
        # file_path = site_path + attachment["file_url"]
        x = get_files_path(attachment['file_name'], is_private=is_private)
        with open(x, "rb") as f:
            # encoded_string = base64.b64encode(image_file.read())
            img_content = f.read()
            img_base64 = base64.b64encode(img_content).decode()
            img_base64 = 'data:image/jpeg;base64,' + img_base64
        resp.append({"image": img_base64})

    return resp

def ng_write_file(data, filename, docname, doctype, file_type):
    try:
        filename_ext = f'/home/laxman/frappe-bench/sites/attendease/{file_type}/files/{filename}.png'
        base64data = data.replace('data:image/jpeg;base64,', '')
        imgdata = base64.b64decode(base64data)
        with open(filename_ext, 'wb') as file:
            file.write(imgdata)

        doc = frappe.get_doc(
            {
                "file_name": f'{filename}.png',
                "is_private": 0 if file_type == 'public' else 1,
                "file_url": f'/{file_type}/files/{filename}.png',
                "attached_to_doctype": doctype,
                "attached_to_name": docname,
                "doctype": "File",
            }
        )
        doc.flags.ignore_permissions = True
        doc.insert()
        frappe.db.commit()
        return doc.file_url

    except Exception as e:
        frappe.log_error(str(e))
        return e
    
    
@frappe.whitelist(allow_guest=True)
def clock_in():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    if frappe.request.method =="GET":
        employee_id = get_employee_from_userid(user_email)
        attendance_log = frappe.db.get_all("Attendance Log", fields=["name", "clock_in", "clock_out", "working_hours", "gps"], filters={"employee": employee_id})
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : attendance_log
        }
        return
    
    elif frappe.request.method == "POST":
        _data = frappe.request.json
        employee_id = get_employee_from_userid(user_email)
        
        if employee_id == False:
            frappe.response["message"] = {
                "status": False,
                "message": "User is not linked with Employee",
                "user_email": user_email
            }
            return
        
        log = frappe.db.get_all("Attendance Log", filters={"posting_date": frappe.utils.today(), "clock_out": ""}, fields=["name", "clock_in", "clock_out", "working_hours", "gps"], order_by='creation desc')
        if len(log) > 0:
            frappe.response["message"] = {
                "status":False,
                "message": "User Has Already Clocked In for the date",
                "data": log[0]
            }
            return
        
        doc = frappe.get_doc({
            "doctype":"Attendance Log",
            "posting_date": frappe.utils.nowdate(),
            "clock_in": frappe.utils.now(),
            "employee": employee_id
        })
        doc.insert()
        doc.save()
        frappe.db.commit()

        frappe.response["message"] = {
            "status":True,
            "message": "Clock in Success",
            "data": doc
        }
        return
    
    elif frappe.request.method == "PUT":
        payload = frappe.request.json
        doc = frappe.get_doc('Attendance Log', payload['name'])
        doc.clock_out = frappe.utils.now()

        doc.save(ignore_permissions=True)
        frappe.response["message"] = {
            "status":True,
            "message": "Updated Successfully",
        }
        
        return

@frappe.whitelist(allow_guest=True)
def clock_in_today():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    if frappe.request.method =="GET":
        employee_id = get_employee_from_userid(user_email)
        attendance_log = frappe.db.get_all("Attendance Log", fields=["name", "clock_in", "clock_out", "working_hours", "gps"], filters={"employee": employee_id, "posting_date": frappe.utils.today(), "clock_out": ""})
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : attendance_log
        }
        return


@frappe.whitelist(allow_guest=True)
def task():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    if frappe.request.method =="GET":
        employee_id = get_employee_from_userid(user_email)
        task = frappe.db.get_all("Task", fields=["*"], filters={"employee": employee_id})
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : task
        }
        return
    
    elif frappe.request.method == "POST":
        _data = frappe.request.json
        employee_id = get_employee_from_userid(user_email)
        
        if employee_id == False:
            frappe.response["message"] = {
                "status": False,
                "message": "User is not linked with Employee",
                "user_email": user_email
            }
            return
                
        doc = frappe.get_doc({
            "doctype":"Task",
            "type": _data.get("type"),
            "subject": _data.get("subject"),
            "status": _data.get("status"),
            "project": _data.get("project"),
            "expected_start_date": _data.get("expected_start_date"),
            "expected_end_date": _data.get("expected_end_date"),
            "completed_on": _data.get("completed_on"),
            "task_description": _data.get("task_description"),
            "employee": employee_id
        })
        doc.insert(ignore_permissions=True)
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.response["message"] = {
            "status":True,
            "message": "Task Added Success",
            "data": doc
        }
        return
    
    elif frappe.request.method == "PUT":
        payload = frappe.request.json
        doc = frappe.get_doc('Task', payload['name'])

        doc.save(ignore_permissions=True)
        frappe.response["message"] = {
            "status":True,
            "message": "Updated Successfully",
        }
        
        return

@frappe.whitelist(allow_guest=True)
def task_type():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    if frappe.request.method =="GET":
        task_type = frappe.db.get_all("Task Type", fields=["name"])
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : task_type
        }
        return

@frappe.whitelist(allow_guest=True)
def projects():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    if frappe.request.method =="GET":
        projects = frappe.db.get_all("Project", fields=["*"])
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : projects
        }
        return


@frappe.whitelist(allow_guest=True)
def dashboard():
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    employee_id = get_employee_from_userid(user_email)
        
    if employee_id == False:
        frappe.response["message"] = {
            "status": False,
            "message": "User is not linked with Employee",
            "user_email": user_email
        }
        return

    if frappe.request.method =="GET":
        
        tasks = frappe.db.sql("""
            SELECT
                CONCAT("Week-", WEEK(creation)) AS weekindex,
                (SELECT COUNT(creation) FROM tabTask WHERE employee = %s AND CONCAT("Week-", WEEK(creation)) = weekindex) total_task,
                (SELECT COUNT(creation) FROM tabTask WHERE employee = %s AND CONCAT("Week-", WEEK(creation)) = weekindex AND STATUS = 'Completed') completed_task,
                (SELECT COUNT(creation) FROM tabTask WHERE employee = %s AND CONCAT("Week-", WEEK(creation)) = weekindex AND STATUS <> 'Completed') pending_task
            FROM `tabTask`
            WHERE `employee` = %s
            GROUP BY weekindex
        """, (employee_id, employee_id, employee_id, employee_id), as_dict=1)
        
        planned = []
        completed = []
        
        if tasks:
            for t in tasks:
                planned.append({"x": t.weekindex, "y": t.total_task})

            for t in tasks:
                completed.append({"x": t.weekindex, "y": t.completed_task})

        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : {"planned": planned, "actual": completed}
        }
        return

@frappe.whitelist(allow_guest=True)
def birthdays():
    
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    employee_id = get_employee_from_userid(user_email)
        
    if employee_id == False:
        frappe.response["message"] = {
            "status": False,
            "message": "User is not linked with Employee",
            "user_email": user_email
        }
        return

    if frappe.request.method =="GET":
        
        employees = frappe.db.sql("""
            SELECT 
            e.name, e.first_name, e.last_name, e.full_name, e.gender, e.company, e.date_of_birth, e.date_of_joining, e.employment_type,
            e.mobile_no, e.user_id, e.emergency_contact_no
            FROM tabEmployee e
            LEFT JOIN `tabUser` u on u.name = e.user_id
            WHERE  DATE_ADD(date_of_birth, 
                            INTERVAL YEAR(CURDATE())-YEAR(date_of_birth)
                                    + IF(DAYOFYEAR(CURDATE()) > DAYOFYEAR(date_of_birth),1,0)
                            YEAR)  
                        BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """, as_dict=1)

        if employees:

            for e in employees:
                user_image = get_doctype_images('User', e.user_id, 1)
                
                if user_image:
                    e.image = user_image[0]['image']
                    
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : employees
        }
        return
    
@frappe.whitelist(allow_guest=True)
def new_joinees():
    
    api_key  = frappe.request.headers.get("Authorization")[6:21]
    api_sec  = frappe.request.headers.get("Authorization")[22:]

    user_email = get_user_info(api_key, api_sec)
    if not user_email:
        frappe.response["message"] = {
            "status": False,
            "message": "Unauthorised Access",
        }
        return

    employee_id = get_employee_from_userid(user_email)
        
    if employee_id == False:
        frappe.response["message"] = {
            "status": False,
            "message": "User is not linked with Employee",
            "user_email": user_email
        }
        return

    if frappe.request.method =="GET":
        
        employees = frappe.db.sql("""
            SELECT 
            e.name, e.first_name, e.last_name, e.full_name, e.gender, e.company, e.date_of_birth, e.date_of_joining, e.employment_type,
            e.mobile_no, e.user_id, e.emergency_contact_no
            FROM tabEmployee e
            LEFT JOIN `tabUser` u on u.name = e.user_id
            WHERE e.date_of_joining BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
        """, as_dict=1)

        if employees:

            for e in employees:
                user_image = get_doctype_images('User', e.user_id, 1)
                
                if user_image:
                    e.image = user_image[0]['image']
                    
        frappe.response["message"] = {
            "status":True,
            "message": "",
            "data" : employees
        }
        return

def get_employee_from_userid(email):
    employee = frappe.db.get_all("Employee", fields=["name"], filters={"user_id": email})
    if employee: 
        return employee[0].name
    else: 
        return False