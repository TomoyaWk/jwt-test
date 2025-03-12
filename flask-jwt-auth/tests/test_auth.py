import json
import pytest
from src.models.user import User

def test_register(client):
    """Test user registration"""
    response = client.post('/auth/register', 
                           data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                           content_type='application/json')
    assert response.status_code == 201
    assert b'User created successfully' in response.data

def test_login(client):
    """Test user login"""
    # Register a user first
    register_result = client.post('/auth/register', 
                data=json.dumps({'username': 'testuser', 'password': 'password123'}),
                content_type='application/json')
    
    assert register_result.status_code == 201
    assert b'User created successfully' in register_result.data

    
    # Test login
    response = client.post('/auth/login',
                          data=json.dumps({'username': 'testuser', 'password': 'password123'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in json.loads(response.data)

    # Test bad pass
    bad_pass_response = client.post('/auth/login',
                          data=json.dumps({'username': 'testuser', 'password': 'badpassword'}),
                          content_type='application/json')
    assert bad_pass_response.status_code == 401 
    assert b'Bad username or password' in bad_pass_response.data


def test_protected_route(client):
    """Test protected route access"""
    # Register and login to get token
    client.post('/auth/register', 
                data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                content_type='application/json')
    response = client.post('/auth/login',
                          data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                          content_type='application/json')
    token = json.loads(response.data)['access_token']
    
    # Test protected route with token
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/auth/protected', headers=headers)
    assert response.status_code == 200
    
    # Test without token
    response = client.get('/auth/protected')
    assert response.status_code == 401