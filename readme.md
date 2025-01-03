# Calender Event Generator for svmmetider

This is a small tool that converts the svmmetider web site event list into a calenendar format compatible with modern calendar systems. This allows you to overlay a swim events calendar on top of your private or work calendar. 

Base website: https://xn--svmmetider-1cb.dk/

The script will fetch the events and produce a number of `*.ics` files which can be imported into most calendar systems.

The script is also linked to a set of public google calendars (through a google service account). The calendars is as follows:

* Swimming meet (all of Denmark)
  * Web url: https://calendar.google.com/calendar/embed?src=ui9jr9vao6nacsckiss2ri1g50%40group.calendar.google.com&ctz=Europe%2FCopenhagen
  * iCal url: https://calendar.google.com/calendar/ical/ui9jr9vao6nacsckiss2ri1g50%40group.calendar.google.com/public/basic.ics
* Swimming meet (Jylland)
  * Web url: https://calendar.google.com/calendar/embed?src=jhpu1liovjefu5mbj5ui4uj8j4%40group.calendar.google.com&ctz=Europe%2FCopenhagen
  * iCal url: https://calendar.google.com/calendar/ical/jhpu1liovjefu5mbj5ui4uj8j4%40group.calendar.google.com/public/basic.ics

<!---
* Swimming meet (Jylland, Odder selection)
 * Web url: https://calendar.google.com/calendar/embed?src=cnc7r2d4qfhp0qhu5js17l91bc%40group.calendar.google.com&ctz=Europe%2FCopenhagen
 * iCal url: https://calendar.google.com/calendar/ical/cnc7r2d4qfhp0qhu5js17l91bc%40group.calendar.google.com/public/basic.ics
-->

## Adding a shared calendar to your google calendar
https://support.google.com/calendar/answer/37100?hl=en&co=GENIE.Platform%3DDesktop

Use a link to add a public calendar
Important: You can only add a calendar with a link if the other person's calendar is public. Learn more about public calendars.

* On your computer, open Google Calendar.
* On the left, next to "Other calendars," click Add Add other calendars and then From URL.(iCal)
* Enter the calendar's address.
* Click Add calendar. The calendar appears on the left, under "Other calendars."

*Tip: It might take up to 12 hours for changes to show in your Google Calendar.*  

### Apple Google
In case you have added the shared calendar to your google account but cannot see it on your apple device. Then you might need to visit this link to enable:

https://calendar.google.com/calendar/syncselect

## Adding a shared calendar directly to your IPhone

* Go to Settings
* Passowrds and Accounts
* Add Account
* Other
* Add Subscribed Calendar

  

  
* Server add one of the urls for iCal from above e.g. https://calendar.google.com/calendar/ical/jhpu1liovjefu5mbj5ui4uj8j4%40group.calendar.google.com/public/basic.ics
* Complete the wizard. No need to add username and password as the calendar is public. 
* You should now be able to see the calendar in the Calendar app
