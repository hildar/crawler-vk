# Web crawler for parsing vk.com

## About

Web crawler scanning social net vk.com via an **API** (for example, the posts of one user known as BadComedian) and collects data about the people who liked and reposted this post. Wrote this data to **MongoDB** database.


### Stack:
* API: requests, API vk.com
* DataBase: MongoDB

### Task:
* Parse social net vk.com. Get information about posts who liked and reposted this.
* Code name: **BIG BRO**.
* Target: Social research. Research trends.
* Main project file: [Project_Parse_VK.py](https://github.com/hildar/parsing/blob/master/Project_Parse_VK.py)

## Usage

<img src="img/logs.png" alt="logs" width="700"/>

Then save to MongoDB information about users:

<img src="img/users.png" alt="users" width="550"/>

And groups:

<img src="img/clubs.png" alt="clubs" width="550"/>
