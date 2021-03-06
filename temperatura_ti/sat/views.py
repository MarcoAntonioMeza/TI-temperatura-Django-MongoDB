from functools import total_ordering
from http.client import HTTPResponse
from typing import Collection
from unittest.case import doModuleCleanups
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bson.objectid import ObjectId 

from utils import get_db

# Create your views here.


def acceso(correo,contraseña):
    col_per = get_db('personal')
    filtro = {
        'inicio_sesion':{
            'correo':correo, 'contraseña':contraseña
            }
    }
    return  col_per.find_one(filtro,{ 'nombre':1, 'rol':1})

def intentar(request):
    try:
        rol = request.session['rol']
        return True
    except:
        return False



def index (request):
    return render(request, 'inicio/index.html')


def cerrar_sesion(request):
    try: 
        del request.session['rol']
        del request.session['nombre']
        return render(request, 'inicio/index.html')
    except:
        return render(request, 'inicio/index.html')




def login(request):
    if request.POST:
        datos = request.POST
        try:
            dic = acceso(datos['correo'],datos['contraseña'])
            request.session['rol'] = dic['rol']
            request.session['nombre'] = dic['nombre']
            print(request.session['rol'])
            if request.session['rol'] == 'Docente':
                return redirect('mis_grupos')
            
            elif request.session['rol'] == 'Director':
                return redirect('grupos-tic')
                
        except:
            return render(request, 'inicio/login.html',{"msg":"Coreo o contraseña incorrecto"})
            
    return render(request, 'inicio/login.html')

'''----------------------------------------- views para CRUD de personal-----------------------------------------'''

def personal(request):
    if  intentar(request) and request.session['rol'] == "Director":
        coleccion = get_db('personal')
        
        personal = coleccion.find({},{"nombre":1,"grado":1,"cargo":1})
        total_personal = coleccion.count_documents({})
        return render(request, 'personal/index.html',{'docentes' : personal, 'total': total_personal })
    else:
        return redirect('cierre-sesion')

def crear_personal(request):
    if  intentar(request) and request.session['rol'] == "Director":
        if request.POST:
            informacion = request.POST
            personal = {
                "nombre": f"{informacion['nombre']} {informacion['apellidos']}",
                "grado" : informacion['grado'],
                "inicio_sesion":{
                    "correo" : informacion['correo'],
                    "contraseña" : "1234"
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
    else:
        return redirect('cierre-sesion')

def actualizar_personal(request, nombre):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')
    


'''---------------------------------Views para grupo-----------------------------------------------------------'''

def grupos(request):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')
        

def grupo_crear(request):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')

def actualizar_grupo(request, id):
    if  intentar(request) and request.session['rol'] == "Director":
    
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
    else:
        return redirect('cierre-sesion')

'''//////////////////////////////////////////////CRUD estudiante//////////////////////////////////////////////////////'''
def estudiante(request):
    if  intentar(request) and request.session['rol'] == "Director":

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
    else:
        return redirect('cierre-sesion')


def crear_estudiante(request):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')

def editar_estudiante(request,matricula):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""

def inicio_personal(request):
    if  intentar(request) and request.session['rol'] == "Director":
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
    else:
        return redirect('cierre-sesion')

def ver_alunos_grupo(request,grupo):
    if  intentar(request) and request.session['rol'] == "Director":
        col_temp= get_db('temperatura')
        match = {'$match': {'grupo':grupo}}
        group = {'$group':{'_id': '$estudiante' , 'promedio':{'$avg': '$temperatura'}}}
        alumnos_promedio = col_temp.aggregate([match,group])
        alumnos = []
        for i in alumnos_promedio:
            alumnos.append(
                {
                    "nombre": i['_id'],
                    "promedio" : "{0:.2f}".format(i['promedio'])  
                }
            )
        datos_template  = { "grupo": grupo,"alumnos": alumnos}

        return render(request, "vista-personal/vista-alumnos.html",datos_template)
    else:
        return redirect('cierre-sesion')

def ver_alumnos_tutor(request):
    if  intentar(request) and request.session['rol'] == "Docente":
        docente = request.session['nombre']
        colec_grupos = get_db('grupos')
        grupos = colec_grupos.find({'tutor': docente},{'nombre':1})       
        total = colec_grupos.count_documents({'tutor': docente})
        alumnos = None
        datos_template = {
            'grupos': grupos,
            'total' : total,
            'alumnos' : alumnos
        }
        if request.POST:
            datos = request.POST

            col_temp= get_db('temperatura')
            match = {'$match': {'grupo':datos['grupo']}}
            group = {'$group':{'_id': '$estudiante' , 'promedio':{'$avg': '$temperatura'}}}

            alumnos_promedio = col_temp.aggregate([match,group])
            alumnos = []
            for i in alumnos_promedio:
                alumnos.append(
                    {
                        "nombre": i['_id'],
                        "promedio" : "{0:.2f}".format(i['promedio'])  
                    }
                )
            datos_template = {
            'grupos': grupos,
            'total' : total,
            'alumnos' : alumnos,
            'grupo' : datos['grupo']
            }

        return render(request,'vista-docente/index.html',datos_template)
    else:
        return redirect('cierre-sesion')