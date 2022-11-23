<div class="-space-y-px rounded-md shadow-sm">
            <div>
              <input 
              type="text"
              class='relative block w-full appearance-none rounded-lg border border-gray-300 p-3 placeholder-gray-500 focus:z-10 focus:border-secondary focus:outline-none focus:ring-secondary font-body text-base text-neutrals-g03'
              name="email"
              placeholder="youremail@email.com"
              required
              >
            </div>
            <div>
              <input 
              type="password"
              class='mt-4 relative block w-full appearance-none rounded-lg border border-gray-300 p-3 placeholder-gray-500 focus:z-10 focus:border-secondary focus:outline-none focus:ring-secondary font-body text-base text-neutrals-g03'
              name="password"
              placeholder="password"
              required
              >
            </div>
          </div>

<input type="hidden" name="remember" value="true">
        <div class="col-span-3">
          {{ form.first_name }}
        </div>
        <div class="col-span-3">
          {{ form.last_name }}
        </div>
        <div class="col-span-6">
          {{ form.email }}
        </div>
        <div class="col-span-3">
          {{ form.password }}
        </div>
        <div class="col-span-3">
          {{ form.password2 }}
        </div>

class StudentRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('student_course_list')
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(email=cd['email'],
                            password=cd['password'])
        login(self.request, user)
        return result

@login_required
def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect("profile", user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        #form.fields['description'].widget.attrs = {'rows': 1}
        return render(
            request=request,
            template_name="registration/profile.html",
            context={"form": form}
            )
    
    return redirect("featured_course_list")

def profile(request, email):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.email)
        else:
            print(form.errors)
        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(email=email).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['bio'].widget.attrs = {'rows': 4}
        return render(request, 'registration/profile.html', context={'form': form})

    return redirect("featured_course_list")