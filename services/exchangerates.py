# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from datetime import datetime
from traceback import format_exc

# anyjson
from json import loads

# lxml
from lxml import etree

# Zato
from zato.server.service import Service

class GetExchangeRateList(Service):
    class SimpleIO:
        response_elem = 'rates'
        input_required = ('from', 'to')
        output_required = ('provider', 'rate', 'ts')
        output_repeated = True

    def get_yahoo(self, from_, to):

        # Response template
        out = {'provider':'Yahoo! Finance', 'rate':None, 'ts':None}

        # Grab a connection by its name
        conn = self.outgoing.plain_http.get('Yahoo! Finance').conn

        # Y! Finance needs a query string in that format
        # ?s=HRKEUR=X&f=snl1d1t1ab
        url_params = {'s':'{}{}=X'.format(from_, to), 'f':'snl1d1t1ab'}

        # Invoking the .get method issues a GET request
        response = conn.get(self.cid, url_params)

        # Y! gives us a CSV response
        response = response.text.split(',')

        # The string we receive is something like
        # u'"EURHRK=X","EUR to HRK",7.4608,"6/14/2013","5:55pm",7.4629,7.4588\r\n'
        # and we need the 3rd item.
        out['rate'] = response[2]
        out['ts'] = datetime.utcnow().isoformat()

        return out

    def get_appspot(self, from_, to):
        out = {'provider':'AppSpot', 'rate':None, 'ts':None}

        # Grab a connection by its name
        conn = self.outgoing.plain_http.get('AppSpot ExchangeRates').conn

        # Google needs a query string in that format
        # ?from=USD&to=EUR&q=1
        url_params = {'from': from_, 'to': to}

        # Invoking the .get method issues a GET request
        response = conn.get(self.cid, url_params)

        # Convert the pseudo-JSON from
        # {lhs: "1 Euro",rhs: "7.46464923 Croatian kune",error: "",icc: true} ->
        # {"lhs": "1 Euro","rhs": "7.46464923 Croatian kune","error": "","icc": true}
        # so it can be parsed as JSON.
        json = response.text

        self.logger.info('get_appspot: channel:[%s], json: %s'%(str(self.channel), json))

        rate = loads(json)['rate']

        out['rate'] = rate
        out['ts'] = datetime.utcnow().isoformat()

        return out

    def get_ecb(self, from_, to):
        out = {'provider':'European Central Bank', 'rate':None, 'ts':None}

        # Grab a connection by its name
        conn = self.outgoing.plain_http.get('European Central Bank').conn

        response = conn.get(self.cid)
        xml = etree.fromstring(response.text.encode('utf-8'))

        ns = {'xref': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        rate = xml.xpath(
            "//xref:Cube[@currency='{}']/@rate".format(to), namespaces=ns)[0]

        out['rate'] = rate
        out['ts'] = datetime.utcnow().isoformat()

        return out

    def handle(self):
        from_ = self.request.input.get('from')
        to = self.request.input.to

        for func in(self.get_yahoo, self.get_appspot, self.get_ecb):
            try:
                rate = func(from_, to)
            except Exception, e:
                self.logger.warn('Caught an exception {}'.format(format_exc(e)))
            else:
                self.response.payload.append(rate)