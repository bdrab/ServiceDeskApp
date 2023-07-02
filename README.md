# ServiceDeskApp

This is a implementation of ticketing system using python web framework - DJANGO. 

I wanted to create a simpy to use ticketing system which will be fully functional. 
The idea was to create system which will be able to support incident(INC) tickets. 
There is "knowledge base" feature which is build by every engineer(admin). 
Incident can be closed only if knowledge article is added to the ticket.
Thanks to that we can search in system by tag or category and find possible solutin for new ticket. 


The system was integrated with IoT device created on ESP8266 and SIM800L module.
This electronic platform was intened to handle all notification outside ticketing sytem. 
It has two main functionalites: 
  - acting as notification system, it sends a SMS to duty engineer everytime when new ticket is created outside business hours.
  - acting as a way to send message to requester from inc view.


Below some screenshots from app: 

- user views:
![ticket-raising](https://github.com/bdrab/ServiceDeskApp/assets/97404833/7d9d31f5-6942-4f7c-bae1-118776949bf0)
![user-dashboard](https://github.com/bdrab/ServiceDeskApp/assets/97404833/31ef617f-0d77-4c6b-a19f-7e70b27bebb9)
![user-inc](https://github.com/bdrab/ServiceDeskApp/assets/97404833/17f5a326-dc4d-4400-a1d5-57ea8edccbba)

- admin views:
  
![admin-dashboard](https://github.com/bdrab/ServiceDeskApp/assets/97404833/2ef9531b-4c22-477d-83f4-6e62f556df51)
![admin-inc](https://github.com/bdrab/ServiceDeskApp/assets/97404833/eb9ce2ec-035c-4228-9ac2-342813d05b41)
![kb-search](https://github.com/bdrab/ServiceDeskApp/assets/97404833/56795a95-92d0-49c0-ae24-4089c2a74a5d)
![kb-article](https://github.com/bdrab/ServiceDeskApp/assets/97404833/680ac3f0-2d14-407a-b0e5-33221401f472)
![admin-inc-new-knowledge](https://github.com/bdrab/ServiceDeskApp/assets/97404833/84deb05b-1e08-4988-871b-bf5e9bb61ad4)


IoT device: 

![357316252_781518137004577_6042032337494715801_n](https://github.com/bdrab/ServiceDeskApp/assets/97404833/385e7b8a-b453-480e-bf6d-a6f371fd3335)
