from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from .models import Project, Block, Zone, Floor, TargetFloor, ActualFloor
from .forms import ProjectForm, UserForm, UpdateTargetFloorForm, UpdateActualFloorForm
import datetime
from rest_framework import viewsets
from .serializers import ProjectSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here.


def upload_video(request):
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        uploaded_video_url = fs.url(filename)
        return render(request, 'upload_video.html', {'uploaded_video_url': uploaded_video_url})
    return render(request, 'upload_video.html')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('project_name')
    serializer_class = ProjectSerializer


def welcomePage(request):
    context = {}
    return render(request, 'base/welcome.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

        # username = request.POST.get('username').lower()
        # password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, 'User does not exist!')

        # user = authenticate(request, username=username, password=password)

        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     messages.error(request, 'Username or password does not exist!')

    form = AuthenticationForm()
    context = {"form": form}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('welcome')


@login_required(login_url='login')
def userHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user_list = User.objects.filter(username__icontains=q)
    user_count = user_list.count()
    context = {'user_list': user_list, 'user_count': user_count}
    return render(request, 'base/user-home.html', context)


@login_required(login_url='login')
def users(request, pk):
    user_list = User.objects.get(id=pk)
    context = {'user_list': user_list}
    return render(request, 'base/users.html', context)


@login_required(login_url='login')
def createUser(request):
    page = 'create_user'
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # messages.success(request, "Registration successful.")
            return redirect('user-home')

            # user = form.save(commit=False)
            # user.username = user.username.lower()
            # user.set_password(user.password)
            # user = User.objects.create_user(user.username, '', user.password)
            # user.save()
            # return redirect('user-home')
        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")

    context = {'form': form, 'page': page}
    return render(request, 'base/register_user.html', context)


@login_required(login_url='login')
def updateUser(request, pk):
    page = 'update_user'
    user = User.objects.get(id=pk)
    form = SetPasswordForm(user)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, "Your password has been changed")
            return redirect('user-home')
        else:
            for error in list(form.errors.values()):
                messages.error(
                    request, "Please check both your password and confirm password.")

    # if request.method == 'POST':
    #     form = UserForm(request.POST, instance=user)
    #     if form.is_valid():
    #         user = form.save()
    #         user.set_password(user.password)
    #         user.save()
    #         return redirect('user-home')

    context = {'form': form, 'page': page}
    return render(request, 'base/register_user.html', context)


