from django.shortcuts import render


def show_index(request):
    return render(
        request,
        "index.html",
        {
            "nama": "Christopher Evan Tanuwidjaja",
            "kelas": "A",
            "app_name": "main"
        }
    )
