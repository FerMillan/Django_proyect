import reuniones

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from django.core.paginator import Paginator
from datetime import datetime

# Reportes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Models
from .models import Documento, Reunion
from .models import Participante
from users.models import Usuarios

# Forms
from .form import DocumentoForm, ReunionForm, ReunionFormUpdate
from .form import ParticipanteForm

# Filter
from .filters import BuscarReunion

# CRUD Reuniones

@login_required(login_url="/accounts/login/")
def lista_reuniones(request, *args, **kwargs):
    
    reuniones = Reunion.objects.all()
    zero = reuniones.count()

    usuarioT = Usuarios.usuario.field

    buscar = BuscarReunion(request.GET, queryset=reuniones)
    reuniones = buscar.qs
    time = str(datetime.now())[0:16]

    num_valores_por_pagina = 10

    paginator = Paginator(reuniones, num_valores_por_pagina)
    page_number = request.GET.get('page')
    reuniones_page = paginator.get_page(page_number)

    num_reuniones = 0

    for i in reuniones:
        num_reuniones += 1

    num_pages = num_reuniones/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    reporte_v = 0

    if request.method == 'POST' and 'reporte' in request.POST:
        # llamamos a la funcion que genera los reportes
        reporte(reuniones)
        reporte_v = 1
    else:
        reporte_v = 0
    
    context = {'reuniones': reuniones, 
                'buscar':buscar, 
                'zero':zero, 
                'usuarioT':usuarioT, 
                'time':time,
                'reuniones_page':reuniones_page,
                'num_pages':num_pages,
                'reporte_v':reporte_v}
        
    return render(request, 'reuniones.html', context)

@login_required(login_url="/accounts/login/")
def calendario_semana(request, *args, **kwargs):
    
    reuniones = Reunion.objects.all()

    usuarioT = Usuarios.usuario.field

    buscar = BuscarReunion(request.GET, queryset=reuniones)
    reuniones = buscar.qs
    time = str(datetime.now())[0:16]

    mes_actual = int(time[5:7])
    año_actual = int(time[0:4])
    dia_actual = int(time[8:10])

    mes = 0
    año = 0
    dia = 0

    mod = 0

    print(f'Dia Actual: {dia_actual}\nMes Actual: {mes_actual}\nAño actual: {año_actual}')

    if (mes_actual == 4) or (mes_actual == 6) or (mes_actual == 9) or (mes_actual == 11):
        mod = 30
    elif (mes_actual == 1) or (mes_actual == 3) or (mes_actual == 5) or (mes_actual == 7) or (mes_actual == 8) or (mes_actual == 10) or (mes_actual == 12):
        mod = 31
    elif (mes_actual == 2):
        mod = 28
    elif (mes_actual == 2) and es_bisiesto(año_actual):
        mod = 29

    semana = reuniones_calendario(7, time, mod, reuniones)

    num_semana = len(semana)

    num_valores_por_pagina = 10

    paginator = Paginator(semana, num_valores_por_pagina)
    page_number = request.GET.get('page')
    reuniones_page = paginator.get_page(page_number)

    num_reuniones = 0

    for i in reuniones:
        num_reuniones += 1

    num_pages = num_reuniones/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    context = {'reuniones': reuniones, 
                'buscar':buscar, 
                'usuarioT':usuarioT, 
                'time':time,
                'reuniones_page':reuniones_page,
                'num_pages':num_pages,
                'semana':semana,
                'num_semana':num_semana}

    if request.method == 'POST' and 'reporte' in request.POST:
        # llamamos a la funcion que genera los reportes
        reporte(reuniones)
        
    return render(request, 'calendario.html', context)


