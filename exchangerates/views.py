from django.template.response import TemplateResponse

def home(req):
    
    # A dictionary of input data read from HTTP GET. If no input was given
    # we translate from EUR to HRK.
    to = req.GET.get('to', 'HRK')
    request = {'from':'EUR', 'to':to}
    
    # Pass the dictionary into the client's invoke method along with the name
    # of a service you want to invoke
    response = req.zato_client.invoke('exchangerates.get-exchange-rate-list', request)
    
    # response.data has a bunch of attributes that can be fed to the template as is
    return TemplateResponse(req, 'rates.html', {'data':response.data['rates'], 'to':to})