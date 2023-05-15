
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms
from .filters import OrderFilter
from datetime import datetime
from django.core.paginator import Paginator

# Reportes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .filters import OrderFilter, OrderFilterRespuesta

# Models
from users.models import Usuarios
from .models import Oficio, OficioRespuesta

# Forms
from . import forms
from .forms import CreateOficio, UpdateOficio, UpdateStatus

# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import oficios

# from django.views.generic.edit import CreateView, UpdateView, DeleteView


@login_required(login_url="/accounts/login/")
def lista_oficios(request, *args, **kwargs):
    data = Oficio.objects.all()
    data2 = OficioRespuesta.objects.all()

    myFilter = OrderFilter(request.GET, queryset=data)
    data = myFilter.qs

    time = str(datetime.now())[0:16]

    num_valores_por_pagina = 10

    paginator = Paginator(data, num_valores_por_pagina)
    page_number = request.GET.get('page')
    oficios_page = paginator.get_page(page_number)

    num_oficios = 0

    for i in data:
        num_oficios += 1

    num_pages = num_oficios/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    reporte_v = 0
    
    if request.method == 'POST' and 'reporte' in request.POST:
        # llamamos a la funcion que genera los reportes
        reporte(data)
        reporte_v = 1
    else:
        reporte_v = 0

    context = {
        "data": data,
        "data2": data2,
        "myFilter": myFilter,
        "time": time,
        "num_pages": num_pages,
        "oficios_page": oficios_page,
        'reporte_v':reporte_v
    }

    return render(request, "oficios.html", context)


@login_required(login_url="/accounts/login/")
def lista_oficios_respuesta(request, *args, **kwargs):
    data_r = OficioRespuesta.objects.all()

    num_valores_por_pagina = 10

    paginator = Paginator(data_r, num_valores_por_pagina)
    page_number = request.GET.get('page')
    oficios_page = paginator.get_page(page_number)

    num_oficios = 0

    for i in data_r:
        num_oficios += 1

    num_pages = num_oficios/num_valores_por_pagina

    if num_pages > int(num_pages):
        num_pages = int(num_pages)+1

    context = {
        "data_r": data_r,
        "oficios_page": oficios_page,
        "num_pages": num_pages
    }
    return render(request, "oficios_respuesta.html", context)


@method_decorator(login_required, name='dispatch')
class AgregarOficio(View):
    template = 'crear_oficios.html'

    def get(self, request):
        formOficio = CreateOficio()
        context = {'form': formOficio}
        return render(request, self.template, context)

    def post(self, request):
        formOficio = CreateOficio(request.POST, request.FILES)
        context = {'form': formOficio}

        if not formOficio.is_valid():
            context = {'form': formOficio}
            return render(request, self.template, context)

        mes_form = int(str(datetime.now().date())[5:7])

        if mes_form == 1:
            mes_m = Oficio.MES.ENERO
        elif mes_form == 2:
            mes_m = Oficio.MES.FEBRERO
        elif mes_form == 3:
            mes_m = Oficio.MES.MARZO
        elif mes_form == 4:
            mes_m = Oficio.MES.ABRIL
        elif mes_form == 5:
            mes_m = Oficio.MES.MAYO
        elif mes_form == 6:
            mes_m = Oficio.MES.JUNIO
        elif mes_form == 7:
            mes_m = Oficio.MES.JULIO
        elif mes_form == 8:
            mes_m = Oficio.MES.AGOSTO
        elif mes_form == 9:
            mes_m = Oficio.MES.SEPTIEMBRE
        elif mes_form == 10:
            mes_m = Oficio.MES.OCTUBRE
        elif mes_form == 11:
            mes_m = Oficio.MES.NOVIEMBRE
        elif mes_form == 12:
            mes_m = Oficio.MES.DICIEMBRE

        Oficio.objects.create(
            folio=formOficio.cleaned_data['folio'],
            usuario=request.user,
            mes=mes_m,
            año=int(str(datetime.now().date())[0:4]),
            asunto=formOficio.cleaned_data['asunto'],
            documento=formOficio.cleaned_data['documento'],
            dependencia=formOficio.cleaned_data['dependencia'],
            turnado=formOficio.cleaned_data['turnado'],
        )

        rid = Oficio.objects.last()

        return redirect('oficios:list')

        # return redirect(f'/reuniones/agregar/participantes/{rid.folio}')

