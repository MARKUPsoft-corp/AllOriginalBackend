from django.db import migrations

# Fonction pour vérifier si Cloudinary est disponible
def is_cloudinary_available():
    try:
        from cloudinary.models import CloudinaryField
        return True
    except ImportError:
        return False

# Opérations conditionnelles en fonction de la disponibilité de Cloudinary
cloudinary_operations = []

if is_cloudinary_available():
    from cloudinary.models import CloudinaryField
    
    # Classe personnalisée pour convertir un champ ImageField en CloudinaryField
    class MigrateToCloudinaryField(migrations.operations.AlterField):
        def database_forwards(self, app_label, schema_editor, from_state, to_state):
            # Cette opération ne modifie pas réellement le schéma de base de données
            # Elle change simplement le type de champ dans le modèle Python
            pass
            
        def database_backwards(self, app_label, schema_editor, from_state, to_state):
            # Opération inverse - rien à faire au niveau de la base de données
            pass

    # Ajouter l'opération de migration du champ vers CloudinaryField
    cloudinary_operations.append(
        MigrateToCloudinaryField(
            model_name='productimage',
            name='image',
            field=CloudinaryField('image', folder='alloriginal/products', resource_type='image', verbose_name="Image"),
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_remove_product_stock'),
    ]

    operations = cloudinary_operations
