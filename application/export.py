import time

from celery.result import AsyncResult
from flask import request, jsonify, Response
from flask_security import auth_token_required

from application.tasks import get_csv_show, get_csv_theatre


@auth_token_required
def csv_push():
    obj = request.args.get('obj')
    print(obj)
    task = get_csv_show.delay(4) if obj == 'shows' else get_csv_theatre.delay(4)
    return jsonify({"task_id": task.id})


def status():
    task_id = request.args.get('task_id')
    print(task_id)

    def generate():
        while True:
            task = AsyncResult(task_id)
            if task.state == 'SUCCESS':
                yield "data: SUCCESS\n\n"
                break
            elif task.state == 'PENDING':
                yield "data: PENDING\n\n"
            else:
                yield "data: FAILED\n\n"
                break
            time.sleep(3)

    return Response(generate(), content_type='text/event-stream')


def get_csv():
    task_id = request.args.get('task_id')
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS':
        response = Response(task.result, content_type='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
        return response
    else:
        return {"status": "failed"}
