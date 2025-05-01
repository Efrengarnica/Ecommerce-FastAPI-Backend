import pytest   #pip install pytest ya que no es nativo, una vez intalado creas tu carpeta test.
from uuid import UUID
from pydantic import ValidationError
from models.user import User, Role 

#PYTHONPATH=. pytest tests/models/test_user_model.py le dice a python que tome en donde estoy como referencia para ejecutar pytest.

# Aquí se prueba que cuando no se pasen todos los valores del modelo se creen de manera automática los que estan por default.
def test_user_crea_id_por_defecto_y_valores_por_defecto():
    # Solo pasamos los campos obligatorios
    u = User(name="Alice", email="alice@example.com", password="s3cr3t")

    # id debe ser un UUID generado automáticamente
    assert isinstance(u.id, UUID)

    # age es opcional y no lo pasamos → debe ser None
    assert u.age is None

    # role por defecto debe ser Role.client
    assert u.role == Role.client

# Aqui se prueba que de verdad se asignan de manera correcta cada valor.
def test_user_asigna_campos_personalizados():
    u = User(
        name="Bob",
        email="bob@example.com",
        password="abc123",
        age=30,
        role=Role.admin
    )
    assert u.name == "Bob"
    assert u.email == "bob@example.com"
    assert u.password == "abc123"
    assert u.age == 30
    assert u.role == Role.admin
        
# Aqui se prueba que se lance un error si se pasa un rol que no es.
@pytest.mark.parametrize("bad_role", ["superuser", 123, None])
def test_user_role_invalido_lanza_error(bad_role):
    data = {
        "name": "Pepe",
        "age": 30,
        "email": "pepe@example.com",
        "role": bad_role,
    }
    with pytest.raises(ValidationError):
        User.model_validate(data)

#Aquí se prueba que se lance un error si la edad no es como esta en el modelo.
@pytest.mark.parametrize("bad_age", ["hd", 25.5])
def test_user_age_invalido_lanza_error(bad_age):
    # age debe ser int o None
    data = {
            "name":"Dave",
            "email":"dave@example.com",
            "password":"pw",
            "age":bad_age
    }
    
    with pytest.raises(ValidationError):
        User.model_validate(data)