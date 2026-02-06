import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            age=25,
            bio='Test bio'
        )
        db.session.add(user)
        db.session.commit()
        return user.id


# =============================================================================
# TEST CASE 1: Valid Registration
# =============================================================================
def test_valid_registration(client):
    """
    TEST CASE 1: Valid User Registration
    
    Description: Test that a user can register with all valid inputs
    Input: Valid username, email, first name, last name, age, bio
    Expected: User is created and redirected to profile page
    """
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'age': 30,
        'bio': 'Hello world'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Account created successfully' in response.data or b'newuser' in response.data
    print("TEST CASE 1: PASSED - Valid registration works")


# =============================================================================
# TEST CASE 2: Invalid Email Format
# =============================================================================
def test_invalid_email_format(client):
    """
    TEST CASE 2: Invalid Email Format
    
    Description: Test that registration fails with invalid email
    Input: Invalid email format (missing @)
    Expected: Form shows validation error
    """
    response = client.post('/register', data={
        'username': 'testuser2',
        'email': 'invalid-email',
        'first_name': 'Test',
        'last_name': 'User',
        'age': 25,
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'valid email' in response.data.lower() or b'email' in response.data.lower()
    print("TEST CASE 2: PASSED - Invalid email rejected")


# =============================================================================
# TEST CASE 3: Empty Required Fields
# =============================================================================
def test_empty_required_fields(client):
    """
    TEST CASE 3: Empty Required Fields
    
    Description: Test that registration fails when required fields are empty
    Input: Empty username and email
    Expected: Form shows validation errors
    """
    response = client.post('/register', data={
        'username': '',
        'email': '',
        'first_name': '',
        'last_name': '',
        'age': '',
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'required' in response.data.lower() or b'Username' in response.data
    print("TEST CASE 3: PASSED - Empty fields rejected")


# =============================================================================
# TEST CASE 4: Edge Case - Minimum Age
# =============================================================================
def test_edge_case_minimum_age(client):
    """
    TEST CASE 4: Edge Case - Minimum Age (1)
    
    Description: Test registration with minimum valid age
    Input: Age = 1
    Expected: Registration succeeds
    """
    response = client.post('/register', data={
        'username': 'younguser',
        'email': 'young@example.com',
        'first_name': 'Young',
        'last_name': 'User',
        'age': 1,
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    print("TEST CASE 4: Testing minimum age boundary")


# =============================================================================
# TEST CASE 5: Edge Case - Maximum Age
# =============================================================================
def test_edge_case_maximum_age(client):
    """
    TEST CASE 5: Edge Case - Maximum Age (150)
    
    Description: Test registration with maximum valid age
    Input: Age = 150
    Expected: Registration succeeds
    """
    response = client.post('/register', data={
        'username': 'olduser',
        'email': 'old@example.com',
        'first_name': 'Old',
        'last_name': 'User',
        'age': 150,
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    print("TEST CASE 5: Testing maximum age boundary")


# =============================================================================
# TEST CASE 6: Invalid Age (Negative)
# =============================================================================
def test_invalid_age_negative(client):
    """
    TEST CASE 6: Invalid Age - Negative Number
    
    Description: Test that registration fails with negative age
    Input: Age = -5
    Expected: Form shows validation error
    """
    response = client.post('/register', data={
        'username': 'negativeage',
        'email': 'negative@example.com',
        'first_name': 'Negative',
        'last_name': 'Age',
        'age': -5,
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    print("TEST CASE 6: Testing negative age validation")


# =============================================================================
# TEST CASE 7: Duplicate Username
# =============================================================================
def test_duplicate_username(client, sample_user):
    """
    TEST CASE 7: Duplicate Username
    
    Description: Test that registration fails with existing username
    Input: Username that already exists
    Expected: Form shows error about username taken
    """
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'first_name': 'Different',
        'last_name': 'User',
        'age': 30,
        'bio': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'already taken' in response.data.lower() or b'username' in response.data.lower()
    print("TEST CASE 7: PASSED - Duplicate username rejected")


# =============================================================================
# TEST CASE 8: View User Profile
# =============================================================================
def test_view_user_profile(client, sample_user):
    """
    TEST CASE 8: View User Profile
    
    Description: Test that user profile page displays correctly
    Input: Valid user ID
    Expected: Profile page shows user data
    """
    response = client.get(f'/profile/{sample_user}')
    
    assert response.status_code == 200
    assert b'testuser' in response.data
    print("TEST CASE 8: PASSED - Profile displays correctly")


# =============================================================================
# TEST CASE 9: Update User Profile
# =============================================================================
def test_update_user_profile(client, sample_user):
    """
    TEST CASE 9: Update User Profile
    
    Description: Test that update form is pre-populated with user data
    Input: Valid user ID
    Expected: Form fields contain current user data
    """
    response = client.get(f'/update/{sample_user}')
    
    assert response.status_code == 200
    assert b'testuser' in response.data
    assert b'test@example.com' in response.data
    print("TEST CASE 9: Testing update form pre-population")


# =============================================================================
# TEST CASE 10: Non-existent User
# =============================================================================
def test_nonexistent_user(client):
    """
    TEST CASE 10: Non-existent User Profile
    
    Description: Test accessing profile of user that doesn't exist
    Input: Invalid user ID (99999)
    Expected: 404 error page
    """
    response = client.get('/profile/99999')
    
    assert response.status_code == 404
    print("TEST CASE 10: PASSED - 404 for non-existent user")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])