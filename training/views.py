from django.shortcuts import render


# Create views here.
def consultation_request(request):

    return render(request, "training/consultation.html")
