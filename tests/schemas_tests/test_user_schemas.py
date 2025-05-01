import pytest   #pip install pytest ya que no es nativo, una vez intalado creas tu carpeta test.
from uuid import UUID
# A pesar de que no lo interprete es necesario para que cuando use PYTHONPATH=$(pwd)/app pytest tests/schemas_tests/test_user_schemas.py
# le diga a python que tome como referencia la carpeta app, cabe aclarar que pytest tests/schemas_tests/test_user_schemas.py es tomado
# pero basandose en la carpeta en la que estoy parado y no en la carpeta app.
from schemas.user import UserCreate, UserResponse, UserPatch, UserPut, UserLogin, UserPassword
from models.user import Role 


#PYTHONPATH=. pytest tests/models/test_user_model.py le dice a python que tome en donde estoy como referencia para ejecutar pytest.

# Importante: las pruebas relacionadas a comprobar que se lanza un error cuando se le pasa otro tipo de dato a un atributo esas no se hacen
# se confia en Pydantic.


# Apartado que verifica que se crean los atributos que no se pasan cuando se crea una instancia.
# UserCreate
def test_user_create_crea_age_por_defecto():
    """ Se usa para probar que el schema crea un age None cuando no le pasamos nada. """
    # Solo pasamos los campos obligatorios
    u = UserCreate(name="Alice", email="alice@example.com", password="s3cr3t")
    
    # age es opcional y no lo pasamos → debe ser None
    assert u.age is None

# UserPatch
def test_user_patch_crea_valores_por_defecto():
    """ Se usa para probar que el schema crea los valores por defecto que deberia de crear. """
    # Solo pasamos los campos obligatorios
    u = UserPatch()
    
    assert u.name is None
    assert u.email is None
    assert u.age is None
    assert u.password is None
    
    
# Apartado para verificar que se asignan las cosas de manera correcta.
# UserCreate
def test_user_create_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserCreate(
        name="Bob",
        email="bob@example.com",
        age=30,
        password="abc123",
    )
    assert u.name == "Bob"
    assert u.email == "bob@example.com"
    assert u.age == 30
    assert u.password == "abc123"
        
# UserResponse
def test_user_response_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserResponse(
        id=UUID('52a86718-9706-45f4-ab5e-091e527909e1'),
        name="Bob",
        email="bob@example.com",
        age=30,
        role=Role.client
    )
    assert u.id == UUID('52a86718-9706-45f4-ab5e-091e527909e1')
    assert u.name == "Bob"
    assert u.email == "bob@example.com"
    assert u.age == 30
    assert u.role == Role.client
    
# UserPatch
def test_user_patch_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserPatch(
        name="Bob",
        email="bob@example.com",
        age=30,
        password = "contraseña"
    )
    assert u.name == "Bob"
    assert u.email == "bob@example.com"
    assert u.age == 30
    assert u.password == "contraseña"
    
# UserPut
def test_user_put_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserPut(
        id=UUID('52a86718-9706-45f4-ab5e-091e527909e1'),
        name="Bob",
        email="bob@example.com",
        age=30,
        password = "contraseña"
    )
    assert u.id == UUID('52a86718-9706-45f4-ab5e-091e527909e1')
    assert u.name == "Bob"
    assert u.email == "bob@example.com"
    assert u.age == 30
    assert u.password == "contraseña"
    
# UserLogin
def test_user_login_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserLogin(
        email="bob@example.com",
        password = "contraseña"
    )
    assert u.email == "bob@example.com"
    assert u.password == "contraseña"
    
# UserPassword
def test_user_password_asigna_campos_personalizados():
    """ Verifica que se asignen de manera correcta las cosas."""
    u = UserPassword(
        passwordActual="actual",
        passwordNuevo = "nueva"
    )
    assert u.passwordActual == "actual"
    assert u.passwordNuevo == "nueva"