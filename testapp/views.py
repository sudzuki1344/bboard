from django.shortcuts import render

def test_cookie(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print('КУКИ РАБОТАЮТ!')
        else:
            print('КУКИ НЕ РАБОТАЮТ!')
    request.session.set_test_cookie()
    print('TEST COOKIE', request.session.test_cookie_worked())
    return render(request, 'testapp/test_cookie.html')
