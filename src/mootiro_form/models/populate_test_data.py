# -*- coding: UTF-8 -*-
from __future__ import unicode_literals  # unicode by default
from datetime import datetime
from mootiro_form.models import *


def deprecated_insert_lots_of_data(hash_salt):
    User.salt = hash_salt
    t = transaction.begin()

    # Insert usernames
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


    # Insert some categories

    # Categories of 1st user

    cat1_user1 = FormCategory(name="desespero", description="AAAAAAAA", user=usuario1)
    sas.add(cat1_user1)

    cat2_user1 = FormCategory(name="estafermo", description="Tipo de boneco\
            com arma presa numa das pontas, usada para treino na Idade Media",\
            user=usuario1)
    sas.add(cat2_user1)

    cat3_user1 = FormCategory(name="Gazola", description="tagarela ou garganta", user=usuario1)
    sas.add(cat3_user1)

    cat4_user1 = FormCategory(name="Lonjura", description="Grande distancia", user=usuario1)
    sas.add(cat4_user1)

    cat5_user1 = FormCategory(name="Escabulhar", description="Descascar", user=usuario1)
    sas.add(cat5_user1)

    # Categories of 2nd user

    cat1_user2 = FormCategory(name="melancolica", description="Pura melancolia", user=usuario2)
    sas.add(cat1_user2)

    cat2_user2 = FormCategory(name="consequencia", description="Toda ação tem\
            uma", user=usuario2)
    sas.add(cat2_user2)

    cat3_user2 = FormCategory(name="mobiliado", description="Se há moveis na \
            casa", user=usuario2)
    sas.add(cat3_user2)

    cat4_user2 = FormCategory(name="eloquente", description='Um formulario\
            que sabe o que esta falando', user=usuario2)
    sas.add(cat4_user2)

    # Categories of 3rd user

    cat1_user3 = FormCategory(name="Deruchette", description="Machado de Assis\
    escreveu isso. Sei lá o que é",user=usuario3)
    sas.add(cat1_user3)

    cat2_user3 = FormCategory(name="Persefone", description="Da Persefonia",
            user=usuario3)
    sas.add(cat2_user3)

    cat3_user3 = FormCategory(name="estremecedor", description="Forms que \
                                  fazem alguém tremer", user=usuario3)
    sas.add(cat3_user3)

    cat4_user3 = FormCategory(name="casamento", description="Forms sobre o \
            pesadelo do Tiago", user=usuario3)
    sas.add(cat4_user3)

    cat5_user3 = FormCategory(name="ingenuidade", description="Forms que nao \
            sabem de nada", user=usuario3)
    sas.add(cat5_user3)

    # Insert some forms for 2nd user
    form1 = Form(name='Espanha', description='Dados para espanhóis',
            category=cat3_user2, user=usuario2)
    sas.add(form1)
    form2 = Form(name='tempestade', description= 'Dados sobre tempestades',
            category=cat3_user2, user=usuario2)
    sas.add(form2)
    form3_user2 = Form(name='adir', description='Sabia que adir é adicionar?',
            category=cat3_user2, user=usuario2)
    sas.add(form3_user2)
    form4_user2 = Form(name='Samba', description='Qual você quer no carnaval?',
            category=cat3_user2, user=usuario2)
    sas.add(form4_user2)
    form5_user2 = Form(name='Marvel', description='Qual gibi você prefere?',
            category=cat3_user2, user=usuario2)
    sas.add(form5_user2)
    form6_user2 = Form(name='Raios', description='Muttley, faca alguma coisa!',
            category=cat3_user2, user=usuario2)
    sas.add(form6_user2)
    form7_user2 = Form(name='Vim or Emacs', description='qual você prefere',
            category=cat1_user2, user=usuario2)
    sas.add(form7_user2)
    form7_user2 = Form(name='Machado de Assis', description='qual foi a melhor obra dele?',
            category=None, user=usuario2)
    sas.add(form7_user2)
    form8_user2 = Form(name='Jorge Luis Borges', description='qual foi a melhor obra dele?',
            category=None, user=usuario2)
    sas.add(form8_user2)
    form9_user2 = Form(name='Paulo Coelho', description='existe obra boa dele?',
            category=None, user=usuario2)
    sas.add(form9_user2)
    form10_user2 = Form(name='Charles Stross', description='qual foi a melhor obra dele?',
            category=None, user=usuario2)
    sas.add(form10_user2)
    form11_user2 = Form(name='Douglas Adams', description="what's not to love in it?",
            category=None, user=usuario2)
    sas.add(form11_user2)

    # Insert some forms for the rest of the users
    form3 = Form(name='censo', description = 'Censo populacional',
            category=None, user=usuario3)
    sas.add(form3)
    form1_user3 = Form(name='Yadda', description = 'Censo populacional',
            category=None, user=usuario3)
    sas.add(form1_user3)
    form4 = Form(name="Voluntariado", description="Dados sobre voluntariado",
            category=cat1_user1, user=usuario1)
    sas.add(form4)
    form5 = Form(name="Banqueiro", description="Dados sobre banqueiros",
            category=cat2_user1, user=usuario1)
    sas.add(form5)
    sas.flush()
    t.commit()


