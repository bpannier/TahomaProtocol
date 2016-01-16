
Why this software package
=========================
I moved into an appartment with many blinds and windows which are IO Homecontrol enabled. The excitement were gone as
soon I figured out that IO is a closed protocol based on 833Mhz. Also after I bought the Tahoma box I was quite
disappointed as the system was closed as well and also all the interfaces are buggy and incomplete. The idea was to include
my IO devices into some other home automation system to make sure I have more fexibility and better interfaces.
I spent some time to debug the protocol to be able to build a library which everybody can use to control the
Tahoma system. The Tahoma system unfortunately depends on the Tahoma server in the Internet, you are not able to
control the local Tahoma box itself, at least yet. I wrote the Library in Python to learn the language and also as
my choice for an Homeautomations system is Indigo which support Python plugins. I made sure the Library runs under
Python Version 3.5 and also I had to make sure it runs under 2.5 as Indigo only supports this version as of today.

Where to start
==============
The main class you should look at is Protocol which provides all the entry points. Please see the documentation in
there and also I provided a lot of examples in the unit tests section.

What does the Tahoma App do
===========================
This library does not support all calls which the Tahoma App uses, just because I believe they are not needed when you
use an other home automation server to control your IO devices. Also I was not able to debug all states and there are
potentially more calls which have not been triggered in my debugging sessions.

When you look at the Tahoma Mobile App from a network perspective the usual flow of calls is as the following:

(POST is used by login, apply, getEvents and getStates all others use GET)

Setup
-----
login
getEndUser
getSetup
getActionGroups
../../enduserAPI/setup/interactiveNotifications/history
../../enduserAPI/setup/interactiveNotifications
../../enduserAPI/setup/conditionGroups
getCalendarDayList
getCalendarRuleList
getScheduledExecutions
getHistory
getSetupTriggers
getUserPreferences
getSetupOptions
getAvailableProtocolsType?gatewayId=<id>
getActiveProtocolsType?gatewayId=<id>
getSetupQuota?quotaId=smsCredit
../../enduserAPI/setup/gateways/<id>/version
getCurrentExecutions
refreshAllStates
getStates
getEvents

Apply for actions
-----------------
getEvents
getCurrentExecutions
apply
getEvents
getCurrentExecutions
getEvents
...
getEvents
getCurrentExecutions
getHistory
getEvents

Launch an action group
----------------------
getEvents
launchActionsGroup?oid=<oid>
getEvents
getCurrentExecutions
getEvents

Schedule launch of an action group
-----------------------------------
getEvents
scheduleActionGroup?oid=<oid>&delay=<milliseconds>
getEvents
getScheduledExecutions
getEvents

Cancel all executions
---------------------
getEvents
cancelExecutions
getEvents




