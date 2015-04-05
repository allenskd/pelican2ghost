#### Pelican2Ghost

This plugin will actively export your data to Ghost JSON structure. You can use it to export your data from Pelican to Ghost. 


##### How to use? 


    git clone git@github.com:allenskd/pelican2ghost.git
    
Open your **pelicanconf.py** and add

    PLUGIN_PATHS = ['/my/base/path']
    PLUGINS = ['pelican2ghost']

You can run `./develop_server.sh start` (or restart) multiple times. The data dump will be generated in your pelican folder `/path/to/your/website/folder/ghost_export`. A file called pelican2ghost.json will be there.

##### Additional notes

This exporter does not support exporting tags, only categories for the time being. Feel free to submit pull requests if you have worked on a solution for it. This also doesn't export Pages, only articles.