@login_required(login_url="/accounts/login/")
def calendario_semana_home(request, *args, **kwargs):
    
    reuniones = Reunion.objects.all()

    usuarioT = Usuarios.usuario.field

    buscar = BuscarReunion(request.GET, queryset=reuniones)
    reuniones = buscar.qs
    time = str(datetime.now())[0:16]

    mes_actual = int(time[5:7])
    año_actual = int(time[0:4])
    dia_actual = int(time[8:10])

    mes = 0
    año = 0
    dia = 0

    mod = 0

    # print(f'Dia Actual: {dia_actual}\nMes Actual: {mes_actual}\nAño actual: {año_actual}')

    if (mes_actual == 4) or (mes_actual == 6) or (mes_actual == 9) or (mes_actual == 11):
        mod = 30
    elif (mes_actual == 1) or (mes_actual == 3) or (mes_actual == 5) or (mes_actual == 7) or (mes_actual == 8) or (mes_actual == 10) or (mes_actual == 12):
        mod = 31
    elif (mes_actual == 2):
        mod = 28
    elif (mes_actual == 2) and es_bisiesto(año_actual):
        mod = 29

    semana = reuniones_calendario(7, time, mod, reuniones)

    num_semana = len(semana)

    num_valores_por_pagina = 10

    paginator = Paginator(semana, num_valores_por_pagina)
    page_number = request.GET.get('page')
    reuniones_page = paginator.get_page(page_number)

    num_reuniones = 0

    for i in reuniones:
        num_reuniones += 1

    num_pages = num_reuniones/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    context = {'reuniones': reuniones, 
                'buscar':buscar, 
                'usuarioT':usuarioT, 
                'time':time,
                'reuniones_page':reuniones_page,
                'num_pages':num_pages,
                'semana':semana,
                'num_semana':num_semana}

    if request.method == 'POST' and 'reporte' in request.POST:
        # llamamos a la funcion que genera los reportes
        reporte(reuniones)
        
    return render(request, 'home.html', context)

@login_required(login_url="/accounts/login/")
def calendario_2_semanas(request, *args, **kwargs):
    
    reuniones = Reunion.objects.all()

    usuarioT = Usuarios.usuario.field

    buscar = BuscarReunion(request.GET, queryset=reuniones)
    reuniones = buscar.qs
    time = str(datetime.now())[0:16]

    mes_actual = int(time[5:7])
    año_actual = int(time[0:4])
    dia_actual = int(time[8:10])

    mod = 0

    print(f'Dia Actual: {dia_actual}\nMes Actual: {mes_actual}\nAño actual: {año_actual}')

    if (mes_actual == 4) or (mes_actual == 6) or (mes_actual == 9) or (mes_actual == 11):
        mod = 30
    elif (mes_actual == 1) or (mes_actual == 3) or (mes_actual == 5) or (mes_actual == 7) or (mes_actual == 8) or (mes_actual == 10) or (mes_actual == 12):
        mod = 31
    elif (mes_actual == 2):
        mod = 28
    elif (mes_actual == 2) and es_bisiesto(año_actual):
        mod = 29

    quincena = reuniones_calendario(14, time, mod, reuniones)

    num_quincena = len(quincena)

    num_valores_por_pagina = 10

    paginator = Paginator(quincena, num_valores_por_pagina)
    page_number = request.GET.get('page')
    reuniones_page = paginator.get_page(page_number)

    num_reuniones = 0

    for i in reuniones:
        num_reuniones += 1

    num_pages = num_reuniones/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    context = {'reuniones': reuniones, 
                'buscar':buscar, 
                'usuarioT':usuarioT, 
                'time':time,
                'reuniones_page':reuniones_page,
                'num_pages':num_pages,
                'quincena':quincena,
                'num_quincena':num_quincena}

    if request.method == 'POST' and 'reporte' in request.POST:
        # llamamos a la funcion que genera los reportes
        reporte(reuniones)
        
    return render(request, 'calendario_2_semanas.html', context)

@method_decorator(login_required, name='dispatch')
class AgregarReunion(View):
    template = 'crear_reunion.html'

    def get(self, request):
        formReunion = ReunionForm()
        context = {'formReunion':formReunion}
        return render(request, self.template, context)

    def post(self, request):
        formReunion = ReunionForm(request.POST, request.FILES)

        if not formReunion.is_valid():
            context = {'formReunion': formReunion}
            return render(request, self.template, context)

        mes_form = int(str(formReunion.cleaned_data['fecha'])[5:7])

        if mes_form == 1:
            mes_m = Reunion.MES.ENERO
        elif mes_form == 2:
            mes_m = Reunion.MES.FEBRERO
        elif mes_form == 3:
            mes_m = Reunion.MES.MARZO
        elif mes_form == 4:
            mes_m = Reunion.MES.ABRIL
        elif mes_form == 5:
            mes_m = Reunion.MES.MAYO
        elif mes_form == 6:
            mes_m = Reunion.MES.JUNIO
        elif mes_form == 7:
            mes_m = Reunion.MES.JULIO
        elif mes_form == 8:
            mes_m = Reunion.MES.AGOSTO
        elif mes_form == 9:
            mes_m = Reunion.MES.SEPTIEMBRE
        elif mes_form == 10:
            mes_m = Reunion.MES.OCTUBRE
        elif mes_form == 11:
            mes_m = Reunion.MES.NOVIEMBRE
        elif mes_form == 12:
            mes_m = Reunion.MES.DICIEMBRE

        Reunion.objects.create(
            folio=formReunion.cleaned_data['folio'],
            fecha=formReunion.cleaned_data['fecha'],
            mes = mes_m,
            año = str(formReunion.cleaned_data['fecha'])[0:4],
            inicio=formReunion.cleaned_data['inicio'],
            termino=formReunion.cleaned_data['termino'],
            lugar=formReunion.cleaned_data['lugar'],
            asunto=formReunion.cleaned_data['asunto'],
            observaciones=formReunion.cleaned_data['observaciones'],
            usuario=request.user,
        )

        rid = Reunion.objects.last()
        
        return redirect(f'/reuniones/agregar/participantes/{rid.folio}')

