from flask import Flask, request, Response, jsonify

from .dao import SQLiteDAO, MySQLDAO
from .metrics import prometheus_middleware, get_latest_metrics

app = Flask(__name__)


@app.route('/v1/students_growth', methods=['GET'])
@prometheus_middleware
def get_students_growth():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    if start_year is None or end_year is None:
        return Response('invalid request', 400)

    # dao = SQLiteDAO()
    # dao.connect(db_path='data.db')

    dao = MySQLDAO()
    dao.connect(
        user='root',
        password='my-secret-pw',
        host='127.0.0.1',
        database='statistics',
        port=3306
    )
    students = dao.select_students_by_gender(start_year, end_year)
    return jsonify({'counts': students})


@app.route('/v1/graduates_degree', methods=['GET'])
@prometheus_middleware
def get_graduates_degree():
    year = request.args.get('year', type=int)
    if year is None:
        return Response('invalid request', 400)

    # dao = SQLiteDAO()
    # dao.connect(db_path='data.db')

    dao = MySQLDAO()
    dao.connect(
        user='root',
        password='my-secret-pw',
        host='127.0.0.1',
        database='statistics',
        port=3306
    )
    try:
        graduates = dao.select_graduates_by_degree(year)
    except KeyError:
        return Response(f'year {year} not found', 404)

    return jsonify(graduates)


@app.route('/metrics')
def metrics():
    return get_latest_metrics()


def main():
    # dao = SQLiteDAO()
    # dao.connect(db_path='data.db')

    dao = MySQLDAO()
    dao.connect(
        user='root',
        password='my-secret-pw',
        host='127.0.0.1',
        database='statistics',
        port=3306
    )
    app.dao = dao
    app.run()


if __name__ == '__main__':
    main()
