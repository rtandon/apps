import urllib2
import cookielib
import requests
from requests import Request , Session
import json

__author__ = 'rtandon'

#http://docs.python-requests.org/en/latest/user/advanced/#session-objects

#https://manage.syncapse-staging.com
#https://manage.syncapse-staging.com/posts/responses
#v.handa@syncapse.com / Testing.

ajax_request ="http://admin-platform.syncapse-staging.com/ajax_request/login"
auth_url = "http://admin-platform.syncapse-staging.com/ajax_request/login?username=v.handa@syncapse.com&password=Testing.&redirect=http%3A%2F%2Fwww.google.com%2F"
auth_url1 = "https://admin-platform.syncapse-staging.com/ajax_request/login?UserEmail=v.handa@syncapse.com&UserPassword=Testing.&redirect=http%3A%2F%2Fwww.google.com%2F"
auth_url2 = "http://platform.syncapse-staging.com/ajax_request/login?username=v.handa@syncapse.com&password=Testing.&redirect=http%3A%2F%2Fwww.google.com%2F"
auth_url3 = "https://sso-platform.syncapse-staging.com/ajax_request/login?username=v.handa@syncapse.com&password=Testing."
response_url = "https://manage.syncapse-staging.com/posts/responses"

def main2():
#http://stackoverflow.com/questions/10247054/http-post-and-get-with-cookies-for-authentication-in-python

    s1 = Session()
        
    prepped = Request('GET',  # or any other method, 'POST', 'PUT', etc.
                      auth_url3,
                      #data=data,
                      #headers=headers
                      # ...
                      ).prepare()

    resp = s1.send(prepped)
                      
    print '----------------'
    print 'Cookie Details  ==  ' + resp.request.headers['Cookie']
    print '----------------'    
    
#Not Working
    headers = {
               "Cookie" : resp.request.headers['Cookie'] + " ; company_guid=6f65b34d-b6f4-4abd-b14a-408b8a11029b"
              }    

#working : if this cookie expires then get the new one from browser
#    headers = {
#               "Cookie" : "AuthSession=aba1d850-5814-48f5-896f-2989609f02c5" + "; company_guid=6f65b34d-b6f4-4abd-b14a-408b8a11029b"
#              }    

    
#working
#    headers = {
#               "Cookie" : "AuthSession=aba1d850-5814-48f5-896f-2989609f02c5; company_guid=6f65b34d-b6f4-4abd-b14a-408b8a11029b"
#              }    

    print '----------------'
    print headers
    print '----------------'
    
    prepped = Request('GET',  # or any other method, 'POST', 'PUT', etc.
                      response_url,
                      #data=data,
                      headers=headers
                      # ...
                      ).prepare()
                      
    resp = s1.send(prepped)
                      
                      
#    print(resp.status_code)
#    print resp.text
    WriteToFile("/home/rtandon/Downloads/Work/0037_TP5952_TCCC Response Time/Requirements/Response_Time_Json_Sample3.txt", resp.text)
    print 'done'

#This code is working. 
#Copy the value of cookie from browser by logging into http://manage.syncapse-staging.com
def main3():
#http://stackoverflow.com/questions/10247054/http-post-and-get-with-cookies-for-authentication-in-python

    headers = {
               "Cookie" : "AuthSession=326d3f9e-15fa-491e-b8a8-a3fa5a8f6292; company_guid=6f65b34d-b6f4-4abd-b14a-408b8a11029b"
              }    
    
    
    s1 = Session()
    prepped = Request('GET',  # or any other method, 'POST', 'PUT', etc.
                      response_url,
                      #data=data,
                      headers=headers
                      # ...
                      ).prepare()
                      
    resp = s1.send(prepped)
                      
                      
    print(resp.status_code)
    print resp.text
    print 'doneeee'

#
#SUPPER ITS IS WORKING.
#
def main4():
#http://stackoverflow.com/questions/10247054/http-post-and-get-with-cookies-for-authentication-in-python
#auth_url3 = "https://sso-platform.syncapse-staging.com/ajax_request/login?username=v.handa@syncapse.com&password=Testing."
#response_url = "https://manage.syncapse-staging.com/posts/responses"
    s = requests.Session()
    r1 = s.get(auth_url3)
    print r1.headers
    
#working
    headers = {
               "Cookie" : r1.headers['set-cookie'] + " ; company_guid=6f65b34d-b6f4-4abd-b14a-408b8a11029b"
              }    

    s1 = Session()
    prepped = Request('GET',  # or any other method, 'POST', 'PUT', etc.
                      response_url,
                      #data=data,
                      headers=headers
                      # ...
                      ).prepare()
                      
    resp = s1.send(prepped)

    WriteToFile("/home/rtandon/Downloads/Work/importdata/TCCC_Response/Response_Time_Json_Sample3_main4.txt", resp.text)
       
#    print resp.text
    print 'done'
    
def main1():
    print 'hello world'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#    for cookie in cj:
#        print cookie

    httpReq = urllib2.Request(auth_url)
    page =  opener.open(response_url)
    print page.read()
    
    print 'done'

def WriteToFile(file_name, content):
    input_file = open(file_name, 'w')
    input_message = input_file.write(content)
    return True

def ReadFromFile(file_name):
    input_file = open(file_name, 'r')
    input_message = input_file.read()
    return input_message

def on_receive_message(json_msg):
    request_msg = None
    request_msg = json.loads(json_msg)
    return request_msg
    
def parse_json(json_response):
    print 'inside parse_json'
    i = 0
    for json_data in json_response['results']:
        print i
        i=i + 1
        if json_data.has_key('Post'):
            json_data['Post']['myxxxx_id'] = json_data['Post']['id']
            print json_data['Post']['id']
            print json_data['Post']
        pass
    pass
    
if __name__ == '__main__':
    main4()
#    msg = ReadFromFile("/home/rtandon/Downloads/Work/0037_TP5952_TCCC Response Time/Requirements/Response_Time_Json_Sample2.json")
#    json_msg=on_receive_message(msg)
#    parse_json(json_msg)
    print "done!!!"
    
    
