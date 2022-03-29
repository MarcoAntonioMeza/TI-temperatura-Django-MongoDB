from http.client import HTTPResponse
from typing import Collection
from unittest.case import doModuleCleanups
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bson.objectid import ObjectId 

from utils import get_db

# Create your views here.

def index (request):
    return render(request, 'inicio/index.html')

def login(request):
    if request.POST:
        print(request.POST)
    return render(request, 'inicio/login.html')

'''----------------------------------------- views para CRUD de personal-----------------------------------------'''

def personal(request):
    coleccion = get_db('personal')
    
    personal = coleccion.find({},{"nombre":1,"grado":1,"cargo":1})
    total_personal = coleccion.count_documents({})
    return render(request, 'personal/index.html',{'docentes' : personal, 'total': total_personal })

def crear_personal(request):
    if request.POST:
        informacion = request.POST
        personal = {
            "nombre": f"{informacion['nombre']} {informacion['apellidos']}",
            "grado" : informacion['grado'],
            "inicio_sesion":{
                "correo" : informacion['correo'],
                "contraseña" : informacion['contraseña']
            },
            "cargo": informacion['cargo'],
            "rol": informacion['rol']
        }
        coleccion_personal = get_db('personal')
        coleccion_personal.insert_one(personal)
        return redirect('personal')

    #Documentos para mostar los cargos 
    coleccion = get_db('cargo')
    cargos = coleccion.find()
    return render (request, 'personal/crear.html',{"cargos": cargos})

def actualizar_personal(request, nombre):
    coleccion = get_db('personal')
    if request.POST:
        datos = request.POST
        json = {
            "nombre": datos['nombre'],
            "grado" : datos['grado'],
            "cargo" : datos['cargo']
        }
        coleccion.update_one({"nombre":datos['nombre']},{"$set":json})
        return redirect('personal')

    docente = coleccion.find_one({"nombre": nombre})
    coleccion = get_db('cargo')
    cargos = coleccion.find()
    return render(request,'personal/actualizar.html',{'docente': docente, 'cargos': cargos})


'''---------------------------------Views para grupo-----------------------------------------------------------'''

def grupos(request):
    #id = "62411478b074e76446ea01c9"
    #objInstance = ObjectId(id) 
    coleccion = get_db('grupos')
    grupos = coleccion.find()
    lista_grupos =[]
    for i in grupos:
        lista_grupos.append(
            {
                "id":i['_id'],
                "grado": i['grado'],
                "grupo": i['grupo'],
                "tutor": i['tutor']
            }
        )
    return render(request,'grupo/index.html',{"grupos":lista_grupos})

def grupo_crear(request):
    if request.POST:
        grupo = request.POST
        json = {
            "grado": grupo['grado'],
            "grupo": grupo['grupo'].upper(),
            "tutor": grupo['tutor'],
            "nombre" : f"{grupo['grado']}° '{grupo['grupo'].upper()}'"
        }
        coleccion = get_db('grupos')
        coleccion.insert_one(json)

        return redirect('grupos')

    collections = get_db('personal')
    tutores = collections.find({},{"nombre":1})
    return render(request,'grupo/crear-grupo.html',{'tutores':tutores})

def actualizar_grupo(request, id):
    coleccion_grupo = get_db('grupos')

    if request.POST:
        datos = request.POST
        json = {
            "grado" : datos['grado'],
            "grupo" : datos['grupo'].upper(),
            "tutor": datos['tutor'],
            "nombre" : f"{datos['grado']}° '{datos['grupo'].upper()}'"
        }
        coleccion_grupo.update_one({"_id":ObjectId(datos['id'])},{"$set":json})
        return redirect('grupos')

        
    
    objeto_id = ObjectId(id)
    grupo = coleccion_grupo.find_one({"_id": objeto_id})
    grupo_final = {
        "id": grupo['_id'],
        "grupo" : grupo['grupo'],
        "grado" : grupo['grado'],
        "tutor" : grupo['tutor']
    }
    collections = get_db('personal')
    tutores = collections.find({},{"nombre":1})
    return render(request,"grupo/editar-grupo.html",{'tutores':tutores,'grupo': grupo_final})

'''//////////////////////////////////////////////CRUD estudiante//////////////////////////////////////////////////////'''
def estudiante(request):

    colec_estudiantes = get_db('estudiantes')
    estudiantes_col = colec_estudiantes.find({},{"_id":0})
    estudiantes = []
    for i in estudiantes_col:
        estudiantes.append(
            {   
                "nombre": i['nombre'],
                "matricula": i['matricula'],
                "grupo" : i['grupo']
            }
        )

    return render(request,'estudiante/index.html',{"estudiantes": estudiantes})


def crear_estudiante(request):
    if request.POST:
        info = request.POST
        estudiante = {
            "matricula": info['matricula'],
            "nombre" : f"{info['nombre']} {info['apellidos']}",
            "grupo": info['grupo']
        }
        colec_estudiante = get_db('estudiantes')
        colec_estudiante.insert_one(estudiante)
        return redirect('estudiantes')

    coleccion = get_db('grupos')
    grupos = coleccion.find({},{"nombre":1})
    return render(request,"estudiante/crear.html",{"grupos": grupos})

def editar_estudiante(request,matricula):
    col_estudiante = get_db('estudiantes')
    if request.POST:
        datos = request.POST
        student = {
            "nombre": datos['nombre'],
            "grupo": datos['grupo']
        }
        col_estudiante.update_one({"matricula":datos['matricula']},{"$set":student})
        return redirect('estudiantes')

    estudiante = col_estudiante.find_one({"matricula": matricula},{"_id":0})
    coleccion = get_db('grupos')
    grupos = coleccion.find({},{"nombre":1})
    return render(request,"estudiante/editar.html",{"grupos": grupos, "estudiante": estudiante})

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""

def inicio_personal(request):
    colec_grupos = get_db('temperatura')
    grupos = colec_grupos.aggregate([{'$group':{'_id': '$grupo' , 'promedio':{'$avg': '$temperatura'}}}])
    grupos_formato = []
    for i in grupos:
        grupos_formato.append(
            {
                "nombre": i['_id'],
                "promedio" : "{0:.2f}".format(i['promedio'])
            }
        )
    return render(request,'vista-personal/index.html',{'grupos':grupos_formato})