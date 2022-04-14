# import requests
# from fastapi import status
# from fastapi.testclient import TestClient
#
# from src.api import app
#
# client: requests.Session = TestClient(app)
#
# anvdev_user = {
#     'id': 28631927,
#     'login': 'anvdev',
#     'name': 'Ivan Titov'
# }
#
#
# def test_user():
#     response = client.put('/v1/users', json=anvdev_user)
#     assert response.status_code == status.HTTP_201_CREATED
#
#     response = client.get('/v1/users')
#     assert response.json() == [anvdev_user]
#
#     response = client.delete(f'/v1/users/{anvdev_user["id"]}')
#     assert response.status_code == status.HTTP_200_OK
#
#     response = client.get('/v1/users')
#     assert response.json() == []


import psycopg2
def drop():
    con = psycopg2.connect(
      database="postgres",
      user="serafim",
      password="1234",
      host="127.0.0.1",
      port="5439"
    )

    cur = con.cursor()
    #cur.execute('''SELECT * FROM public.stats''')
    cur.execute('''TRUNCATE TABLE public.stats''')
    # rezult = cur.fetchall()
    # print(rezult)
    con.commit()
    #con.close()