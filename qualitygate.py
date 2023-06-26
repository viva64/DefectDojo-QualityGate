from defectdojo_api import defectdojo_apiv2 as defectdojo
import sys

host = 'http://localhost:8080/'
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
user = 'admin'

def sum_severity(findings):
    severity = [0,0,0,0,0]
    for finding in findings.data["results"]:
        if finding["severity"] == "Critical":
            severity[0] = severity[0] + 1
        if finding["severity"] == "High":
            severity[1] = severity[1] + 1
        if finding["severity"] == "Medium":
            severity[2] = severity[2] + 1
        if finding["severity"] == "Low":
            severity[3] = severity[3] + 1

    return severity

def quality_gate(severity):
    gateway = [0,10,50,150] #Quality Gate by severity: Critical High Medium Low
    health = True
    for i in range(4):
        if(severity[i]> gateway[i]):
            health = False
    
    print("Quality Gate Status: " +  ("Success", "Failed")[health])   
    sys.exit((0, 1)[health])

class Main:
    dd = defectdojo.DefectDojoAPIv2(host, api_key, user, debug=False)
    tests = dd.list_tests(sys.argv[1])
    last_test_id = tests.data['results'][-1]['id']

    findings = dd.list_findings(test_id_in=last_test_id, limit=sys.maxsize, duplicate="false", is_mitigated="false")
    severity = sum_severity(findings)
    
    quality_gate(severity)
    