# @login_required(login_url="/accounts/login/")
# def crear_oficio(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = forms.CreateOficio(request.POST, request.FILES)
#         if form.is_valid():
#             # guardar oficio en la BD
#             instance = form.save(commit=False)
#             instance.usuario = request.user
#             instance.save()
#             return redirect('oficios:list')

#     else:
#         form = forms.CreateOficio()
#     return render(request, "crear_oficios.html", {'form': form})


@login_required(login_url="/accounts/login/")
def editar_oficio(request, pk):

    oficio = Oficio.objects.get(folio=pk)
    form_up = forms.UpdateOficio(instance=oficio)
    context = {'form_up': form_up}
    if request.method == 'POST':
        form_up = forms.UpdateOficio(
            request.POST, request.FILES, instance=oficio)
        if form_up.is_valid():
            # guardar oficio en la BD
            instance = form_up.save(commit=False)
            instance.usuario = request.user
            instance.save()
            return redirect('oficios:list')
    return render(request, "editar_oficio.html", context)


@login_required(login_url="/accounts/login/")
def change_status(request, pk):

    oficio = Oficio.objects.get(folio=pk)
    form_status = forms.UpdateStatus(instance=oficio)
    context = {'form_status': form_status}
    if oficio.estatus == 'NU':
        if request.method == 'POST':
            oficio.estatus = 'L'
            form_status = forms.UpdateStatus(request.POST, instance=oficio)
            if form_status.is_valid():
                instance = form_status.save(commit=False)
                instance.usuario = request.user
                instance.save()
                return redirect('oficios:list')
    return render(request, "oficios_confirmacion.html", context)

    # form_status = forms.UpdateStatus(instance=oficio)
    # context = {'form_status': form_status}
    # if request.method == 'POST':
    #     form_status = forms.UpdateStatus(
    #         request.POST, request.FILES, instance=oficio)
    #     if form_status.is_valid():
    #         # guardamos el nuevo status en la BD
    #         instance = form_status.save(commit=False)
    #         instance.usuario = request.user
    #         oficio.estatus = 'L'
    #         instance.save()
    #         print(oficio.estatus)
    #         return redirect('oficios:list')


@login_required(login_url="/accounts/login/")
def borrar_oficio(request, pk):
    oficio = Oficio.objects.get(folio=pk)
    if request.method == "POST":
        oficio.delete()
        return redirect('oficios:list')
    context = {'item': oficio}
    return render(request, "borrar_oficio.html", context)


@login_required(login_url="/accounts/login/")
def responder_oficio(request, pk):
    if request.method == 'POST':
        form = forms.CreateOficioDeRespuesta(
            request.POST, request.FILES, pk)
        if form.is_valid():
            # guardar oficio en la BD
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.id_oficio = Oficio.objects.get(folio=pk)
            instance.id_usuario = request.user
            instance.save()
            return redirect('oficios:list')
    else:
        form = forms.CreateOficioDeRespuesta()
    return render(request, "responder_oficio.html", {'form': form})


