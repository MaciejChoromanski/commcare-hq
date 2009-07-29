from xformmanager.models import *
from organization.models import *
from reporters.models import Reporter, ReporterGroup
import organization.utils as utils        

import datetime
from datetime import timedelta


def get_org_reportdata(organization, startdate, enddate):
    fullret = []    
    members, supervisors = utils.get_members_and_supervisors(organization)    
    is_first = True    
    
    fdefs = get_formdefs_for_domain(organization.domain)
    
    
    #[depth, type, item, get_aggregate_count(item, startdate, enddate)]
    
    
    for supervisor in supervisors:
        # leaving the hack in that everything after the first is expected
        # to have a "None" description.  This should be revisited
        try:
            username = ReporterProfile.objects.get(reporter=supervisor).chw_username   
            usercount = get_username_count(fdefs,[username], startdate, enddate)[username]        
        except Exception, e:
            logging.error("Error with reporter profile query: " + str(supervisor) + " :: " +  str(e))
            continue
        
        if is_first: 
            fullret.append([1,"Supervisors", supervisor, usercount])
            is_first = False
        else: 
            fullret.append([1,None, supervisor, usercount])            
    
    is_first = True #reset the first of the supervisors
    for member in members:
        
        try:
            username = ReporterProfile.objects.get(reporter=member).chw_username
            usercount = get_username_count(fdefs,[username], startdate, enddate)[username]
        except Exception, e:
            logging.error("Error with reporter profile query: " + str(member) + " :: " +  str(e))
            continue
        
        if is_first:            
            fullret.append([1,"Members", member, usercount])
            is_first = False
        else: 
            fullret.append([1,None, member, usercount])
    
    return fullret






def get_formdefs_for_domain(domain):
    return FormDefModel.objects.filter(domain=domain)

def get_username_count(formdef_lst, username_lst, timestart, timeend):
    """return a dictionary keyed by usernames and their corresponding meta form counts given a list of formdefs
    if the username_lst is None, then just do it over all users for a given formdef_lst
    
    this does not group by formdef.  if you want to do that, you should run each formdef individually.    
    """
    
    totalspan = timeend-timestart
    metas = Metadata.objects.filter(formdefmodel__in=formdef_lst).filter(timestart__gte=timestart).filter(timeend__lte=timeend)    
       
    if username_lst == None:    
        usernames = metas.values_list('username').distinct()
    else:
        #ReporterProfile.chw_username!
        usernames = metas.filter(username__in=username_lst).values_list('username').distinct()
    
    username_count_dict = {}
    for uname in usernames:
        username_count_dict[uname[0]] = []
   
   #need to go through each DAY and do the query each time.
    oneday = timedelta(days=1)
    for day in range(0,totalspan.days+1):        
        delta = timedelta(days=day)        
        target_start = timestart + delta    
        target_end = target_start + oneday
            
        dayslice = metas.filter(timestart__gte=target_start).filter(timeend__lt=target_end)
    
        for uname in usernames:
            username_count_dict[uname[0]].append(dayslice.filter(username=uname[0]).count())     
        
    return username_count_dict




