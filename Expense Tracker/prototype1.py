import flet
from flet import *



def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'



    page.padding=0
    
    #First page
    first_page_contents=Container(
        content=Column(
            controls=[Row(alignment='spaceBetween',
                        controls=[IconButton(on_click=lambda e:shrink(e),
                                            content=Icon(icons.ARROW_FORWARD)),
                                  IconButton(on_click=lambda _:page.go('/Dataput'),
                                            content=Icon(icons.ADD))]
                                            )
                                        ]
                                    )
                                )

    page_1= Container(expand=True,
                bgcolor=BG,
                padding=20,
                content=Column(
                    controls=[Container(height=17),
                        IconButton(on_click=lambda e:restore(e),
                            content=Icon(icons.ARROW_BACK)),
                            Container(height=17),
                            Row(controls=[TextButton('Analysis',icon=icons.ANALYTICS_SHARP,on_click=lambda _:page.go('/Analysis'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Categories',icons.CATEGORY_SHARP,on_click=lambda _:page.go('/Categories'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Dataput',icon=icons.DATA_ARRAY_SHARP,on_click=lambda _:page.go('/Dataput'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Settings',icon=icons.SETTINGS,on_click=lambda _:page.go('/Settings'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Exit',icon=icons.EXIT_TO_APP_SHARP,on_click=lambda _:page.go('/Exit'))])

                            ]
                        )
                     )

    
    page_2= Row(alignment='end',#when animation happens it should move to right , default left  
        controls=[
            Container(expand=True,
                bgcolor=FG,
                animate=animation.Animation(600,AnimationCurve.DECELERATE),
                animate_scale=animation.Animation(400,AnimationCurve.DECELERATE),
                padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                content=Column(
                    controls=[
                        first_page_contents
                        ]
                    )
                )
            ]
        )

    container=Container(expand=True,
                         bgcolor=BG,
                        content=Stack(
                            controls=[
                            page_1,
                            page_2
                        ]
                    )
                )
    
    Category_contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    Dataput_contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    Analysis_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    Settings_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    

    Exit_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    

    #routing info
    pages={'/':View('/',[container]),
            '/Dataput':View('/Dataput',[Container(
                expand=True,
                bgcolor=FG,
                content=Dataput_contents
                                  
                )]),'/Analysis':View('/Analysis',[Container(
                expand=True,
                bgcolor=FG,
                content=Analysis_Contents
                                  
                )]),'/Categories':View('/Categories',[Container(
                expand=True,
                bgcolor=FG,
                content=Category_contents
                                  
                )]),
                
               
                '/Settings':View('/Settings',[Container(
                expand=True,
                bgcolor=FG,
                content=Settings_Contents
                
                )]),
                '/Exit':View('/Exit',[Container(
                expand=True,
                bgcolor=FG,
                content=Exit_Contents
                )])
    }

    #Route functions
    def shrink(e):
        page_2.controls[0].expand=False
        page_2.controls[0].width=page.width/2
        page_2.controls[0].scale=transform.Scale(0.8,alignment.center_right)
        page_2.update()


    def restore(e):
        page_2.controls[0].width=page.width
        page_2.controls[0].scale=transform.Scale(1,alignment.center_right)
        page_2.update()

    def change_route(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()

    
    page.on_route_change= change_route #when the route changes this function is called



    page.add(container)









flet.app(target=main)
