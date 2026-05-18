from django.shortcuts import render
import json
import os
from django.http import JsonResponse
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def load_data(filename):
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

@csrf_exempt
def reporters_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            reporter = Reporter(
                data['id'],
                data['name'],
                data['email'],
                data['team']
            )

            reporter.validate()

            reporters = load_data('reporters.json')
            reporters.append(reporter.to_dict())


            save_data('reporters.json', reporters)

            return JsonResponse(reporter.to_dict(), status=201)
        
        except ValueError as e:
            return JsonResponse({'error':str(e)}, status=400)



            
    elif request.method == 'GET':
        reporters = load_data('reporters.json')

        reporter_id = request.GET.get('id')

        if reporter_id:
            for reporter in reporters:
                if reporter['id'] == int(reporter_id):
                    return JsonResponse(reporter, status=200)
            
            return JsonResponse({'error':'Reporter not found'}, status=404)
        

        return JsonResponse(reporters, safe=False, status=200)
    

@csrf_exempt
def issues_view(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            #check if reporter exists
            reporters = load_data('reporters.json')

            reporter_exists = any(
                reporter['id'] == data['reporter_id']
                for reporter in reporters    
            )

            if not reporter_exists:
                return JsonResponse(
                    {'error': 'Reporter not found'},
                    status = 404
                )
            
            #create correct issue type based on priority 
            if data['priority'] == 'critical':
                issue = CriticalIssue(
                    data['id'],
                    data['title'],
                    data['description'],
                    data['status'],
                    data['priority'],
                    data['reporter_id']
                )

            elif data['priority'] == 'low':
                issue = LowPriorityIssue(
                    data['id'],
                    data['title'],
                    data['description'],
                    data['status'],
                    data['priority'],
                    data['reporter_id']
                )

            else:
                issue = Issue(
                    data['id'],
                    data['title'],
                    data['description'],
                    data['status'],
                    data['priority'],
                    data['reporter_id']
                )

            #validate issue
            issue.validate()

            #load existing issues
            issues = load_data('issues.json')

            #save new issue
            issues.append(issue.to_dict())

            save_data('isues.json', issues)


            #adding custom message
            response_data = issue.to_dict()
            response_data['message'] = issue.describe()


            return JsonResponse(response_data, status=201)
        
        except(ValueError,KeyError, json.JSONDecodeError) as e:
            return JsonResponse(
                {'error':str(e)},
                status=400
            )
        

    elif request.method == 'GET':
        
        issues = load_data('issues.json')

        #get single issue by id
        issue_id = request.GET.get('id')

        if issue_id:
            for issue in issues:
                if issue['id'] == int(issue_id):
                    return JsonResponse(issue, status=200)

            return JsonResponse(
                {'error': 'Issue not found'},
                status = 404
            ) 
        
        #filtering by satatus
        status_filter = request.GET.get('status')

        if status_filter:
            filtered_issues = [
                issue for issue in issues
                if issue['status'] == status_filter
            ]

            return JsonResponse(
                filtered_issues,
                safe=False,
                status=200
            )
        
    #return all isuues
    return JsonResponse(
        issues,
        safe=False,
        status=200
    )

