import flet
from flet import *
 

#SMALL ERROR PRESENT THE SELECTED INDEX DOES NOT CHANGE AFTER ROUTING 

def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'
    color_options = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']

#####################################################################################################################

    page.padding=0

    page.floating_action_button = FloatingActionButton(icon=icons.ADD_OUTLINED,
                                                       bgcolor=colors.WHITE,
                                                       foreground_color=colors.BLACK,
                                                       shape=CircleBorder(),
                                                       width=50,
                                                       on_click=lambda _:page.go('/Dataput'))
    
    page.floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = NavigationBar(
        bgcolor=colors.BLACK12,
        on_change=lambda e:changetab(e),
        destinations=[
            NavigationDestination(label='Home',icon=icons.HOME_OUTLINED,selected_icon=icons.HOME),
            NavigationDestination(label='Analysis',icon=icons.ANALYTICS_OUTLINED,selected_icon=icons.ANALYTICS),
            NavigationDestination(label='Categories',icon=icons.CATEGORY_OUTLINED,selected_icon=icons.CATEGORY),
            NavigationDestination(label='More',icon=icons.MORE_HORIZ_OUTLINED,selected_icon=icons.MORE_HORIZ),
                    ]
            )
    
#####################################################################################################################

    Home_Page_Contents=Row(                                                         #DAILY GRAPHS WILL APPEAR IN HOME PAGE
        controls=[Container(expand=True,
                        bgcolor=colors.CYAN,
                        padding=padding.only(top=50,left=20,
                                right=20,bottom=5),
                                content=Column()
                                        )
                                    ]
                                )
    
    Analysis_Page_Contents=Row(                                                     #ALL GRAPHS IN ANALYSIS PAGE
        controls=[Container(expand=True,
                        bgcolor=colors.TEAL,
                        padding=padding.only(top=50,left=20,
                                right=20,bottom=5),
                                content=Column()
                                        )
                                    ]
                                )


    Category_contents=Row(                                                             #TANISHQ CODE + PARTH SQL CODE HERE
        controls=[Container(expand=True,
                        bgcolor=colors.INDIGO,
                        padding=padding.only(top=50,left=20,
                                right=20,bottom=5),
                                content=Column()
                                        )
                                    ]
                                )
   
    More_Page_Contents=Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                                Row(
                                   controls=[Row(controls=[TextButton('Settings',icon=icons.SETTINGS,on_click=lambda _:page.go('/Settings'))])]),
                                Row(controls=[TextButton('EditDataPage',icon=icons.MONEY_OUTLINED,on_click=lambda _:page.go('/EditDataPage'))])
                           ]
                           )
                           )
                  ]
              )
    
    Dataput_Contents=Row(                                                   #PARTH CODE FOR PLUS BUTTON IN HOME SCREEN
            controls=[Container(expand=True,
                        bgcolor=FG,
                        padding=padding.only(top=50, left=20,
                                            right=20, bottom=5),
                        content=Column(controls=[
                            Row(
                                controls=[IconButton(on_click=lambda _: page.go('/'),
                                                    content=Icon(icons.CLOSE_ROUNDED))])
                        ]
                        )
                        )
                ]
            )
    
    Settings_Contents=Row(
        controls=[Container(expand=True,
                           bgcolor=colors.TEAL,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )
    EditDataPage_Contents=Row(                                                        #PARTH CODE FOR EDIT DATA PAGE
        controls=[Container(expand=True,
                           bgcolor=colors.TEAL,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )
    
#####################################################################################################################
    
    Home_Page= Container(expand=True,visible=True,content=Home_Page_Contents)

    Analysis_Page = Container(expand=True,visible=False,content=Analysis_Page_Contents)

    Category_Page = Container(expand=True,visible=False,content=Category_contents)

    More_Page = Container(expand=True,
                          visible=False,
                          content=More_Page_Contents)

    Initial_Page=Container(expand=True,
                           content=Row(
                               [
                                    Home_Page,
                                    Analysis_Page,
                                    Category_Page,
                                    More_Page

                                    ]
                                )
                            )
    

    
#####################################################################################################################

    pages={'/':View('/',[Initial_Page]),
           '/Dataput':View('/Dataput',[Container(expand=True,
                                                 bgcolor=BG,
                                                 content=Dataput_Contents)]),
            '/Settings':View('/Settings',[Container(
                expand=True,
                bgcolor=FG,
                content=Settings_Contents)]),
            '/EditDataPage':View('EditDataPage',[Container(
                expand=True,
                bgcolor=FG,
                content=EditDataPage_Contents

            )])
                }
    
#####################################################################################################################
    def changetab(e):
        my_index = e.control.selected_index
        Home_Page.visible = True if my_index == 0 else False
        Analysis_Page.visible = True if my_index == 1 else False
        Category_Page.visible = True if my_index == 2 else False
        More_Page.visible = True if my_index == 3 else False
        page.update()

    def savecurrentindexNavigation(e):
        pass


    def change_route(route):

        page.views.clear()
        page.views.append(
                pages[page.route]
                )
        
        if page.route=='/':

            page.views[-1].floating_action_button = FloatingActionButton(icon=icons.ADD,
                                                       bgcolor=colors.WHITE,
                                                       foreground_color=colors.BLACK,
                                                       shape=CircleBorder(),
                                                       on_click=lambda _:page.go('/Dataput'))
    
            page.views[-1].floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED

            page.views[-1].bottom_appbar = NavigationBar(
                        bgcolor=colors.BLACK12,
                        on_change=lambda e:changetab(e),
                        destinations=[
                            NavigationDestination(label='Home',icon=icons.HOME_OUTLINED,selected_icon=icons.HOME),
                            NavigationDestination(label='Analysis',icon=icons.ANALYTICS_OUTLINED,selected_icon=icons.ANALYTICS),
                            NavigationDestination(label='Categories',icon=icons.CATEGORY_OUTLINED,selected_icon=icons.CATEGORY),
                            NavigationDestination(label='More',icon=icons.MORE_HORIZ_OUTLINED,selected_icon=icons.MORE_HORIZ),
                            ])
            

            
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()

#####################################################################################################################

    page.add(
        Initial_Page
        )
    

    page.on_route_change= change_route 


flet.app(target=main)