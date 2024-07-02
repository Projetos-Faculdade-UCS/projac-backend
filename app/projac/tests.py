from django.test import TestCase
from django.utils import timezone
from .models import (
    Projeto, Area, SubArea, Pesquisador, PesquisadorProjeto, AgenciaFomento,
    ValorArrecadado, ProducaoAcademica
)

class AreaModelTests(TestCase):
    def test_create_area(self):
        area = Area.objects.create(nome="Engenharia", cor="#0000FF")
        self.assertEqual(area.nome, "Engenharia")
        self.assertEqual(area.cor, "#0000FF")

class SubAreaModelTests(TestCase):
    def test_create_subarea(self):
        area = Area.objects.create(nome="Engenharia", cor="#0000FF")
        subarea = SubArea.objects.create(nome="Software", area=area)
        self.assertEqual(subarea.nome, "Software")
        self.assertEqual(subarea.area, area)

class PesquisadorModelTests(TestCase):
    def test_create_pesquisador(self):
        pesquisador = Pesquisador.objects.create(
            nome="João",
            sobrenome="Silva",
            email="joao.silva@example.com",
            data_nascimento=timezone.now().date(),
            curriculo_lattes="http://example.com/lattes"
        )
        self.assertEqual(pesquisador.nome, "João")
        self.assertEqual(pesquisador.sobrenome, "Silva")
        self.assertEqual(pesquisador.email, "joao.silva@example.com")
        self.assertEqual(pesquisador.full_name, "João Silva")

class ProjetoModelTests(TestCase):
    def test_create_projeto(self):
        projeto = Projeto.objects.create(
            titulo="Projeto 1",
            objetivo="Objetivo do projeto",
            data_criacao=timezone.now().date(),
            valor_solicitado=1000.00,
        )
        self.assertEqual(projeto.titulo, "Projeto 1")
        self.assertEqual(projeto.objetivo, "Objetivo do projeto")
        self.assertEqual(projeto.valor_solicitado, 1000.00)

    def test_projeto_status(self):
        projeto = Projeto.objects.create(
            titulo="Projeto 1",
            objetivo="Objetivo do projeto",
            data_criacao=timezone.now().date(),
            valor_solicitado=1000.00,
            cancelado=True
        )
        self.assertEqual(projeto.status, "CANCELADO")
        projeto.cancelado = False
        projeto.data_conclusao = timezone.now().date()
        projeto.save()
        self.assertEqual(projeto.status, "CONCLUIDO")
        projeto.data_conclusao = None
        projeto.save()
        self.assertEqual(projeto.status, "EM_ANDAMENTO")

    def test_valor_total_arrecadado(self):
        projeto = Projeto.objects.create(
            titulo="Projeto 1",
            objetivo="Objetivo do projeto",
            data_criacao=timezone.now().date(),
            valor_solicitado=1000.00
        )
        ValorArrecadado.objects.create(
            valor=500.00, descricao="Doação A", data=timezone.now().date(), projeto=projeto
        )
        ValorArrecadado.objects.create(
            valor=300.00, descricao="Doação B", data=timezone.now().date(), projeto=projeto
        )
        self.assertEqual(projeto.valor_total_arrecadado, 800.00)

    def test_coordenador(self):
        projeto = Projeto.objects.create(
            titulo="Projeto 1",
            objetivo="Objetivo do projeto",
            data_criacao=timezone.now().date(),
            valor_solicitado=1000.00
        )
        pesquisador = Pesquisador.objects.create(
            nome="João",
            sobrenome="Silva",
            email="joao.silva@example.com",
            data_nascimento=timezone.now().date(),
            curriculo_lattes="http://example.com/lattes"
        )
        PesquisadorProjeto.objects.create(
            pesquisador=pesquisador, projeto=projeto, cargo="COORDENADOR"
        )
        self.assertEqual(projeto.coordenador, pesquisador)

class AgenciaFomentoModelTests(TestCase):
    def test_agencia_fomento(self):
        agencia = AgenciaFomento.objects.create(nome="CNPq", sigla="CNPq")
        self.assertEqual(agencia.nome, "CNPq")
        self.assertEqual(agencia.sigla, "CNPq")
        self.assertEqual(agencia.full_name, "CNPq (CNPq)")

class ProducaoAcademicaModelTests(TestCase):
    def test_producao_academica(self):
        projeto = Projeto.objects.create(
            titulo="Projeto 1",
            objetivo="Objetivo do projeto",
            data_criacao=timezone.now().date(),
            valor_solicitado=1000.00
        )
        producao = ProducaoAcademica.objects.create(
            titulo="Artigo 1",
            descricao="Descrição do artigo",
            tipo="Artigo",
            projeto=projeto
        )
        self.assertEqual(producao.titulo, "Artigo 1")
        self.assertEqual(producao.descricao, "Descrição do artigo")
        self.assertEqual(producao.tipo, "Artigo")
        self.assertEqual(producao.projeto, projeto)