@method_decorator(login_required, name='dispatch')  
class BorrarReunion(DeleteView):
    model = Reunion
    template_name = 'borrar_reunion.html'
    success_url = '/reuniones'

@login_required(login_url='/accounts/login/')
def editar_reunion(request, pk):

    reunion = Reunion.objects.get(folio=pk)
    form = ReunionFormUpdate(instance=reunion)
    context = {'form': form}
    if request.method == 'POST':
        form = ReunionFormUpdate(request.POST, request.FILES, instance=reunion)
        if form.is_valid():
            # guardar reunion en la BD
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            return redirect('reuniones:list')
        # else:
        #     error="Revisa que las horas tengan coherencia"
        #     context = {'form': form,'error':error}
    return render(request, 'editar_reunion.html', context)

# CRUD Participantes

@method_decorator(login_required, name='dispatch')
class ParticipantesView(View):
    
    template = 'participantes.html'

    def get(self, request, pk):
        'GET method.'
        participantes = Participante.objects.all()
        documentos = Documento.objects.all()
        reunion = Reunion.objects.get(folio=pk)
        #dc = str(Documento.objects.get(reunion=pk))

        context = {'participantes': participantes, 'reunion': reunion, 'documentos':documentos, }
        return render(request, self.template, context)

@method_decorator(login_required, name='dispatch')
class AgregarParticipante(View):
    template = 'agregar_participante.html'

    def get(self, request, pk):
        formParticipante = ParticipanteForm()
        reunion = Reunion.objects.get(folio=pk)
        context = {'formParticipante':formParticipante, 'reunion':reunion}
        return render(request, self.template, context)

    def post(self, request, pk):
        reunion = Reunion.objects.get(folio=pk)
        formParticipante = ParticipanteForm(request.POST, request.FILES, instance=reunion)

        if not formParticipante.is_valid():
            context = {'formParticipante': formParticipante}
            return render(request, self.template, context)
        
        if formParticipante.is_valid():
            # guardar reunion en la BD
            instance = formParticipante.save(commit=False)
            instance.usuario = request.user
            instance.save()

        Participante.objects.create(
            nombre=formParticipante.cleaned_data['nombre'],
            apellido_p=formParticipante.cleaned_data['apellido_p'],
            apellido_m=formParticipante.cleaned_data['apellido_m'],
            instituto=formParticipante.cleaned_data['instituto'],
            email=formParticipante.cleaned_data['email'],
            # (Campo del modelo que tendrá la informacion) = 
            # (ID de la reunion a la que se asignan los participantes)
            reunion=reunion,
        )
        return redirect(f'/reuniones/participantes/{reunion.folio}')

@method_decorator(login_required, name='dispatch')  
class BorrarParticipante(View):
    def post(self, request, pk, fk):
        participante = Participante.objects.get(id=pk)
        participante.delete()
        return redirect(f'/reuniones/participantes/{fk}')


@login_required(login_url='/accounts/login/')
def editar_participante(request, pk, fk):

    reunion = Reunion.objects.get(folio=fk)
    participante = Participante.objects.get(id=pk)
    form = ParticipanteForm(instance=participante)
    context = {'form': form, 'reunion':reunion}
    if request.method == 'POST':
        form = ParticipanteForm(
            request.POST, request.FILES, instance=participante)
        if form.is_valid():
            # guardar reunion en la BD
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            return redirect(f'/reuniones/participantes/{fk}')
    return render(request, 'editar_participante.html', context)

