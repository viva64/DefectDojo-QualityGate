from defectdojo_api import defectdojo_apiv2 as defectdojo
import datetime
import argparse

def upload_report(host, api_key, user, engagement_id, report):

    dd = defectdojo.DefectDojoAPIv2(host, api_key, user, debug=False)
    now = datetime.datetime.now()
    scanner = "Generic Findings Import"
    dd.upload_scan(engagement_id, scanner, report, active=False, verified=False, close_old_findings=False, skip_duplicates=False, scan_date=now.strftime("%Y-%m-%d"))


class Main:
    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='DefectDojo report uploader')
        parser.add_argument('--host', help="DefectDojo Hostname", required=True)
        parser.add_argument('--api_key', help="API Key", required=True)
        parser.add_argument('--user', help="User", required=True)
        parser.add_argument('--engagement', help="Engagement ID", required=True)
        parser.add_argument('--report', help="Path to report", required=True)
        
        args = vars(parser.parse_args())
        host = args["host"]
        api_key = args["api_key"]
        user = args["user"]
        engagement_id = args["engagement"]
        report = args["report"]
        
        upload_report(host, api_key, user, engagement_id, report)
        
#Launch exaple python .\upload.py --host 'http://localhost:8080/' --api_key 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' --user admin --engagement 6 --report "D:\dojo\report.defectdojo.json"