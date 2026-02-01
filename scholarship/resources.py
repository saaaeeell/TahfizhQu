from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Student, Examiner, User
from django.contrib.auth.hashers import make_password

class StudentResource(resources.ModelResource):
    username = fields.Field(
        column_name='username',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Student
        fields = ('id', 'username', 'nama', 'email', 'nim', 'kampus', 'asal_sekolah', 'fakultas', 'jurusan', 'jumlah_hafalan', 'ipk', 'semester', 'tanggal_lahir', 'status_seleksi')
        export_order = fields
        import_id_fields = ('nim',) # Use NIM as unique identifier for import if ID is missing

    def before_import_row(self, row, **kwargs):
        username = row.get('username')
        email = row.get('email')
        
        if username and email:
            User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': make_password('password'),
                    'role': 'student',
                    'is_active': True 
                }
            )

class ExaminerResource(resources.ModelResource):
    username = fields.Field(
        column_name='username',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Examiner
        fields = ('id', 'username', 'nama', 'email', 'nomor_telepon')
        export_order = fields
        import_id_fields = ('email',)

    def before_import_row(self, row, **kwargs):
        username = row.get('username')
        email = row.get('email')
        
        if username and email:
            User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': make_password('password'),
                    'role': 'examiner',
                    'is_staff': True,
                    'is_active': True
                }
            )
