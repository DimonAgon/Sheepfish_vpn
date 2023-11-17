from django.shortcuts import render, redirect


def vpnsite(request):
    if request.user.is_authenticated:
        return render(request, 'vpnsite.html')

    else:
        return redirect('authorization')
