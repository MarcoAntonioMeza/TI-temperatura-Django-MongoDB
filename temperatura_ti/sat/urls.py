from django.urls import path
from . import views


urlpatterns = [
    #Url para  el inicio de la aplicacion inicio
    path('', views.index, name='index'),
    #url para el login 
    path('login', views.login, name='login'),

    #url para el crud de personal
    path('personal',views.personal, name= 'personal'),
    path('personal/crear',views.crear_personal, name='crear_personal'),
    path('personal/actualizar', views.actualizar_personal, name='actualizar_personal'),
    path('personal/actualizar<str:nombre>', views.actualizar_personal, name='actualizar_personal'),

    #url para grupos
    path('grupos',views.grupos, name='grupos'),
    path('grupos/crear',views.grupo_crear, name='crear_grupo'),
    path('grupos/editar', views.actualizar_grupo, name='editar_grupo'),
    path('personal/editar<str:id>', views.actualizar_grupo, name='editar_grupo'),


    #url para crud de estudiantes
    path('estudiantes', views.estudiante, name='estudiantes'),
    path('estudiantes/crear',views.crear_estudiante, name ='crear_estudiante'),
    path('estudiantes/editar', views.editar_estudiante, name="editar_estudiante"),
    path('estudiantes/editar<str:matricula>', views.editar_estudiante, name="editar_estudiante"),

    #url para docentes
    path('grupos-tic',views.inicio_personal,name='grupos-tic')



    #path('nosotros' ,views.index ,name='nosotros'),
    #path('libros', views.libros, name='libros'),
    #path('libros/crear',views.crear, name='crear'),
    #path('libros/editar', views.editar, name='editar'),
    #path('libros/editar/<int:id>', views.editar, name='editar'),
    #path('eliminar/<int:id>',views.eliminar, name='eliminar'),
]