import requests, sys, argparse, os

host = os.environ['DD_HOST']
headers = {'Authorization' : 'Token '+ os.environ['DD_API_TOKEN'], 'accept':'application/json'}

def sum_severity(findings):
    severity = [0,0,0,0,0]
    for finding in findings:
        if finding["severity"] == "Critical":
            severity[0] = severity[0] + 1
        if finding["severity"] == "High":
            severity[1] = severity[1] + 1
        if finding["severity"] == "Medium":
            severity[2] = severity[2] + 1
        if finding["severity"] == "Low":
            severity[3] = severity[3] + 1

    return severity

def quality_gate(severity, critical=0, high=0, Medium=0,Low=0):
    gateway = [critical,high,Medium,Low] #Quality Gate by severity
    health = True
    for i in range(4):
        if(severity[i]> int(gateway[i])):
            health = False
    print("Critical: "+str(severity[0])+" High: "+str(severity[1])+" Medium: "+str(severity[2])+" Low: "+ str(severity[3]))
    print("Quality Gate Status: " +  ("Failed","Success")[health])   
    sys.exit((1,0)[health])

def last_test(engagement_id):
    test_rq = host + 'api/v2/tests/'
    payload = {'engagement':engagement_id, 'o':'-updated', 'limit':'1'}
    request = requests.get(test_rq, params=payload, headers=headers)

    return request.json()['results'][0]['id']

def findings(engagement_id):
    findings_rq = host + 'api/v2/findings/'
    payload = {'test':last_test(engagement_id), 'false_p':'false', 'limit':10000000}
    request = requests.get(findings_rq, params=payload, headers=headers)
    
    return request.json()['results']


class Main:
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='DefectDojo report uploader')
        parser.add_argument('--engagement', help="Engagement ID", required=True)
        parser.add_argument('--critical', help="Quality Gate Critical Warnings Level", required=False)
        parser.add_argument('--high', help="Quality Gate High Warnings Level", required=False)
        parser.add_argument('--medium', help="Quality Gate Medium Warnings Level", required=False)
        parser.add_argument('--low', help="Quality Gate Low Warnings Level", required=False)
        
        args = vars(parser.parse_args())
        engagement_id = args["engagement"]
        critical = args["critical"]
        high = args["high"]
        medium = args["medium"]
        low = args["low"]
        
        severity = sum_severity(findings(engagement_id))
    
        quality_gate(severity, critical, high, medium, low)
#Launch example python ./qualitygate.py --engagement 6 --critical 0 --high 10 --medium 50 --low 250
        
