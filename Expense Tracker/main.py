import flet
from flet import *

def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'



    #First page 
    first_page_contents=Container(
        content=Column(
            controls=[Row(alignment='spaceBetween',
                        controls=[Container(on_click=lambda e:shrink(e),
                                            content=Icon(icons.ARROW_FORWARD)),
                                  Container(on_click=lambda _:page.go('/create_task'),
                                            content=Icon(icons.ADD))]
                                            )
                                        ]
                                    )
                                )


    page_1= Container(width=350,
                height=650,
                bgcolor=BG,
                padding=20,
                content=Column(
                    controls=[Container(height=17),
                        Container(on_click=lambda e:restore(e),
                            content=Icon(icons.ARROW_BACK)),
                            Container(height=17),
                            Row(controls=[Icon(icons.ANALYTICS_SHARP),Container(content=Text('Analysis'),border_radius=5,ink=True,on_click=lambda _:page.go('/Analysis'))]),
                            Container(height=17),
                            Row(controls=[Icon(icons.CATEGORY_SHARP),Container(content=Text('Category'),border_radius=5,ink=True,on_click=lambda _:page.go('/Categories'))]),
                            Container(height=17),
                            Row(controls=[Icon(icons.DATA_ARRAY_SHARP),Container(content=Text('Dataput'),border_radius=5,ink=True,on_click=lambda _:page.go('/create_task'))]),
                            Container(height=17),
                            Row(controls=[Icon(icons.SETTINGS),Container(content=Text('Settings'),border_radius=5,ink=True,on_click=lambda _:page.go('/Settings'))]),
                            Container(height=17),
                            Row(controls=[Icon(icons.EXIT_TO_APP_SHARP),Container(content=Text('Exit'),border_radius=5,ink=True,on_click=lambda _:page.go('/Exit'))])

                            ]
                        )
                     )

    
    page_2= Row(alignment='end',#when animation happens it should move to right , default left  
        controls=[
            Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                animate=animation.Animation(600,AnimationCurve.DECELERATE),
                animate_scale=animation.Animation(400,AnimationCurve.DECELERATE),
                padding=padding.only(top=50,left=20,
                                     right=20,bottom=5 ),
                content=Column(
                    controls=[
                        first_page_contents
                        ]
                    )
                )
            ]
        )

    container=Container(
                         width=350,
                         height=650, 
                         bgcolor=BG,
                         border_radius=35,
                         content=Stack(
                            controls=[
                            page_1,
                            page_2
                        ]
                    )
                )
    Category_contents=Container(on_click=lambda _:page.go('/'),
                                  content=Text(value='X'))
    
    #routing info
    pages={'/':View('/',[container]),
            '/create_task':View('/create_task',[Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                padding=20,
                content=Container(on_click=lambda _:page.go('/'),
                                  content=Text(value='X'))
                )]),'/Analysis':View('/Analysis',[Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                padding=20,
                content=Container(on_click=lambda _:page.go('/'),
                                  content=Text(value='X'))
                                  
                )]),'/Categories':View('/Categories',[Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                padding=20,
                content=Category_contents
                
                )]),
                '/Settings':View('/Settings',[Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                padding=20,
                content=Container(on_click=lambda _:page.go('/'),
                                  content=Text(value='X')),
                
                )]),
                '/Exit':View('/Exit',[Container(
                width=350,
                height=650, 
                bgcolor=FG,
                border_radius=35,
                padding=20,
                content=Container(on_click=lambda _:page.go('/'),
                                content=Text(value='X'))
                )])
    }

    #Route functions
    def shrink(e):
        page_2.controls[0].width=150
        page_2.controls[0].scale=transform.Scale(0.8,alignment.center_right)
        page_2.update()

    def restore(e):
        page_2.controls[0].width=350
        page_2.controls[0].scale=transform.Scale(1,alignment.center_right)
        page_2.update()
    def change_route(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
    
    page.on_route_change= change_route #when the route changes this function is called

    page.add(container)




flet.app(target=main)
