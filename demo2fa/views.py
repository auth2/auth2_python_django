# Source code provided under FreeBSD License as described below. 
# If you need any other type please write us at lic@auth2.com
"""
Copyright (c) 2012 Auth2.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from auth2api_r1 import *
from forms import *
from models import *
import random

import logging

logger = logging.getLogger(__name__)

def home(request):
      variables = RequestContext(request, {'request':request})
      return render_to_response('index.html',variables)

def register(request):
  form = None
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      username=form.cleaned_data['username']
      user = User.objects.create_user(username=username,password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
      phone = form.cleaned_data['phone']
      profile = user.profile
      profile.phone = phone
      profile.save()
      variables = RequestContext(request, {'request':request})
      return render_to_response('accounts/success.html',variables)                
  if not form:
    form = RegistrationForm()

  variables = RequestContext(request, {'request':request, 'form': form})
  return render_to_response('accounts/register.html',variables)

def login_username_password(request):
    if request.POST:        
        username = request.POST.get('username', '')
        password = request.POST.get('password','')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:                
                phone_number = user.profile.phone

                request.session['username'] = username
                request.session['password'] = password
                key = random.randint(10001,99999)

                print key

                json_resp = send_key(settings.AUTH2_API_KEY, settings.AUTH2_API_SECRET, phone_number, key)
                #todo: check return values if the call was successful

                request.session['session_login_key']= str(key)
                variables = RequestContext(request, {'request':request})
                return render_to_response('accounts/login_2nd.html',variables)                
            else:
                status_reason = 'Account disabled.'
                variables = RequestContext(request, {'error_title': 'Account Disabled', 'error_message':'Your account is inactive'})
                return render_to_response('error.html',variables)
        else:
            logger.info("Login attempt failed. Wrong Username/Password. User = "+username)
    else:
        next = request.GET.get('next')
        if next is not None:            
            request.session['next'] = next

    form = AuthenticationForm(request.POST)
    variables = RequestContext(request, {'form': form})
    return render_to_response('accounts/login.html',variables)

def delete_login_session_values(request):
    if not request.session:
        return
    if request.session.has_key('username'):
        del request.session['username']
    if request.session.has_key('password'):
        del request.session['password']
    if request.session.has_key('session_login_key'):
        del request.session['session_login_key']

def login_session_key(request):
    logger.debug("Function called: login_session_key");
    ipAddress = request.META['REMOTE_ADDR']
    if request.POST:
        #todo: password should not be stored in session
        username = request.session.get('username')
        password = request.session.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                key = request.POST.get('key', '')
                session_login_key = request.session.get('session_login_key','')  
                
                if key and key == session_login_key:
                    login(request, user)                    
                    delete_login_session_values(request)
                                       
                    next = request.session.get('next', '/')
                    return HttpResponseRedirect(next)
                else:                                        
                    #make sure user is not trying to guess- you may want to give a few attempts though (suggested maximum 3)
                    delete_login_session_values(request)
                    form = AuthenticationForm()
                    variables = RequestContext(request, {'form': form})
                    return render_to_response('accounts/login.html',variables)                                        
            else:
                logger.info('Account disabled. User = '+username )
                variables = RequestContext(request, {'error_title': 'Account Disabled', 'error_message':'Your account is inactive'})
                return render_to_response('error.html',variables)
        else:
            form = AuthenticationForm(request.POST)
            variables = RequestContext(request, {'request':request,'form': form})
            return render_to_response('accounts/login.html',variables)

    variables = RequestContext(request, {'request':request})
    return render_to_response('accounts/login_2nd.html',variables)



