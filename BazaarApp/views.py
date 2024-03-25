from django.http import HttpResponse

def index(request):
    # Check the type of HTTP request
    if request.method == "GET":
        # If it's a GET request, return a response saying "This was a GET request"
        return HttpResponse("This was a GET request from BazaarBisharBlog project in BazaarApp app")
    elif request.method == "POST":
        # If it's a POST request, return a response saying "This was a POST request"
        return HttpResponse("This was a POST request from BazaarBisharBlog project in BazaarApp app")