# CRUD Documento de Reunion

@method_decorator(login_required, name='dispatch')  
class BorrarDocumento(View):
    def post(self, request, pk, fk):
        documento = Documento.objects.get(id=pk)
        documento.delete()
        return redirect(f'/reuniones/participantes/{fk}')

@method_decorator(login_required, name='dispatch')
class AgregarDocumento(View):
    template = 'agregar_documento.html'

    def get(self, request, pk):
        formDoc = DocumentoForm()
        reunion = Reunion.objects.get(folio=pk)
        context = {'formDoc':formDoc, 'reunion':reunion}
        return render(request, self.template, context)

    def post(self, request, pk):
        reunion = Reunion.objects.get(folio=pk)
        formDoc = DocumentoForm(request.POST, request.FILES, instance=reunion)

        if not formDoc.is_valid():
            context = {'formDoc': formDoc}
            return render(request, self.template, context)
        
        if formDoc.is_valid():
            # guardar documento en la BD
            instance = formDoc.save(commit=False)
            instance.usuario = request.user
            instance.save()

        Documento.objects.create(
            documento=formDoc.cleaned_data['documento'],
            reunion=reunion,
        )
        return redirect(f'/reuniones/participantes/{reunion.folio}')

# Funcion Auxiliar que dice si un Año es bisiesto
def es_bisiesto(año):
    if (año % 100) == 0 and (año % 400) == 0:
        return True
    elif (año % 4) == 0:
        return True
    else:
        return False

# Funcion que separa por dias las reuniones para el calendario
def reuniones_calendario(dias, time, mod, reuniones):
    reuniones_dias = []
    dia_actual = int(time[8:10])
    mes_actual = int(time[5:7])

    for r in reuniones:
        dia_r = int(str(r.fecha)[8:10])
        mes_r = int(str(r.fecha)[5:7])

        if (dia_actual+dias) < mod:
            if int(dia_r) > int(dia_actual+dias):
                pass
            elif dia_r <= (dia_actual+dias) and dia_r >= dia_actual: 
                if mes_actual < mes_r :
                    pass
                elif (mes_actual == 12) and (mes_r == 1):
                    pass
                else:
                    reuniones_dias.append(r)
        
        elif (dia_actual+dias) > mod:
            mes = (mes_actual + 1) % 12
        
            if (dia_r <= mod and dia_r >= dia_actual) or (dia_r <= ((dia_actual+dias) % mod) and mes_r == mes):
                reuniones_dias.append(r)
    
    return reuniones_dias