def insert_lots_of_data(password='igorigor', n_users='1', n_forms='5',
                        n_fields='100', n_entries='500'):
    if hasattr(User, 'nickname'):
        stravinsky = User(email='stravinsky@geniuses.ru', password=password,
            nickname='Igor Fyodorovich', real_name='Igor Stravinsky',
            is_email_validated=True)
    else:  # In CAS mode the User model has fewer properties
        stravinsky = User(email='stravinsky@geniuses.ru')
    sas.add(stravinsky)
    transaction.commit()

    # Arguments to this function come from a configuration file, that is why
    # they come as strings.
    n_users = int(n_users)
    n_forms = int(n_forms)
    n_fields = int(n_fields)
    n_entries = int(n_entries)

    t = transaction.begin()
    print('Creating test data: {0} users, {1} forms each, {2} fields each, ' \
        '{3} entries for each form. Total forms: {4}. Total fields: {5}. ' \
        'Total entries: {6}. Total questions answered: {7}.'
        .format(n_users, n_forms, n_fields, n_entries, n_users * n_forms,
            n_users * n_forms * n_fields, n_users * n_forms * n_entries,
            n_users * n_forms * n_fields * n_entries))
    start = datetime.utcnow()
    for i in xrange(0, n_users):
        if i == 0:
            u = sas.query(User).get(1)
        else:
            email = nick + '@somenteumteste.net'
            if hasattr(User, 'nickname'):
                nick = 'test' + unicode(i)
                real_name = 'User '+ unicode(i)
                u = User(nickname=nick, real_name=real_name, email=email,
                         password=password, is_email_validated=True)
            else:  # In CAS mode the User model has fewer properties
                u = User(email=email)
        print(u)
        sas.add(u)
        make_forms(u, n_forms=n_forms, n_fields=n_fields, n_entries=n_entries)

    sas.flush()
    t.commit()
    print('Test data created in {0}'.format(datetime.utcnow() - start))
    sas.remove()


def make_forms(user, n_forms=50, n_fields=50, n_entries=500, field_type=None):
    descr = 'Test form with an adequate number of characters for a description'
    for i in xrange(1, n_forms + 1):
        name = "form {0} of {1} for {2}".format(i, n_forms, user)
        form = Form(name=name, description=descr, category=None, user=user)
        print('   ' + unicode(form))
        sas.add(form)
        populate_form(form, n_fields=n_fields)
        collector = create_collector(form)
        create_entries(form, collector, n_entries)


def populate_form(form, n_fields=100, field_type=None,
                  description="Test field bruhaha"):
    if not field_type:
        field_type = sas.query(FieldType) \
            .filter(FieldType.name=='TextField').one()
    for i in range(1, n_fields + 1):
        label = 'Field ' + unicode(i)
        field = Field(label=label, description=description, help_text='',
                      title=label, position=i, required=False, typ=field_type,
                      form=form)
        sas.add(field)
        FieldOption(field=field, option='defaul', value='bruhaha ultra')
        FieldOption(field=field, option='enableLength', value='false')
        FieldOption(field=field, option='minLength', value='3')
        FieldOption(field=field, option='maxLength', value='9')
        FieldOption(field=field, option='enableWords', value='false')
        FieldOption(field=field, option='minWords', value='1')
        FieldOption(field=field, option='maxWords', value='2')


def create_collector(form):
    name = 'collector_' + form.name
    msg = 'Test Collector. Please do not use'
    tks_url = '_test_only_do_not_use_this_url'

    collector = PublicLinkCollector(name=name, thanks_message=msg,
                          thanks_url=tks_url, limit_by_date=False,
                          email_each_entry=False, on_completion='msg',
                          message_after_end=msg, message_before_start=msg,
                          form = form)
    sas.add(collector)
    return collector


def create_entries(form, collector, n_entries=500):
    for i in xrange(1, n_entries + 1):
        entry = Entry(entry_number=i, form=form, collector=collector)
        sas.add(entry)
        for field in form.fields:
            if field.typ.name == 'TextField':
                TextData(
                    field=field,
                    entry=entry,
                    value='Data {0} for field {1} of form {2}' \
                        .format(i, field.id, form.id),
                )
            else:
                raise RuntimeError('We do not fill out entries for {} yet.' \
                    .format(field.typ))

