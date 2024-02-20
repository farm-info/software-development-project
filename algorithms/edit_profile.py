from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect(reverse('view_profile'))

    else:
        form = UserChangeForm(instance=request.user)

        var = {'form': form}
        return render(request, 'accounts/edit_profile.html', var)