# Funcion que Genera un pdf con los oficios
def reporte(data):
    w,h = letter
    
    time = str(datetime.now())[0:16]

    c = canvas.Canvas(f'static/pdf/reportes/reuniones/Reporte-Reuniones - {time}.pdf', pagesize=letter)
    # c = canvas.Canvas(f'static/pdf/reportes/reuniones/Reporte-Reuniones.pdf', pagesize=letter)

    c.setFont('Helvetica-Bold', 20)

    c.drawString(w/2-100, h - 75,'Reporte - Reuniones')

    generar_cabecera(c,h)
    # c.setLineWidth(.2)
    c.line(50,50,w-50,50)

    # Lineas para formar el cuadrado de los titulos de las columnas
    c.line(45,h-130,w-45,h-130)
    c.line(45,h-130,45,h-95)
    c.line(w-45,h-130,w-45,h-95)
    c.line(45,h-95,w-45,h-95)

    # Lineas que dividen las columnas en los titulos
    c.line(87,h-130,87,h-95)
    c.line(187,h-130,187,h-95)
    c.line(251,h-130,251,h-95)
    c.line(307,h-130,307,h-95)
    c.line(367,h-130,367,h-95)
    c.line(461,h-130,461,h-95)

    linea = h-145

    for d in data:
        c.setFont('Helvetica',10)

        ### Colocación de Datos del atributo Folio
        # c.drawString(50,linea, str(d.folio))

        ### Colocación de Datos del atributo Fecha
        c.drawString(194, linea, str(d.fecha))
        
        ### Colocación de Datos del atributo Hora de Inicio
        inicio = int(str(d.inicio)[0:2])
        if (inicio > 12):
            c.drawString(260, linea, str(inicio-12)+str(d.inicio)[2:5]+' p.m.')
        else:
            c.drawString(260, linea, str(d.inicio)[0:5]+' a.m.')

        ### Colocación de Datos del atributo Hora de Termino
        termino = int(str(d.termino)[0:2])
        if (termino > 12):
            c.drawString(314, linea, str(termino-12)+str(d.termino)[2:5]+' p.m.')
        else:
            c.drawString(314, linea, str(d.termino)[0:5]+' a.m.')
        
        ### Colocación de Datos del atributo Lugar, Asunto y Observaciones

        len = 0
        linAsunto = linea
        linLugar = linea
        linObs = linea
        linFolio = linea
    
        finAsunto = 0
        finLugar = 0
        finObs = 0
        finFolio = 0

        lenAsunto = 0
        for i in str(d.asunto):
            lenAsunto += 1
        
        lenLugar = 0
        for i in str(d.lugar):
            lenLugar += 1

        lenObs = 0
        for i in str(d.observaciones):
            lenObs+= 1

        lenFolio = 0
        for i in str(d.folio):
            lenFolio+= 1

        # print("Longitud Asunto: "+str(lenAsunto))
        # print("Longitud Lugar: "+str(lenLugar))

        for a in range(max([lenAsunto,lenLugar,lenObs])):
            
            len+=1

            if len > lenAsunto:
                pass

            elif(len == lenAsunto):
                restantesAsunto = lenAsunto - finAsunto
                c.drawString(90, linAsunto, str(d.asunto)[lenAsunto-restantesAsunto:lenAsunto])
                linAsunto-=15

                if (linAsunto <= 52):
                    c.showPage()
                    linObs = h-145
                    linAsunto = h-145
                    linLugar = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

            elif((len % 16) == 0):
                finAsunto = len
                c.drawString(90, linAsunto, str(d.asunto)[finAsunto-16:len]+'-')
                linAsunto-=15

                if (linAsunto <= 52):
                    c.showPage()
                    linObs = h-145
                    linAsunto = h-145
                    linLugar = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)
            

            if len > lenLugar:
                pass

            elif (len == lenLugar):
                restantesLugar = lenLugar - finLugar
                c.drawString(375, linLugar, str(d.lugar)[lenLugar-restantesLugar:lenLugar])
                linLugar-=15

                if (linLugar <= 52):
                    c.showPage()
                    linObs = h-145
                    linAsunto = h-145
                    linLugar = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

            elif((len % 14) == 0):
                finLugar = len
                c.drawString(375, linLugar, str(d.lugar)[finLugar-14:len]+'-')
                linLugar-=15

                if (linLugar <= 52):
                    c.showPage()
                    linObs = h-145
                    linAsunto = h-145
                    linLugar = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

            if len > lenObs:
                pass

            elif (len == lenObs):
                restantesObs = lenObs - finObs
                c.drawString(467, linObs, str(d.observaciones)[lenObs-restantesObs:lenObs])
                linObs-=15

                if (linObs <= 52):
                    c.showPage()
                    linObs = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

            elif((len % 17) == 0):
                finObs = len
                c.drawString(467, linObs, str(d.observaciones)[finObs-17:len]+'-')
                linObs-=15

                if (linObs <= 52):
                    c.showPage()
                    linObs = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)
            
            if len > lenFolio:
                pass

            elif (len == lenFolio):
                restantesObs = lenFolio - finFolio
                c.drawString(50, linFolio, str(d.folio)[lenFolio-restantesObs:lenFolio])
                linFolio-=15

                if (linFolio <= 52):
                    c.showPage()
                    linFolio = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

            elif((len % 6) == 0):
                finFolio = len
                c.drawString(50, linFolio, str(d.folio)[finFolio-6:len]+'-')
                linFolio-=15

                if (linFolio <= 52):
                    c.showPage()
                    linFolio = h-145

                    generar_cabecera(c,h)
                    c.setFont('Helvetica',10)
                    c.setLineWidth(.2)
                    c.line(50,50,w-50,50)

        linea = min([linAsunto, linLugar, linObs, linFolio])
        c.line(45,linea+7,w-45,linea+7)
        linea -= 5
    
    c.line(45,linea+12,45,h-130)
    c.line(w-45,linea+12,w-45,h-130)

    c.line(87,linea+12,87,h-130)
    c.line(187,linea+12,187,h-130)
    c.line(251,linea+12,251,h-130)
    c.line(307,linea+12,307,h-130)
    c.line(367,linea+12,367,h-130)
    c.line(461,linea+12,461,h-130)

    c.line(50,45,w-50,45)

    c.drawImage('static/img/logounam.jpg', 60, h-85, 70, 70)
    c.drawImage('static/img/cigu.jpg', w-170, h-85, 110, 70)
    c.drawImage('static/img/pormiraza.jpg', w-370, h-50, 100, 30)

    c.save()