@login_required(login_url="/accounts/login/")
def agregar_dependencia(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.CreateDependency(request.POST, request.FILES)
        if form.is_valid():
            # guardar oficio en la BD
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            return redirect('oficios:list')
    else:
        form = forms.CreateDependency()
    return render(request, "crear_dependencias.html", {'form': form})


def buscar_oficio(request, *args, **kwargs):
    return render(request, "buscar_oficio.html")


# Funcion que Genera un pdf con los oficios
def reporte(self):
    w, h = letter

    time = str(datetime.now())[0:16]

    c = canvas.Canvas(
        f'static/pdf/reportes/oficios/Reporte-Oficios - {time}.pdf', pagesize=letter)

    # c = canvas.Canvas(
    #     f'static/pdf/reportes/oficios/Reporte-Oficios.pdf', pagesize=letter)

    c.setFont('Helvetica-Bold', 20)

    c.drawString(w/2-100, h - 75, 'Reporte - Oficios')

    generar_cabecera_oficios(c, h)

    # Lineas para formar el cuadrado de los titulos de las columnas
    c.line(45, h-130, w-45, h-130)
    c.line(45, h-130, 45, h-95)
    c.line(w-45, h-130, w-45, h-95)
    c.line(45, h-95, w-45, h-95)

    # Lineas que dividen las columnas en los titulos
    c.line(87, h-130, 87, h-95)
    c.line(151, h-130, 151, h-95)
    c.line(231, h-130, 231, h-95)
    c.line(321, h-130, 321, h-95)
    c.line(396, h-130, 396, h-95)
    c.line(496, h-130, 496, h-95)

    linea = h-145

    for l in self:
        c.setFont('Helvetica', 10)

        c.drawString(90, linea, str(l.fecha)[0:10])

        if str(l.estatus) == 'NU':
            c.drawString(505, linea, 'Nuevo')
        elif str(l.estatus) == 'NR':
            c.drawString(505, linea, 'No Revisado')
        elif str(l.estatus) == 'L':
            c.drawString(505, linea, 'Leído')
        elif str(l.estatus) == 'S':
            c.drawString(505, linea, 'Seguimiento')
        elif str(l.estatus) == 'C':
            c.drawString(505, linea, 'Completado')
        else:
            c.drawString(505, linea, 'N/A')

        # c.setLineWidth(.2)
        c.line(50, 50, w-50, 50)
        c.line(50, 45, w-50, 45)

        len = 0

        linAsunto = linea
        linUsr = linea
        linFolio = linea
        linDep = linea
        linTurn = linea

        finAsunto = 0
        finUsr = 0
        finFolio = 0
        finDep = 0
        finTurn = 0

        lenAsunto = 0
        for i in str(l.asunto):
            lenAsunto += 1

        lenUsr = 0
        for i in str(l.usuario.usuario):
            lenUsr += 1

        lenFolio = 0
        for i in str(l.folio):
            lenFolio += 1

        lenDep = 0
        for i in str(l.dependencia):
            lenDep += 1

        lenTurn = 0
        for i in str(l.turnado):
            lenTurn += 1

        for a in range(max([lenAsunto, lenUsr, lenFolio, lenDep, lenTurn])):

            len += 1

            if len > lenAsunto:
                pass

            elif(len == lenAsunto):
                restantesAsunto = lenAsunto - finAsunto
                c.drawString(405, linAsunto, str(l.asunto)[
                             lenAsunto-restantesAsunto:lenAsunto])
                linAsunto -= 15

                if (linAsunto <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            elif((len % 17) == 0):
                finAsunto = len
                c.drawString(405, linAsunto, str(
                    l.asunto)[finAsunto-17:len]+'-')
                linAsunto -= 15

                if (linAsunto <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            if len > lenUsr:
                pass

            elif (len == lenUsr):
                restantesUsr = lenUsr - finUsr
                c.drawString(160, linUsr, str(l.usuario.usuario)
                             [lenUsr-restantesUsr:lenUsr])
                linUsr -= 15

                if (linUsr <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            elif((len % 14) == 0):
                finUsr = len
                c.drawString(160, linUsr, str(
                    l.usuario.usuario)[finUsr-14:len]+'-')
                linUsr -= 15

                if (linUsr <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            if len > lenFolio:
                pass

            elif (len == lenFolio):
                restantesFolio = lenFolio - finFolio
                c.drawString(50, linFolio, str(l.folio)[
                             lenFolio-restantesFolio:lenFolio])
                linFolio -= 15

                if (linFolio <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            elif((len % 6) == 0):
                finFolio = len
                c.drawString(50, linFolio, str(l.folio)[finFolio-6:len]+'-')
                linFolio -= 15

                if (linFolio <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            if len > lenDep:
                pass

            elif (len == lenDep):
                restantesDep = lenDep - finDep
                c.drawString(240, linDep, str(l.dependencia)
                             [lenDep-restantesDep:lenDep])
                linDep -= 15

                if (linDep <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            elif((len % 10) == 0):
                finDep = len
                c.drawString(240, linDep, str(
                    l.dependencia)[finDep-10:len]+'-')
                linDep -= 15

                if (linDep <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            if len > lenTurn:
                pass

            elif (len == lenTurn):
                restantesTurn = lenTurn - finTurn
                c.drawString(330, linTurn, str(l.turnado)[
                             lenTurn-restantesTurn:lenTurn])
                linTurn -= 15

                if (linTurn <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

            elif((len % 8) == 0):
                finTurn = len
                c.drawString(330, linTurn, str(l.turnado)[finTurn-8:len]+'-')
                linTurn -= 15

                if (linTurn <= 52):
                    c.showPage()
                    linFolio = h-145
                    linAsunto = h-145
                    linUsr = h-145
                    linDep = h-145
                    linTurn = h-145

                    generar_cabecera_oficios(c, h)
                    c.setFont('Helvetica', 10)
                    c.setLineWidth(.2)
                    c.line(50, 50, w-50, 50)

        linea = min([linAsunto, linUsr, linFolio, linDep, linTurn])
        c.line(45, linea+7, w-45, linea+7)
        linea -= 5

    c.line(45, linea+12, 45, h-130)
    c.line(w-45, linea+12, w-45, h-130)

    c.line(87, linea+12, 87, h-130)
    c.line(151, linea+12, 151, h-130)
    c.line(231, linea+12, 231, h-130)
    c.line(321, linea+12, 321, h-130)
    c.line(396, linea+12, 396, h-130)
    c.line(496, linea+12, 496, h-130)

    c.drawImage('static/img/logounam.jpg', 60, h-85, 70, 70)
    c.drawImage('static/img/cigu.jpg', w-170, h-85, 110, 70)
    c.drawImage('static/img/pormiraza.jpg', w-370, h-50, 100, 30)

    c.save()


def generar_cabecera_oficios(c, h):

    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, h - 110, 'Folio')
    c.drawString(102, h - 110, 'Fecha')
    c.drawString(170, h - 110, 'Usuario')
    c.drawString(240, h - 110, 'Dependencia')
    c.drawString(330, h - 110, 'Turnado A')
    c.drawString(425, h - 110, 'Asunto')
    c.drawString(510, h - 110, 'Estatus')

# def limitar_letras(c, atributo, linea, w, h, posAltura, fin):
#     len = 0
#     lenA = 0

#     const = fin

#     for i in atributo:
#         lenA+=1

#     for a in str(atributo):
#         len+=1
#         if(lenA == const):
#             c.drawString(posAltura, linea, str(atributo))

#             if (linea <= 52):
#                 c.showPage()
#                 linea = h-145

#                 generar_cabecera_oficios(c,h)
#                 c.setLineWidth(.2)
#                 c.line(50,50,w-50,50)

#         elif((len % const) == 0):
#             fin = len
#             c.drawString(posAltura, linea, str(atributo)[fin-const:len]+'-')
#             linea-=15

#             if (linea <= 52):
#                 c.showPage()
#                 linea = h-145

#                 generar_cabecera_oficios(c,h)
#                 c.setLineWidth(.2)
#                 c.line(50,50,w-50,50)

#         elif(len == lenA):
#             restantes = lenA - fin
#             c.drawString(posAltura, linea, str(atributo)[lenA-restantes:lenA])
#             linea-=15

#             if (linea <= 52):
#                 c.showPage()
#                 linea = h-145

#                 generar_cabecera_oficios(c,h)
#                 c.setLineWidth(.2)
#                 c.line(50,50,w-50,50)

#         elif(lenA < const and len == lenA-1):
#             c.drawString(posAltura, linea, str(atributo))

#             if (linea <= 52):
#                 c.showPage()
#                 linea = h-145

#                 generar_cabecera_oficios(c,h)
#                 c.setLineWidth(.2)
#                 c.line(50,50,w-50,50)

#         c.setFont('Helvetica', 10)

#     return linea

# # Generate PDF
# def view_pdf(request):
#     # Create bytestream buffer
#     buf = io.BytesIO()
#     # Create canvas
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     # Create a text object
#     textobj = c.beginText()
#     textobj.setTextOrigin(inch, inch)
#     textobj.setFont("Helvetica", 14)

#     # Add some lines of text
#     lines = [
#         "This is line 1",
#         "This is line 2",
#         "This is line 3",
#     ]

#     # Loop
#     for line in lines:
#         textobj.textLine(line)

#     # Finish up
#     c.drawText(textobj)
#     c.showPage()
#     c.save()
#     buf.seef(0)

#     # Return
#     return FileResponse(buf, as_attachment=True, filename='oficio.pdf')

# font_variants = ("DejaVuSans","DejaVuSans-Oblique","DejaVuSans-Bold")
    # folder = '/usr/share/fonts/truetype/dejavu/'
    # for variant in font_variants:
    #     pdfmetrics.registerFont(TTFont(variant, os.path.join(folder, variant+'.ttf')))


@login_required(login_url="/accounts/login/")
def check_oficio(request, pk):

    oficio = Oficio.objects.get(folio=pk)
    oficio_respuesta = OficioRespuesta.objects.get(id_oficio_respuesta=pk)

    context = {
        # "oficio": oficio,
        "oficio_respuesta": oficio_respuesta
    }

    return render(request, "oficios.html", context)


def check_oficio(request, pk):
    oficio = get_object_or_404(Oficio, folio=pk)
    if oficio.oficiorespuesta.exists():
        messages.error(request, "Sorry can't be deleted.")
        return redirect('oficios:list')
