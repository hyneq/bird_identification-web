from django.shortcuts import render
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
@permission_required('stream.view_stream')
def index(request):
    return render(request, "stream/index.html")


@login_required
@permission_required('stream.view_stream')
def stream(request):
    """A fallback view for the WebRTC stream endpoint.
    Web server configuration should use the path as a reverse proxy
    to the actual WebRTC stream.
    """
    return HttpResponseServerError("This path should contain the raw WebRTC stream, you are getting this message most likely due to wrong web server configuration.")
