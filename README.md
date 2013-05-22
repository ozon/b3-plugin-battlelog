Battlelog plugin for [B3](http://www.bigbrotherbot.net/ "BigBrotherBot")
=============================================================================
This plugin extends B3 to the ability to obtain player data from Battlelog.
The Client Object gets a new property that includes a the `clanTag` and `platoonName`.
For players currently no functions are provided. Is interesting rather for plugin developers.

## Features
- retrieve player clantag and platoon from battlelog
- cache results

## Usage

### Requirements
- [BigBrotherBot](http://bigbrotherbot.net/)
- [Requests](http://docs.python-requests.org/en/latest/user/install.html#install)

### Installation
1. Copy the [extplugins/battlelog](extplugins/battlelog) folder into your `b3/extplugins` folder and
[extplugins/conf/plugin_battlelog.ini](extplugins/conf/plugin_battlelog.ini) into your `b3/conf` folder

2. This plugin requires the great requests module. That can be installed with the command `easy_install requests`.

3. Import the table structure [sql/battlelog_users.sql](sql/battlelog_users.sql) into your b3 database

4. Add the following line in your b3.xml file (below the other plugin lines)
```xml
<plugin name="battlelog" config="@conf/plugin_battlelog.ini"/>
```
