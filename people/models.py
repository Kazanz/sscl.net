from __future__ import unicode_literals

import pytz
import re
from datetime import datetime, timedelta

from django.db import models

from people.helpers import unique_hash


class Waiver(models.Model):
    CARRIERS = (
        ("@sms.3rivers.net", "3 River Wireless"),
        ("@paging.acswireless.com", "ACS Wireless"),
        ("@txt.att.net", "AT&T"),
        ("@message.alltel.com", "Alltel"),
        ("@bplmobile.com", "BPL Mobile"),
        ("@bellmobility.ca", "Bell Canada"),
        ("@txt.bellmobility.ca", "Bell Mobility"),
        ("@txt.bell.ca", "Bell Mobility (Canada)"),
        ("@blueskyfrog.com", "Blue Sky Frog"),
        ("@sms.bluecell.com", "Bluegrass Cellular"),
        ("@myboostmobile.com", "Boost Mobile"),
        ("er@cwwsms.com", "Carolina West Wireless"),
        ("@mobile.celloneusa.com", "Cellular One"),
        ("@csouth1.com", "Cellular South"),
        ("@cwemail.com", "Centennial Wireless"),
        ("@messaging.centurytel.net", "CenturyTel"),
        ("@txt.att.net", "Cingular (Now AT&T)"),
        ("@msg.clearnet.com", "Clearnet"),
        ("@comcastpcs.textmsg.com", "Comcast"),
        ("@corrwireless.net", "Corr Wireless Communications"),
        ("@sms.mycricket.com", "Cricket"),
        ("@mobile.dobson.net", "Dobson"),
        ("@sms.edgewireless.com", "Edge Wireless"),
        ("@fido.ca", "Fido"),
        ("@sms.goldentele.com", "Golden Telecom"),
        ("@msg.fi.google.com", "Google fi"),
        ("@messaging.sprintpcs.com", "Helio"),
        ("@text.houstoncellular.net", "Houston Cellular"),
        ("@ideacellular.net", "Idea Cellular"),
        ("@ivctext.com", "Illinois Valley Cellular"),
        ("@inlandlink.com", "Inland Cellular Telephone"),
        ("@pagemci.com", "MCI"),
        ("@text.mtsmobility.com", "MTS"),
        ("@mymetropcs.com", "Metro PCS"),
        ("@page.metrocall.com", "Metrocall"),
        ("@my2way.com", "Metrocall 2-way"),
        ("@fido.ca", "Microcell"),
        ("@clearlydigital.com", "Midwest Wireless"),
        ("@mobilecomm.net", "Mobilcomm"),
        ("@messaging.nextel.com", "Nextel"),
        ("@onlinebeep.net", "OnlineBeep"),
        ("@pcsone.net", "PCS One"),
        ("@txt.bell.ca", "President's Choice"),
        ("@sms.pscel.com", "Public Service Cellular"),
        ("@qwestmp.com", "Qwest"),
        ("@pcs.rogers.com", "Rogers AT&T Wireless"),
        ("@pcs.rogers.com", "Rogers Canada"),
        ("@txt.bell.ca", "Solo Mobile"),
        ("@email.swbw.com", "Southwestern Bell"),
        ("@messaging.sprintpcs.com", "Sprint"),
        ("@messaging.sprintpcs.com", "Sprint"),
        ("@tms.suncom.com", "Sumcom"),
        ("@mobile.surewest.com", "Surewest Communicaitons"),
        ("@tmomail.net", "T-Mobile"),
        ("@msg.telus.com", "Telus"),
        ("@txt.att.net", "Tracfone"),
        ("@tms.suncom.com", "Triton"),
        ("@email.uscc.net", "US Cellular"),
        ("@uswestdatamail.com", "US West"),
        ("@utext.com", "Unicel"),
        ("@vtext.com", "Verizon"),
        ("@vmobl.com", "Virgin Mobile"),
        ("@vmobile.ca", "Virgin Mobile Canada"),
        ("@sms.wcc.net", "West Central Wireless"),
        ("@cellularonewest.com", "Western Wireless"),
    )

    created = models.DateTimeField(auto_now_add=True)
    first = models.CharField(max_length=40)
    last = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=16)
    carrier = models.CharField(max_length=40, choices=CARRIERS)
    dob = models.DateField()
    signature = models.CharField(max_length=40)
    confirmed = models.BooleanField(default=False, blank=True)
    sent = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=8, blank=True, null=True)

    def __unicode__(self):
        return self.first + " " + self.last

    def save(self, *args, **kwargs):
        self.phone = re.sub("\D", "", self.phone)
        super(Waiver, self).save(*args, **kwargs)

    def re_hash(self):
        three_days_ago = pytz.utc.localize(datetime.utcnow() - timedelta(days=3))
        if not self.sent or self.sent < three_days_ago:
            self.hash = unique_hash(Waiver, 'hash')
            self.confirmed = False
            self.save()
        return self.hash

    def confirm(self):
        self.hash = None
        self.confirmed = True
        self.save()

    @property
    def number(self):
        return self.phone + self.carrier