def generar_cabecera(c,h):

    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, h - 110, 'Folio')
    c.drawString(120, h - 110, 'Asunto')
    c.drawString(202, h - 110, 'Fecha')
    c.drawString(257, h - 110, 'Hora de')
    c.drawString(264, h - 125, 'Inicio')
    c.drawString(314, h - 110, 'Hora de')
    c.drawString(312, h - 125, 'Termino')
    c.drawString(390, h - 110, 'Lugar de')
    c.drawString(390, h - 125, 'Reunion')
    c.drawString(470, h - 110, 'Observaciones')
    

########################## POR SI SE VUELVE A UTILIZAR (BORRAR AL TERMINAR EL PROYECTO)






# elif len < 16 and len == lenLugar:
            #     # lin+=10
            #     c.drawString(375, linea, str(d.lugar))
            #     # lin-=10

            #     if (linLugar <= 52):
            #         c.showPage()
            #         linLugar = h-145

            #         generar_cabecera(c,h)
            #         c.setLineWidth(.2)
            #         c.line(50,50,w-50,50)
            
            # if((len % 16) == 0):
            #     finLugar = len
            #     c.drawString(375, linea, str(d.lugar)[finLugar-16:len]+'-')
            #     linea-=15

            #     if (linea <= 52):
            #         c.showPage()
            #         linea = h-145

            #         generar_cabecera(c,h)
            #         c.setLineWidth(.2)
            #         c.line(50,50,w-50,50)

            # elif(len == lenLugar):
            #     restantes = lenLugar - finLugar
            #     c.drawString(375, linea, str(d.lugar)[lenLugar-restantes:lenLugar])
            #     linea-=15

            #     if (linea <= 52):
            #         c.showPage()
            #         linea = h-145

            #         generar_cabecera(c,h)
            #         c.setLineWidth(.2)
            #         c.line(50,50,w-50,50)


########
            # if(lengAtributos[0] == const):
            #     c.drawString(90, linea, str(d.asunto))

            #     if (linea <= 52):
            #         c.showPage()
                
            #         generar_cabecera(c,h)
            #         c.setLineWidth(.2)
            #         c.line(50,50,w-50,50)
            
            # elif(lengAtributos[0] < const and len == lengAtributos[0]-1):
            #     c.drawString(90, linea, str(d.asunto))

            #     if (linea <= 52):
            #         c.showPage()
            #         linea = h-145
                
            #         generar_cabecera(c,h)
            #         c.setLineWidth(.2)
            #         c.line(50,50,w-50,50)


        # lineaSaltoA = limitar_letras(c, lAtributos, linea, w, h, fila, limites)

        # lineas = [lineaSaltoA[0] ,linea]
        # ,lineaSaltoL[0] ,lineaSaltoO[0] 

        # linea = min(lineas)

# def limitar_letras(c, atributos, linea, w, h, posAltura, limites):
#     len = 0
#     lineas = []

#     lin = linea

#     # for i in atributos[0]:
#     #     lenA+=1

#     lengs = []

#     cantidadAtributos = 0
#     for at in atributos:
#         cantidadAtributos += 1

#     for l in atributos:
#         lenS = 0
#         for a in l:
#             lenS+=1
#         lengs.append(lenS)
    
#     maxi = max(lengs)

#     indexM = 0
#     for j in lengs:
#         if j != maxi:
#             indexM += 1
#         else:
#             break

#     lengAtributos = []
#     att = 0
#     leng = 0

#     for i in atributos:
#         for i in atributos[att]:
#             leng+=1
#         att+=1
#         lengAtributos.append(leng)
#         leng = 0

#     ######### LO QUE ESTá PENDIENTE
#     lenCadenaActual = 0
#     lin = linea 
#     for a in str(atributos[indexM]):
#         indiceListaLimites = 0
#         for l in range(cantidadAtributos):
#             if (lenCadenaActual % limites[l]) == 0:
#                 indiceListaLimites += 1
#                 break
            
#         const = limites[indiceListaLimites]
#         print(indiceListaLimites)