@login_required(login_url='login')
def deleteUser(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('user-home')

    return render(request, 'base/delete.html', {'obj': user})


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    project_list = Project.objects.filter(project_name__icontains=q)
    project_count = project_list.count()
    context = {'project_list': project_list, 'project_count': project_count}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def projects(request, pk):
    project_list = Project.objects.get(id=pk)
    blocks = project_list.projectblocks.all()
    zones = project_list.projectzones.all()
    floors = project_list.projectfloors.all()
    targetfloors = project_list.targetfloors.all()
    firstfloors = floors.first()
    actualfloors = project_list.actualfloors.all()
    context = {'project_list': project_list,
               'blocks': blocks, 'zones': zones, 'floors': floors, 'targetfloors': targetfloors, 'firstfloors': firstfloors, 'actualfloors': actualfloors}
    return render(request, 'base/projects.html', context)


@login_required(login_url='login')
def createTargetFloor(request, project_data):
    projects = Project.objects.get(id=project_data.pk)
    blocks = projects.projectblocks.all()
    zones = projects.projectzones.all()
    floors = projects.projectfloors.all()

    for block in blocks:
        latestfloors = projects.targetfloors.filter(block=block)
        for zone in zones:
            latestfloors1 = latestfloors.filter(zone=zone)
            for floor in floors:
                if latestfloors1.exists():
                    targetfloors = TargetFloor(
                        project=projects, block=block, zone=zone, floor=floor, target_due_date=latestfloors1.last().target_due_date+datetime.timedelta(days=6), target_floor_cycle=6)
                else:
                    targetfloors = TargetFloor(
                        project=projects, block=block, zone=zone, floor=floor, target_due_date=projects.start_date + datetime.timedelta(days=6), target_floor_cycle=6)
                targetfloors.save()


@login_required(login_url='login')
def updateTargetFloor(request, pk):
    page = 'update_targetfloor'
    targetfloor = TargetFloor.objects.get(id=pk)
    projects = Project.objects.get(id=targetfloor.project.pk)
    blocks = projects.projectblocks.filter(id=targetfloor.block.pk)
    zones = projects.projectzones.filter(id=targetfloor.zone.pk)
    floors = projects.projectfloors.all()
    form = UpdateTargetFloorForm(instance=targetfloor)

    if request.method == 'POST':
        form = UpdateTargetFloorForm(request.POST, instance=targetfloor)
        if form.is_valid():
            for block in blocks:
                targetfloor1 = projects.targetfloors.filter(block=block)
                for zone in zones:
                    targetfloor2 = targetfloor1.filter(zone=zone)
                    for floor in floors:
                        targetfloor3 = targetfloor2.filter(
                            id__gte=targetfloor.pk, floor=floor)
                        for targetfloors in targetfloor3:
                            if targetfloors.pk == targetfloor.pk:
                                floor_cycle_days = targetfloor.target_floor_cycle - targetfloors.target_floor_cycle
                                targetfloors.target_floor_cycle = targetfloors.target_floor_cycle+floor_cycle_days
                            targetfloors.target_due_date = targetfloors.target_due_date + \
                                datetime.timedelta(days=floor_cycle_days)
                            targetfloors.save()
            # messages.success(request, "Your password has been changed")
            return redirect('projects', pk=targetfloor.project.id)
        else:
            for error in list(form.errors.values()):
                messages.error(
                    request, "Please input the right value.")

    context = {'form': form, 'targetfloor': targetfloor, 'page': page}
    return render(request, 'base/targetfloor_form.html', context)


@login_required(login_url='login')
def createActualFloor(request, project_data):
    projects = Project.objects.get(id=project_data.pk)
    blocks = projects.projectblocks.all()
    zones = projects.projectzones.all()
    floors = projects.projectfloors.all()
    new_date = projects.start_date + datetime.timedelta(days=6)

    for block in blocks:
        latestfloors = projects.actualfloors.filter(block=block)
        for zone in zones:
            latestfloors1 = latestfloors.filter(zone=zone)
            for floor in floors:
                if latestfloors1.exists():
                    actualfloors = ActualFloor(
                        project=projects, block=block, zone=zone, floor=floor, actual_due_date=latestfloors1.last().actual_due_date+datetime.timedelta(days=6), actual_floor_cycle=6)
                else:
                    actualfloors = ActualFloor(
                        project=projects, block=block, zone=zone, floor=floor, actual_due_date=new_date, actual_floor_cycle=6)
                actualfloors.save()


@login_required(login_url='login')
def updateActualFloor(request, pk):
    page = 'update_actualfloor'
    actualfloor = ActualFloor.objects.get(id=pk)
    projects = Project.objects.get(id=actualfloor.project.pk)
    blocks = projects.projectblocks.filter(id=actualfloor.block.pk)
    zones = projects.projectzones.filter(id=actualfloor.zone.pk)
    floors = projects.projectfloors.all()
    form = UpdateActualFloorForm(instance=actualfloor)

    if request.method == 'POST':
        form = UpdateActualFloorForm(request.POST, instance=actualfloor)
        if form.is_valid():
            for block in blocks:
                actualfloor1 = projects.actualfloors.filter(block=block)
                for zone in zones:
                    actualfloor2 = actualfloor1.filter(zone=zone)
                    for floor in floors:
                        actualfloor3 = actualfloor2.filter(
                            id__gte=actualfloor.pk, floor=floor)
                        for actualfloors in actualfloor3:
                            if actualfloors.pk == actualfloor.pk:
                                floor_cycle_days = actualfloor.actual_floor_cycle - actualfloors.actual_floor_cycle
                                actualfloors.actual_floor_cycle = actualfloors.actual_floor_cycle+floor_cycle_days
                            actualfloors.actual_due_date = actualfloors.actual_due_date + \
                                datetime.timedelta(days=floor_cycle_days)
                            actualfloors.save()
            # messages.success(request, "Your password has been changed")
            return redirect('projects', pk=actualfloor.project.id)
        else:
            for error in list(form.errors.values()):
                messages.error(
                    request, "Please input the right value.")

    context = {'form': form, 'actualfloor': actualfloor, 'page': page}
    return render(request, 'base/actualfloor_form.html', context)


@login_required(login_url='login')
def load_blocks(request):
    project_id = request.GET.get('project')
    blocks = Block.objects.filter(project_id=project_id).order_by('block_name')
    context = {'blocks': blocks}
    return render(request, 'base/dropdown_blocks.html', context)


@login_required(login_url='login')
def load_zones(request):
    project_id = request.GET.get('project')
    zones = Zone.objects.filter(project_id=project_id).order_by('zone_name')
    context = {'zones': zones}
    return render(request, 'base/dropdown_zones.html', context)


@login_required(login_url='login')
def load_floors(request):
    project_id = request.GET.get('project')
    floors = Floor.objects.filter(project_id=project_id).order_by('floor_name')
    context = {'floors': floors}
    return render(request, 'base/dropdown_floors.html', context)


@login_required(login_url='login')
def createProject(request):
    page = 'create_project'
    form = ProjectForm()

    # if request.method == 'POST':
    #     form = ProjectForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_name = request.POST.get("project_name")
            manager_name = request.POST.get("manager_name")
            start_date = request.POST.get("start_date")
            due_date = request.POST.get("due_date")
            block_name_list = request.POST.getlist("block_name")
            zone_name_list = request.POST.getlist("zone_name")
            floor_name_list = request.POST.getlist("floor_name")

            block_info = zip(block_name_list)
            zone_info = zip(zone_name_list)
            floor_info = zip(floor_name_list)

            project_data = Project(
                project_name=project_name, manager_name=manager_name, start_date=start_date, due_date=due_date)

            project_data.save()

            for i in block_info:
                if not len(i[0]) == 0:
                    project_info_data = Block(
                        project=project_data, block_name=i[0])
                    project_info_data.save()

            for i in zone_info:
                if not len(i[0]) == 0:
                    project_info_data = Zone(
                        project=project_data, zone_name=i[0])
                    project_info_data.save()

            for i in floor_info:
                if not len(i[0]) == 0:
                    project_info_data = Floor(
                        project=project_data, floor_name=i[0])
                    project_info_data.save()

            createTargetFloor(request, project_data)
            createActualFloor(request, project_data)
            return redirect('home')

        else:
            messages.error(request, "Project details not valid.")

    context = {'form': form, 'page': page}
    return render(request, 'base/projects_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    page = 'update_project'
    projects = Project.objects.get(id=pk)
    blocks = projects.projectblocks.all()
    zones = projects.projectzones.all()
    floors = projects.projectfloors.all()
    form = ProjectForm(instance=projects)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=projects)
        if form.is_valid():
            blocks.delete()
            zones.delete()
            floors.delete()
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
            id = projects.id
            project_name = request.POST.get("project_name")
            manager_name = request.POST.get("manager_name")
            start_date = request.POST.get("start_date")
            due_date = request.POST.get("due_date")
            block_name_list = request.POST.getlist("block_name")
            zone_name_list = request.POST.getlist("zone_name")
            floor_name_list = request.POST.getlist("floor_name")
            created = projects.created

            block_info = zip(block_name_list)
            zone_info = zip(zone_name_list)
            floor_info = zip(floor_name_list)

            project_data = Project(id=id, project_name=project_name, manager_name=manager_name,
                                   start_date=start_date, due_date=due_date, created=created)
            project_data.save()

            for i in block_info:
                if not len(i[0]) == 0:
                    project_info_data = Block(
                        project=project_data, block_name=i[0])
                    project_info_data.save()

            for i in zone_info:
                if not len(i[0]) == 0:
                    project_info_data = Zone(
                        project=project_data, zone_name=i[0])
                    project_info_data.save()

            for i in floor_info:
                if not len(i[0]) == 0:
                    project_info_data = Floor(
                        project=project_data, floor_name=i[0])
                    project_info_data.save()

            createTargetFloor(request, project_data)
            createActualFloor(request, project_data)
            return redirect('home')

        else:
            messages.error(request, "Project details not valid.")

    context = {'form': form, 'page': page,
               'blocks': blocks, 'zones': zones, 'floors': floors}
    return render(request, 'base/projects_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': project})


@login_required(login_url='login')
def menuPage(request):
    return render(request, 'base/menu.html', {})
