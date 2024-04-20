import flet
from flet import *
 
#FEEL FREE TO CHANGE COLOURS


def main(page:Page):
    global on_start
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'
    CG='#201D1D'
    color_options = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
    on_start=True
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

    Dataput_Contents=Row(                                                   #PARTH CODE FOR PLUS BUTTON IN HOME SCREEN
            controls=[Container(expand=True,
                        bgcolor=FG,
                        padding=padding.only(top=50, left=20,
                                            right=20, bottom=5),
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
    

    EditDataPage_Contents=Row(                                                        #PARTH CODE FOR EDIT DATA PAGE
        controls=[Container(expand=True,
                           bgcolor=FWG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(
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

    
#####################################################################################################################
    
    Home_Page= Container(expand=True,visible=True,content=Home_Page_Contents)

    Analysis_Page = Container(expand=True,visible=False,content=Analysis_Page_Contents)

    Category_Page = Container(expand=True,visible=False,content=Category_contents)

    EditData_Page = Container(expand=True,
                          visible=False,
                          content=EditDataPage_Contents)

    Initial_Page=Container(expand=True,
                           content=Row(
                               [
                                    Home_Page,
                                    Analysis_Page,
                                    Category_Page,
                                    EditData_Page

                                    ]
                                )
                            )
    

    
#####################################################################################################################

    pages={'/':View('/',[Initial_Page]),
           '/Dataput':View('/Dataput',[Container(expand=True,
                                                 bgcolor=BG,
                                                 content=Dataput_Contents)],
                                        AppBar(leading=IconButton(icon=icons.ARROW_BACK,on_click=lambda _:page.go('/'),tooltip='Go back'),
                                                bgcolor=CG,
                                                title=Text('Expense today',size=20))),
            '/Settings':View('/Settings',[Container(
                expand=True,
                bgcolor=FG,
                content=Settings_Contents)])
                }
    
#####################################################################################################################
    def changetab(e):
        my_index = e.control.selected_index

        if my_index == 0:
            Home_Page.visible = True 
            page.appbar=AppBar(bgcolor=CG,title=Text('ExpenseTracker'))
        else:
            Home_Page.visible=False


        if my_index == 1:
            Analysis_Page.visible = True
            page.appbar=AppBar(bgcolor=CG,title=Text('Analysis'))
        else :
            Analysis_Page.visible = False


        if my_index == 2:
            Category_Page.visible = True
            page.appbar=AppBar(bgcolor=CG,title=Text('Categories'))
        else :
            Category_Page.visible = False


        if my_index == 3:
            EditData_Page.visible = True
            page.appbar=AppBar(bgcolor=CG,title=Text('Edit Data'))
        else :
            EditData_Page.visible = False

        page.update()


    def change_route(route):

        global on_start
        if page.route=='/':

            if on_start:
                
                page.add(Initial_Page)

                page.padding=0

                page.floating_action_button = FloatingActionButton(icon=icons.ADD_OUTLINED,
                                                       bgcolor=colors.WHITE,
                                                       foreground_color=colors.BLACK,
                                                       shape=CircleBorder(),
                                                       width=50,
                                                       on_click=lambda _:page.go('/Dataput'))
    
                page.floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED

                page.appbar=AppBar(bgcolor=CG,title=Text('ExpenseTracker',size=20))

                page.drawer = NavigationDrawer(
                            controls=[
                            Container(height=15),
                            Text(value='Profilephoto',text_align='center'),
                            Container(height=30),
                            Text(value='Username',text_align='center'),
                            Divider(thickness=2,color='white'),
                            NavigationDrawerDestination(
                                    label="Settings",
                                    icon=icons.SETTINGS_OUTLINED,
                                    ),
                            NavigationDrawerDestination(
                                    label="Another option idk",
                                    icon=icons.READ_MORE,
                                    )
                            ]
                )

                page.bottom_appbar = NavigationBar(
                        bgcolor=CG,
                        selected_index=0,
                        on_change=lambda e:changetab(e),
                        destinations=[
                        NavigationDestination(label='Home',icon=icons.HOME_OUTLINED,selected_icon=icons.HOME),
                        NavigationDestination(label='Analysis',icon=icons.ANALYTICS_OUTLINED,selected_icon=icons.ANALYTICS),
                        NavigationDestination(label='Categories',icon=icons.CATEGORY_OUTLINED,selected_icon=icons.CATEGORY),
                        NavigationDestination(label='EditData',icon=icons.DATASET_OUTLINED,selected_icon=icons.DATASET),
                        ]
                         )
                on_start=False
                
            else:
                page.views.pop()



        else:
            page.views.append(
                pages[page.route]
                )

            
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()
        on_start=False

#####################################################################################################################

    page.go('/')

    page.on_route_change= change_route 


flet.app(target=main)