#         # for ca in range(cantidadAtributos):
#         if (lengAtributos[indiceListaLimites] == const) :
#             c.drawString(posAltura[indiceListaLimites], lin, str(atributos[indiceListaLimites]))
#         elif (lengAtributos[indiceListaLimites] < const):
#             c.drawString(posAltura[indiceListaLimites], lin, str(atributos[indiceListaLimites]))
#             # elif (lengAtributos[ca] % const) == 0:
#             #     print(ca)
#             #     c.drawString(posAltura[ca], lin, str(atributos[ca]))
#             #     lin-=15

#         # indList = 0
#         # for i in range(3):
#         #     c.setFont('Helvetica', 10)

#         #     if (lengAtributos[i] == limites[i]):

#         #         c.drawString(posAltura[i], lin, str(atributos[i]))

#         #         if (lin <= 52):
#         #             c.showPage()
#         #             lin = linea
                
#         #             generar_cabecera(c,h)
#         #             c.setLineWidth(.2)
#         #             c.line(50,50,w-50,50)
                    


#             # elif ((lenCadenaActual % lim) == 0):
#             #     c.drawString(posAltura[indList], lin, str(atributos[indList])[lenCadenaActual-lim:lenCadenaActual])
#             #     lin-= 15

#             #     if (lin <= 52):
#             #         c.showPage()
#             #         lin = linea
                
#             #         generar_cabecera(c,h)
#             #         c.setLineWidth(.2)
#             #         c.line(50,50,w-50,50)
#             # indList +=1

#         lenCadenaActual += 1

#     lin-=10
#         # lineas.append(lin)
#         # lin = min(lineas)


#     # atts = 0
#     # for at in atributos:
#     #     const = limites[atts]

#     #     len = 0
#     #     lin = linea

#     #     for a in str(atributos[atts]):
            
#     #         len+=1
#     #         if(lengAtributos[atts] == const):
#     #             c.drawString(posAltura[atts], lin, str(atributos[atts]))

#     #             if (lin <= 52):
#     #                 c.showPage()
#     #                 lin = linea
                
#     #                 generar_cabecera(c,h)
#     #                 c.setLineWidth(.2)
#     #                 c.line(50,50,w-50,50)


#     #         elif((len % const) == 0):
#     #             limites[atts] = len
#     #             c.drawString(posAltura[atts], lin, str(atributos[atts])[limites[atts]-const:len]+'-')
#     #             lin-=15

#     #             if (lin <= 52):
#     #                 c.showPage()
#     #                 lin = h-145

#     #                 generar_cabecera(c,h)
#     #                 c.setLineWidth(.2)
#     #                 c.line(50,50,w-50,50)

                    
#     #         elif(len == lengAtributos[atts]):
#     #             restantes = lengAtributos[atts] - limites[atts]
#     #             c.drawString(posAltura[atts], lin, str(atributos[atts])[lengAtributos[atts]-restantes:lengAtributos[atts]])
#     #             lin-=15

#     #             if (lin <= 52):
#     #                 c.showPage()
#     #                 lin = h-145

#     #                 generar_cabecera(c,h)
#     #                 c.setLineWidth(.2)
#     #                 c.line(50,50,w-50,50)


#     #         elif(lengAtributos[atts] < const and len == lengAtributos[atts]-1):
#     #             c.drawString(posAltura[atts], lin, str(atributos[atts]))

#     #             if (lin <= 52):
#     #                 c.showPage()
#     #                 lin = h-145
                
#     #                 generar_cabecera(c,h)
#     #                 c.setLineWidth(.2)
#     #                 c.line(50,50,w-50,50)

            
#     #         c.setFont('Helvetica', 10)
#     #     atts+=1
#     #     lineas.append(lin)
#     #     lin = min(lineas)

#     return [lin, linea]

############# Metodos auxiliares sin usar

# @method_decorator(login_required, name='dispatch')
# class ReunionesView(View):
    
#     template = 'reuniones.html'

#     def get(self, request):
#         'GET method.'
#         reuniones = Reunion.objects.all()
#         zero = reuniones.count()

#         usuarioT = Usuarios.usuario.field

#         buscar = BuscarReunion(request.GET, queryset=reuniones)
#         reuniones = buscar.qs

#         context = {'reuniones': reuniones, 'buscar':buscar, 'zero':zero, 'usuarioT':usuarioT}
            
#         return render(request, self.template, context)

