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
            "tutor": grupo['tutor']
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
            "tutor": datos['tutor']
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
    