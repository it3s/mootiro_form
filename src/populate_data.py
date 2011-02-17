# -*- coding: UTF-8 -*-

from mootiro_form.models import User, Form, FormCategory, transaction,sas


t = transaction.begin()

User.salt = "Mootiro is awesome"
#Insert usernames
usuario1 = User(nickname='test1', real_name='Macarrao da Silva',
        email='test1@somenteumteste.net', password='test0000',
        is_email_validated=True)
sas.add(usuario1)

usuario2 = User(nickname='test2', real_name='Joao Stravinsky',
        email='test2@somenteumteste.net', password='test0000',
        is_email_validated=True)
sas.add(usuario2)

usuario3 = User(nickname='test3', real_name='Jarbas Stravinsky',
        email='test3@somenteumteste.net', password='test0000',
        is_email_validated=True)
sas.add(usuario3)

usuario4 = User(nickname='test4', real_name='Ivana Stravinsky',
        email='test4@somenteumteste.net', password='test0000',
        is_email_validated=True)
sas.add(usuario4)

usuario5 = User(nickname='test5', real_name='Maria da Graca Stravinsky',
        email='test5@somenteumteste.net', password='test0000',
        is_email_validated=True)
sas.add(usuario5)


#Insert some categories

#Categories of 1st user

cat1_user1 = FormCategory(name="desespero", description="AAAAAAAA", user=usuario1)
sas.add(cat1_user1)

cat2_user1 = FormCategory(name="estafermo", description='''Tipo de boneco com arma
                    presa numa das pontas, usada para treino na Idade Media''', user=usuario1)
sas.add(cat2_user1)

cat3_user1 = FormCategory(name="Gazola", description="tagarela ou garganta", user=usuario1)
sas.add(cat3_user1)

cat4_user1 = FormCategory(name="Lonjura", description="Grande distancia", user=usuario1)
sas.add(cat4_user1)

cat5_user1 = FormCategory(name="Escabulhar", description="Descascar", user=usuario1)
sas.add(cat5_user1)

#Categories of 2nd user

cat1_user2 = FormCategory(name="melancolica", description="Pura melancolia", user=usuario2)
sas.add(cat1_user2)

cat2_user2 = FormCategory(name="consequencia", description='''Toda acao tem
uma''', user=usuario2)
sas.add(cat2_user2)

cat3_user2 = FormCategory(name="mobiliado", description="Se ha moveis na \
        casa", user=usuario2)
sas.add(cat3_user2)

cat4_user2 = FormCategory(name="eloquente", description='''Um formulario
        que sabe o que esta falando''', user=usuario2)
sas.add(cat4_user2)

#Categories of 3rd user

cat1_user3 = FormCategory(name="Deruchette", description="Machado de Assis\
escreveu isso. Sei la o que e",user=usuario3)
sas.add(cat1_user3)

cat2_user3 = FormCategory(name="Persefone", description="Da Persefonia",
        user=usuario3)
sas.add(cat2_user3)

cat3_user3 = FormCategory(name="estremecedor", description="Forms que \
                              fazem alguem tremer", user=usuario3)
sas.add(cat3_user3)

cat4_user3 = FormCategory(name="casamento", description="Forms sobre o \
        pesadelo do Fernando", user=usuario3)
sas.add(cat4_user3)

cat5_user3 = FormCategory(name="ingenuidade", description="Forms que nao \
        sabem de nada", user=usuario3)
sas.add(cat5_user3)

#Insert some forms
form1 = Form(name='Espanha', description='Dados para espanhois', public=True,
        category=cat3_user2, user=usuario2)
sas.add(form1)

form2 = Form(name='censo', description = 'Censo Populacional', public=True,
        category=cat3_user3, user=usuario3)
sas.add(form2)
form3 = Form(name='tempestade', description= 'Dados sobre tempestades',
        public=True, category=cat3_user2, user=usuario2)
sas.add(form3)
form4 = Form(name="Voluntariado", description="Dados sobre voluntariado",
        public=True, category=cat1_user1, user=usuario1)
sas.add(form4)
form5 = Form(name="Banqueiro", description="Dados sobre banqueiros",
        public=True, category=cat2_user1, user=usuario1)
sas.add(form5)

sas.flush()
t.commit()