# @method_decorator(login_required, name='dispatch')
# class EditarReunion(UpdateView):
#     model = Reunion
#     fields = '__all__'
#     template_name = 'editar_reunion.html'
#     success_url = '/reuniones'

#   reunion_id = request.GET.get('reunirse', 1)
#   reunion_reunirse = Reunion1.objects.filter(id=reunion_id)
        
#   if reunion_reunirse.count() == 0:
#       reunirse = Reunion1.objects.first()
#   else:
#       reunirse = reunion_reunirse.first()
#  ''' 'reunirse': reunirse'''


# @method_decorator(login_required, name='dispatch')
# class EditarReunion(View):
#     template = 'editar_reunion.html'

#     def get(self, request, pk):
#         reunion = Reunion.objects.get(id=pk)
#         form = ReunionForm(request.GET, instance=reunion)
#         context = {'form': form}
#         return render(request, self.template, context)

#     def post(self, request, pk):
#         reunion = Reunion.objects.get(id=pk)
#         form = ReunionForm(request.POST, request.FILES, instance=reunion)
#         if form.is_valid():
#             # guardar reunion en la BD
#             instance = form.save(commit=False)
#             instance.usuario = request.user
#             instance.save()
#             return redirect('reuniones:list')
        
#         if not form.is_valid():
#             context = {'form': form}
#             return render(request, self.template, context)

# class EditarReuniones(UpdateView):
#     model = Reunion
#     fields = '__all__'
#     template_name = 'editar_reunion.html'
#     success_url = '/reuniones'
#     error_messages = {
#             'fecha': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#             'inicio': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#             'termino': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#             'lugar': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#             'asunto': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#             'observaciones': {
#                 'required': ('Campo obligatorio, Favor de llenar'),
#             },
#         }

# @method_decorator(login_required, name='dispatch')
# class FormWizardView(SessionWizardView):
#     template_name = 'crear_reunion1.html'
#     form_list = [Reunion1Form, Reunion2Form]

#     def done(self, form_list, **kwargs):
#         for form in form_list:
#                 print(form)
#                 form.save()
#         return HttpResponseRedirect('/reuniones')
#         # return render(self.request, 'reuniones.html', {
#         #     'form_data': [form.cleaned_data for form in form_list],
#         # })
    
#     def get(self, request, *args, **kwargs):
#         try:
#             return self.render(self.get_form())
#         except KeyError:
#             return super().get(request, *args, **kwargs)

#         # def post(self, request):
#         #     formReunion1 = Reunion1Form(request.POST, request.FILES)
#         #     formReunion2 = Reunion2Form(request.POST, request.FILES)

#         #     if not formReunion1.is_valid() and not formReunion2.is_valid():
#         #         context = {'formReunion1': formReunion1, 'formReunion2': formReunion2}
#         #         return render(request, self.template_name, context)

#         #     Reunion1.objects.create(
#         #         fecha=formReunion1.cleaned_data['fecha'],
#         #         inicio=formReunion1.cleaned_data['inicio'],
#         #         termino=formReunion1.cleaned_data['termino'],
#         #         lugar=formReunion1.cleaned_data['lugar']
#         #     )

#         #     Reunion2.objects.create(
#         #         asunto=formReunion1.cleaned_data['asunto'],
#         #         observaciones=formReunion1.cleaned_data['observaciones']
#         #     )
#         #     return redirect('/reuniones/')

# @method_decorator(login_required, name='dispatch')
# class AgregarReunion2(View):
#     template = 'crear_reunion2.html'

#     def get(self, request):
#         formReunion2 = Reunion2Form()
#         context = {'formReunion2':formReunion2}
#         return render(request, self.template, context)

#     def post(self, request):
#         formReunion2 = Reunion2Form(request.POST, request.FILES)

#         if not formReunion2.is_valid():
#             context = {'formReunion2': formReunion2}
#             return render(request, self.template, context)

#         Reunion2.objects.create(
#             asunto=formReunion2.cleaned_data['asunto'],
#             observaciones=formReunion2.cleaned_data['observaciones'],
#         )
#         return redirect('/reuniones/')

# @login_required(login_url='/accounts/login/')
# def borrar_oficio(request, pk):
#     reuniones = Reunion.objects.get(id=pk)
#     if request.method == 'POST':
#         reuniones.delete()
#         return redirect('reuniones:list')
#     context = {'reuniones': reuniones}
#     return render(request, 'borrar_reunion.html', context)