from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage, get_connection, EmailMultiAlternatives, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string

def test_cookie(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print('КУКИ РАБОТАЮТ!')
        else:
            print('КУКИ НЕ РАБОТАЮТ!')
    request.session.set_test_cookie()
    print('TEST COOKIE', request.session.test_cookie_worked())
    return render(request, 'testapp/test_email.html')


def test_mail(request):

    em = EmailMessage(subject='Test', body='Test', to=['user@supersite.kz'])
    em.send()

    em = EmailMessage(subject='Ваш новый пароль', body='Ваш новый пароль находится во вложении', attachments=[('password.txt', '1234234', 'text/plain')],
                      to=['user@supersite.kz'])
    em.send()

    # em = EmailMessage(subject='Запрошенный вами файл', body='Получите запрошенный вами файл',
    #                   to=['user@supersite.kz'])
    # em.attach_file('password.txt', '1234234', 'text/plain')
    # em.send()

    context = {'user': 'Вася Пупкин'}
    s = render_to_string('email/letter.txt', context)
    em = EmailMessage(subject='Оповещение', body=s, to=['user@supersite.kz'])
    em.send()

    # con = get_connection()
    # con.open()
    # email1 = EmailMessage(..., connection=con)
    # email1.send()
    #
    # email2 = EmailMessage(..., connection=con)
    # email2.send()
    #
    # email3 = EmailMessage(..., connection=con)
    # email3.send()
    # con.close()

    # con = get_connection()
    # con.open()
    # email1 = EmailMessage(subject='Ваш новый пароль', body='Ваш новый пароль находится во вложении', attachments=[('password.txt', '1234234', 'text/plain')],
    #                   to=['user@supersite.kz'])
    # email2 = EmailMessage(subject='Ваш новый пароль', body='Ваш новый пароль находится во вложении', attachments=[('password.txt', '1234234', 'text/plain')],
    #                   to=['user@supersite.kz'])
    # email3 = EmailMessage(subject='Ваш новый пароль', body='Ваш новый пароль находится во вложении', attachments=[('password.txt', '1234234', 'text/plain')],
    #                   to=['user@supersite.kz'])
    # con.send_messages([email1, email2, email3])
    # con.close()

    # em = EmailMultiAlternatives(subjects='Test', body='Test', to=['user@supersite.kz'])
    # em.attach_alternative('<h1>Test</h1>', 'text/html')
    # em.send()
    send_mail('Test email', 'Test!!!', 'webmaster@supersite.kz', ['user@othersite.kz'], html_message='<h1>Test!!!</h1>')

    msg1 = ('Подписка', 'Подтвердите пожалуйста подписку', 'subscribe@supersite.kz', ['user@supersite.kz', 'megauser@megasite.kz'])
    msg2 = ('Подписка', 'Ваша подписка подтверждена', 'subscribe@supersite.kz',
            ['user@supersite.kz', 'megauser@megasite.kz'])
    send_mass_mail((msg1, msg2), fail_silently=True)

    user = User.objects.get(username='admin')
    user.email_user('Подьём!', 'Admin, не спи!', fail_silently=True)

    return render(request, 'testapp/test_email.html')